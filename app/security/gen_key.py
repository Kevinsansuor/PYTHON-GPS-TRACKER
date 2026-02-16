"""
Generador de API Keys seguros para GPS Tracker
"""

import secrets
from datetime import datetime


def generate_api_key(prefix: str = "gps") -> str:
    """
    Genera una API Key segura.

    Args:
        prefix: Prefijo para la clave (ej: gps, test, prod)

    Returns:
        str: API Key en formato prefix_randomstring
    """
    random_part = secrets.token_urlsafe(32)
    return f"{prefix}_{random_part}"


def generate_multiple_api_keys(count: int = 1, prefix: str = "gps") -> list:
    """
    Genera múltiples API Keys.

    Args:
        count: Cantidad de claves a generar
        prefix: Prefijo para las claves

    Returns:
        list: Lista de API Keys generadas
    """
    return [generate_api_key(prefix) for _ in range(count)]


if __name__ == "__main__":
    print("=" * 60)
    print("GENERADOR DE API KEYS - GPS TRACKER")
    print("=" * 60)
    print(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Generar una clave para desarrollo
    DEV_KEY = generate_api_key("dev")
    print(f"Clave de DESARROLLO:\n   {DEV_KEY}\n")

    # Generar una clave para producción
    PROD_KEY = generate_api_key("prod")
    print(f"Clave de PRODUCCIÓN:\n   {PROD_KEY}\n")

    # Generar una clave de prueba
    TEST_KEY = generate_api_key("test")
    print(f"Clave de PRUEBA:\n   {TEST_KEY}\n")

    print("=" * 60)
    print("INSTRUCCIONES:")
    print("=" * 60)
    print("1. Copia estas claves")
    print("2. Actualiza el archivo .env con:")
    print("   API_KEYS=key1,key2,key3")
    print("3. Usa el header en las solicitudes:")
    print("   X-API-Key: <tu_clave>")
    print("=" * 60)
