"""
Configuración de la aplicación GPS Tracker
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = Path(__file__).parent.parent.parent / ".env"

try:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f"Variables de entorno cargadas desde: {env_path}")
    else:
        print(f"Archivo .env no encontrado en: {env_path}")
        print("   Usando variables de entorno del sistema")
except (OSError, IOError, RuntimeError) as e:
    print(f"Error al cargar variables de entorno: {e}")
    print("Continuando con valores por defecto...")

# Variables de configuración
API_KEYS = os.getenv("API_KEYS", "")

# Opcional: Google Geocoding API Key
# Si quieres usar Google Maps en lugar de OSM/ArcGIS, agrega:
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
