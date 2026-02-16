# GPS Tracker API

API de geolocalización y seguimiento GPS con **FastAPI**, validación con **Pydantic** y seguridad por **API Key**.

---

## Descripción

Servicio REST para geocoding (dirección ↔ coordenadas), reverse geocoding, rastreo de ubicaciones por IP y análisis de direcciones completas. Utiliza proveedores **gratuitos** (OpenStreetMap y ArcGIS).

---

## Características

- ✅ API REST con FastAPI
- ✅ Forward Geocoding (dirección → coordenadas)
- ✅ Reverse Geocoding (coordenadas → dirección)
- ✅ Rastreo por IP pública
- ✅ Análisis detallado de direcciones
- ✅ Proveedores gratuitos (OSM + ArcGIS)
- ✅ Validación de datos con Pydantic
- ✅ Seguridad con API Key
- ✅ Documentación automática con Swagger
- ✅ CORS habilitado
- ✅ Health check
- ✅ Dockerizado

---

## Estructura del proyecto

```
app/
├── main.py                          # Aplicación FastAPI
├── configs/
│   ├── __init__.py
│   └── config.py                    # Configuración
├── models/                          # Modelos Pydantic (modulares)
│   ├── __init__.py
│   ├── base.py                      # Modelos compartidos
│   ├── ip_location.py
│   ├── forward_geocoding.py
│   ├── reverse_geocoding.py
│   └── house_address.py
├── services/                        # Lógica de negocio (modulares)
│   ├── __init__.py
│   ├── ip_location_service.py
│   ├── forward_geocoding_service.py
│   ├── reverse_geocoding_service.py
│   └── house_address_service.py
├── routers/                         # Endpoints (modulares)
│   ├── __init__.py
│   ├── health_router.py
│   ├── ip_location_router.py
│   ├── forward_geocoding_router.py
│   ├── reverse_geocoding_router.py
│   └── house_address_router.py
├── security/
│   ├── api_key.py                   # Validación de API Key
│   ├── encript.py                   # Cifrado
│   ├── decript.py                   # Descifrado
│   └── gen_key.py                   # Generación de claves
└── tests/
    └── test.py
```

📖 **Ver documentación completa de la arquitectura**: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Instalación

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## Configuración

### 1. Copiar archivo de ejemplo

```bash
cp .env.example .env
```

### 2. Generar API Keys

```bash
python app/security/gen_key.py
```

### 3. Configurar variables de entorno en `.env`

```bash
API_KEYS=dev_xxx,prod_yyy,test_zzz
NOMINATIM_USER_AGENT=gps-tracker/1.0 (contact: tu-email@dominio.com)
NOMINATIM_FROM=tu-email@dominio.com
NOMINATIM_ACCEPT_LANGUAGE=es-ES,es;q=0.9
```

**Nota**: La API usa proveedores gratuitos (OSM y ArcGIS). OSM (Nominatim) requiere `NOMINATIM_USER_AGENT`. Si deseas usar Google Maps, añade `GOOGLE_API_KEY` en el `.env`.

---

## Ejecución

```bash
# Desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La aplicación estará disponible en: `http://localhost:8000`

---

## Documentación de la API

- **Swagger UI**: `http://localhost:8000/api/gps/docs`
- **ReDoc**: `http://localhost:8000/api/gps/redoc`
- **OpenAPI JSON**: `http://localhost:8000/api/gps/openapi.json`

---

## Endpoints

### 🏥 Health Check

```http
GET /api/health
GET /api/gps/health
```

### 📍 Rastreo por IP

```http
POST /api/gps/my-location
X-API-Key: your_api_key_here
Content-Type: application/json

{"ip": "8.8.8.8"}  # opcional, usa la IP del cliente si no se especifica
```

### 🌍 Forward Geocoding (Dirección → Coordenadas)

```http
POST /api/gps/forward-geocoding
X-API-Key: your_api_key_here
Content-Type: application/json

{"address": "Mountain View, CA"}
```

### 🔄 Reverse Geocoding (Coordenadas → Dirección)

```http
POST /api/gps/reverse-geocoding
X-API-Key: your_api_key_here
Content-Type: application/json

{"latitude": 45.15, "longitude": -75.14}
```

### 🏠 Detalles de Dirección

```http
POST /api/gps/house-address
X-API-Key: your_api_key_here
Content-Type: application/json

{"address": "453 Booth Street, Ottawa ON"}
```

Ver ejemplos completos en: [API_EXAMPLES.md](API_EXAMPLES.md)

---

## Docker

```bash
# Construir imagen
docker build -t gps-tracker:1.0 .

# Ejecutar contenedor
docker run -d -p 8000:8000 --name gps-tracker gps-tracker:1.0
```

---

## Seguridad

- Todos los endpoints POST están protegidos con **API Key** (encabezado `X-API-Key`)
- En desarrollo, si `API_KEYS` está vacío, los endpoints estarán abiertos
- En producción, asegúrate de establecer claves seguras

---

## Licencia

MIT
