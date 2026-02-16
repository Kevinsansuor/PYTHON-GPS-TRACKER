import os
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader


API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


# claves desde entorno (separadas por coma). ej: API_KEYS="key1,key2,key3"
_ALLOWED_KEYS = {k.strip() for k in os.getenv(
    "API_KEYS", "").split(",") if k.strip()}


def require_api_key(x_api_key: str | None = Depends(API_KEY_HEADER)):
    # condicion para modo dev
    if not _ALLOWED_KEYS:
        return True
    if not x_api_key or x_api_key not in _ALLOWED_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing API key"
        )
    return True
