# PDF ExtractExt

API para extracción y procesamiento de PDFs construida con **FastAPI** y **Clean Architecture**.

## Integrantes del Grupo

| Apellido y Nombre | Legajo |
|-------------------|--------|
| Arccidiacono Fabricio | 10772 |
| Lasagno Valentino | 10845 |
| Martinez José | 10864 |
| Sabio Antonio | 10927 |
| Videla Lautaro | 10954 |

*Carrera: Ingeniería en Sistemas - Desarrollo de Software*

## Descripción

Extraer un texto de un PDF que es proporcionado por el usuario. Después se hace un resumen gracias a un modelo de IA.

## Tecnologías

- Python 3.11+
- UV (gestor de paquetes)
- FastAPI
- MongoDB (base de datos no relacional)
- Ollama (modelo de IA)
- PyPDF (extracción de texto de PDFs)

## Requerimientos

### Software Necesario

| Requerimiento | Versión | Descripción |
|---------------|---------|-------------|
| Python | 3.11+ | Lenguaje de programación |
| UV | Última versión | Gestor de paquetes Python |
| MongoDB | 7.0+ | Base de datos no relacional |
| Docker | 20.10+ | Contenedorización (opcional pero recomendado) |
| Docker Compose | 2.0+ | Orquestación de servicios |
| Git | 2.30+ | Control de versiones |

## Instalación y Ejecución

### Paso 1: Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd pdf-extractext
```

### Paso 2: Instalar UV (Gestor de Paquetes)

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Paso 3: Configurar Variables de Entorno

Copiar el archivo de ejemplo:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Editar el archivo `.env` con los valores correspondientes:

```env
APP_NAME="PDF ExtractExt"
VERSION="0.1.0"
DESCRIPTION="API para extraccion y procesamiento de PDFs"
DEBUG=true
HOST=0.0.0.0
PORT=8000
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_ROOT_USERNAME=admin
MONGODB_ROOT_PASSWORD=changeme
MONGODB_DATABASE_NAME=pdf_extractext
MONGODB_AUTH_SOURCE=admin
UPLOAD_PATH=./uploads
```

### Paso 4: Instalar Dependencias

```bash
uv sync --dev
```

## Ejecución de la Aplicación

### Opción 1: Usando Docker Compose (Recomendado)

Esta opción levanta automáticamente MongoDB y la aplicación.

```bash
docker-compose up --build
```

La API estará disponible en:
- API: http://localhost:8000
- MongoDB: localhost:27017
- Swagger UI: http://localhost:8000/docs

**Comandos útiles:**
```bash
# Ver logs
docker-compose logs -f app

# Detener servicios
docker-compose down
```

### Opción 2: Instalación Local (Desarrollo)

**Paso 1: Iniciar MongoDB**

Si no tienes MongoDB instalado, usa Docker:

```bash
docker run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=changeme mongo:7.0
```

**Paso 2: Ejecutar la Aplicación**

```bash
# Con hot-reload (desarrollo)
uv run uvicorn src.interface_adapters.http.main:app --reload --host 0.0.0.0 --port 8000

# Sin reload (producción)
uv run uvicorn src.interface_adapters.http.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en:
- API Base: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc

## Tests

```bash
# Ejecutar todos los tests
uv run pytest

# Tests unitarios
uv run pytest tests/unit/ -v

# Tests de integración
uv run pytest tests/integration/ -v

# Con cobertura
uv run pytest --cov=src --cov-report=html
```
