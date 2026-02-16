"""
Smart geocoding client using Builder pattern.
"""

from __future__ import annotations

import hashlib
import os
import random
import threading
import time
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Callable, Dict, Optional

import geocoder
import requests
from requests.adapters import HTTPAdapter


@dataclass
class RetryPolicy:
    max_retries: int = 2
    base_delay: float = 0.5
    factor: float = 2.0
    jitter: float = 0.2
    retry_statuses: Optional[set[int]] = None

    def should_retry_status(self, status: Optional[int]) -> bool:
        if status is None or self.retry_statuses is None:
            return False
        return status in self.retry_statuses

    def get_delay(self, attempt: int) -> float:
        base = self.base_delay * (self.factor**attempt)
        return base + random.uniform(0, self.jitter)


class InMemoryCache:
    def __init__(self, ttl_seconds: int) -> None:
        self._ttl_seconds = ttl_seconds
        self._store: Dict[str, tuple[float, Dict[str, Any]]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None
            expires_at, value = entry
            if time.time() >= expires_at:
                self._store.pop(key, None)
                return None
            return value

    def set(self, key: str, value: Dict[str, Any]) -> None:
        expires_at = time.time() + self._ttl_seconds
        with self._lock:
            self._store[key] = (expires_at, value)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()


class TimestampRateLimiter:
    def __init__(self, min_interval_seconds: float) -> None:
        self._min_interval = min_interval_seconds
        self._last_request = 0.0
        self._lock = threading.Lock()

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_request
            if elapsed < self._min_interval:
                time.sleep(self._min_interval - elapsed)
            self._last_request = time.monotonic()


class SmartGeocodingClient:
    def __init__(
        self,
        session: requests.Session,
        cache: Optional[InMemoryCache],
        rate_limiter: Optional[TimestampRateLimiter],
        retry_policy: Optional[RetryPolicy],
    ) -> None:
        self._session = session
        self._cache = cache
        self._rate_limiter = rate_limiter
        self._retry_policy = retry_policy

    def ip_lookup(self, ip: str) -> SimpleNamespace:
        return self._request(
            provider="ip",
            cache_key=f"ip:{ip}",
            rate_limit=False,
            fn=lambda: geocoder.ip(ip, session=self._session),
        )

    def osm_geocode(self, address: str) -> SimpleNamespace:
        return self._request(
            provider="osm",
            cache_key=f"osm:geocode:{address}",
            rate_limit=True,
            swallow_exceptions=True,
            fn=lambda: geocoder.osm(address, session=self._session),
        )

    def osm_reverse(self, latitude: float, longitude: float) -> SimpleNamespace:
        return self._request(
            provider="osm",
            cache_key=f"osm:reverse:{latitude},{longitude}",
            rate_limit=True,
            swallow_exceptions=True,
            fn=lambda: geocoder.osm(
                [latitude, longitude], method="reverse", session=self._session
            ),
        )

    def arcgis_geocode(self, address: str) -> SimpleNamespace:
        return self._request(
            provider="arcgis",
            cache_key=f"arcgis:geocode:{address}",
            rate_limit=False,
            fn=lambda: geocoder.arcgis(address, session=self._session),
        )

    def arcgis_reverse(self, latitude: float, longitude: float) -> SimpleNamespace:
        return self._request(
            provider="arcgis",
            cache_key=f"arcgis:reverse:{latitude},{longitude}",
            rate_limit=False,
            fn=lambda: geocoder.arcgis(
                [latitude, longitude], method="reverse", session=self._session
            ),
        )

    def _request(
        self,
        provider: str,
        cache_key: str,
        rate_limit: bool,
        fn: Callable[[], Any],
        swallow_exceptions: bool = False,
    ) -> SimpleNamespace:
        key = self._hash_key(provider, cache_key)
        cached = self._cache.get(key) if self._cache else None
        if cached:
            return SimpleNamespace(**cached)

        if rate_limit and self._rate_limiter:
            self._rate_limiter.wait()

        try:
            response = self._run_with_retry(fn)
            data = self._normalize_response(response)
        except Exception as exc:  # noqa: BLE001
            if not swallow_exceptions:
                raise
            data = {"ok": False, "error": str(exc)}

        if data.get("ok") and self._cache:
            self._cache.set(key, data)

        return SimpleNamespace(**data)

    def clear_cache(self) -> None:
        if self._cache:
            self._cache.clear()

    def _run_with_retry(self, fn: Callable[[], Any]) -> Any:
        if not self._retry_policy:
            return fn()

        last_exc: Optional[Exception] = None
        for attempt in range(self._retry_policy.max_retries + 1):
            try:
                response = fn()
                if self._should_retry_response(response):
                    delay = self._retry_policy.get_delay(attempt)
                    time.sleep(delay)
                    continue
                return response
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt >= self._retry_policy.max_retries:
                    raise
                delay = self._retry_policy.get_delay(attempt)
                time.sleep(delay)

        if last_exc:
            raise last_exc
        return fn()

    def _should_retry_response(self, response: Any) -> bool:
        status = getattr(response, "status", None)
        if status is None:
            status = getattr(response, "status_code", None)
        if not getattr(response, "ok", False) and self._retry_policy:
            return self._retry_policy.should_retry_status(status)
        return False

    @staticmethod
    def _hash_key(provider: str, cache_key: str) -> str:
        raw = f"{provider}:{cache_key}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    @staticmethod
    def _normalize_response(response: Any) -> Dict[str, Any]:
        return {
            "ok": bool(getattr(response, "ok", False)),
            "lat": getattr(response, "lat", None),
            "lng": getattr(response, "lng", None),
            "latlng": getattr(response, "latlng", None),
            "address": getattr(response, "address", None),
            "city": getattr(response, "city", None),
            "state": getattr(response, "state", None),
            "state_long": getattr(response, "state_long", None),
            "country": getattr(response, "country", None),
            "country_long": getattr(response, "country_long", None),
            "postal": getattr(response, "postal", None),
            "street": getattr(response, "street", None),
            "street_long": getattr(response, "street_long", None),
            "housenumber": getattr(response, "housenumber", None),
            "geojson": getattr(response, "geojson", None),
            "ip": getattr(response, "ip", None),
            "status": getattr(response, "status", None),
            "status_code": getattr(response, "status_code", None),
        }


class SmartClientBuilder:
    def __init__(self) -> None:
        self._pool_connections = 10
        self._pool_maxsize = 10
        self._pool_block = True
        self._cache: Optional[InMemoryCache] = None
        self._rate_limiter: Optional[TimestampRateLimiter] = None
        self._retry_policy: Optional[RetryPolicy] = None

    def with_connection_pooling(
        self,
        pool_connections: int = 10,
        pool_maxsize: int = 10,
        pool_block: bool = True,
    ) -> "SmartClientBuilder":
        self._pool_connections = pool_connections
        self._pool_maxsize = pool_maxsize
        self._pool_block = pool_block
        return self

    def with_distributed_cache(self, ttl_seconds: int = 3600) -> "SmartClientBuilder":
        self._cache = InMemoryCache(ttl_seconds=ttl_seconds)
        return self

    def with_rate_limiting(self, limit_per_second: float = 1.0) -> "SmartClientBuilder":
        min_interval = 1.0 / max(limit_per_second, 0.1)
        self._rate_limiter = TimestampRateLimiter(min_interval_seconds=min_interval)
        return self

    def with_retry_policy(
        self,
        max_retries: int = 2,
        base_delay: float = 0.5,
        factor: float = 2.0,
        jitter: float = 0.2,
        retry_statuses: Optional[set[int]] = None,
    ) -> "SmartClientBuilder":
        if retry_statuses is None:
            retry_statuses = {429, 500, 502, 503}
        self._retry_policy = RetryPolicy(
            max_retries=max_retries,
            base_delay=base_delay,
            factor=factor,
            jitter=jitter,
            retry_statuses=retry_statuses,
        )
        return self

    def build(self) -> SmartGeocodingClient:
        session = requests.Session()
        user_agent = os.getenv(
            "NOMINATIM_USER_AGENT",
            "gps-tracker/1.0 (contact: you@example.com)",
        )
        from_email = os.getenv("NOMINATIM_FROM")
        accept_language = os.getenv("NOMINATIM_ACCEPT_LANGUAGE")
        session.headers.update(
            {
                "User-Agent": user_agent,
                "Accept": "application/json",
            }
        )
        if from_email:
            session.headers["From"] = from_email
        if accept_language:
            session.headers["Accept-Language"] = accept_language
        adapter = HTTPAdapter(
            pool_connections=self._pool_connections,
            pool_maxsize=self._pool_maxsize,
            pool_block=self._pool_block,
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return SmartGeocodingClient(
            session=session,
            cache=self._cache,
            rate_limiter=self._rate_limiter,
            retry_policy=self._retry_policy,
        )


class GeocodingClientDirector:
    @staticmethod
    def build_production_client() -> SmartGeocodingClient:
        return (
            SmartClientBuilder()
            .with_connection_pooling(pool_connections=20, pool_maxsize=20)
            .with_distributed_cache(ttl_seconds=3600)
            .with_rate_limiting(limit_per_second=1.0)
            .with_retry_policy(max_retries=2, base_delay=0.5, factor=2.0, jitter=0.2)
            .build()
        )


_client_instance: Optional[SmartGeocodingClient] = None


def get_geocoding_client() -> SmartGeocodingClient:
    global _client_instance
    if _client_instance is None:
        _client_instance = GeocodingClientDirector.build_production_client()
    return _client_instance


def clear_geocoding_cache() -> None:
    client = get_geocoding_client()
    client.clear_cache()
