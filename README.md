# PDF ExtractExt

API para extracción y procesamiento de PDFs construida con **FastAPI** y **Clean Architecture**.

## Integrantes del Grupo

| Apellido y Nombre | Legajo |
|-------------------|--------|
| Arccidiacono Fabricio | - |
| Lasagno Valentino | - |
| Martinez José | - |
| Sabio Antonio | - |
| Videla Lautaro | - |

*Carrera: Ingenieria en Sistemas - Desarrollo de Software*

## Descripcion

Extraer un texto de un PDF que es proporcionado por el usuario. Despues se hace un resumen gracias a un modelo de IA.

## Tecnologías

- Python 3.11+
- UV (gestor de paquetes)
- FastAPI
- MongoDB (base de datos no relacional)
- Ollama (modelo de IA)
- PyPDF2 / pypdf (extracción de texto de PDFs)

## Metodologías

- **TDD** (Test-Driven Development)
- GitHub Project Management
- **12-Factor App**

## Principios de Programacion

- **KISS** (Keep It Simple, Stupid)
- **DRY** (Don't Repeat Yourself)
- **YAGNI** (You Aren't Gonna Need It)
- **SOLID**

---

## Requerimientos

### Software Necesario

| Requerimiento | Version | Descripcion |
|---------------|---------|-------------|
| Python | 3.11+ | Lenguaje de programacion |
| UV | Ultima version | Gestor de paquetes Python |
| Docker | 20.10+ | Contenedorizacion (opcional pero recomendado) |
| Docker Compose | 2.0+ | Orquestacion de servicios |
| Git | 2.30+ | Control de versiones |

### Requerimientos de Hardware

- **Minimo:** 4GB RAM, 2 CPUs, 10GB espacio libre
- **Recomendado:** 8GB RAM, 4 CPUs, 20GB espacio libre

### Dependencias del Proyecto

Las dependencias estan definidas en `pyproject.toml`:

**Produccion:**
- FastAPI >= 0.115.0
- Uvicorn >= 0.32.0
- Pydantic >= 2.9.0
- PyMongo >= 4.9.0
- Motor >= 3.6.0
- PyPDF >= 5.0.0

**Desarrollo:**
- Pytest >= 9.0.2
- Pytest-asyncio >= 1.3.0
- HTTPX >= 0.28.1
- Pytest-cov >= 6.1.1

---

## Instalacion y Configuracion

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

---

## Ejecucion de la Aplicacion

### Opcion 1: Usando Docker Compose (Recomendado)

Esta opcion levanta automaticamente MongoDB y la aplicacion.

```bash
docker-compose up --build
```

**Servicios disponibles:**
- API: http://localhost:8000
- MongoDB: localhost:27017
- Swagger UI: http://localhost:8000/docs

```bash
# Ver logs
docker-compose logs -f app

# Detener servicios
docker-compose down
```

### Opcion 2: Instalacion Local (Desarrollo)

**Paso 1: Iniciar MongoDB**

Si no tienes MongoDB instalado, usa Docker:

```bash
docker run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=changeme mongo:7.0
```

**Paso 2: Ejecutar la Aplicacion**

```bash
# Con hot-reload (desarrollo)
uv run uvicorn src.interface_adapters.http.main:app --reload --host 0.0.0.0 --port 8000

# Sin reload (produccion)
uv run uvicorn src.interface_adapters.http.main:app --host 0.0.0.0 --port 8000
```

**La API estara disponible en:**
- API Base: http://localhost:8000
- Documentacion Swagger: http://localhost:8000/docs
- Documentacion ReDoc: http://localhost:8000/redoc

---

## Estructura del Proyecto

El proyecto sigue **Clean Architecture / Hexagonal Architecture** con las siguientes capas:

```
pdf-extractext/
├── application/          # Casos de uso y servicios de aplicación
│   ├── use_cases/        # Casos de uso específicos
│   ├── dtos/             # DTOs de la capa de aplicación
│   ├── mappers/          # Conversores entre capas
│   └── services/         # Servicios de aplicación
├── domain/               # Entidades, value objects, reglas de negocio
│   ├── entities/         # Entidades del dominio
│   ├── repositories/     # Interfaces de repositorios
│   └── value_objects/    # Value objects
├── infrastructure/       # Configuración, presentación, vistas
│   ├── config/           # Configuración de la app
│   ├── presenters/       # Presentadores
│   └── views/            # Vistas
├── interface_adapters/   # Adaptadores de entrada/salida
│   ├── database/         # Implementaciones de repositorios
│   ├── http/             # API REST con FastAPI
│   └── services_external/ # Adaptadores externos (Ollama, etc)
└── tests/                # Tests
    ├── unit/             # Tests unitarios
    └── integration/      # Tests de integración
```

## Principios de Clean Architecture Aplicados

- **Dependency Inversion**: Domain no importa nada de otras capas
- **Single Responsibility**: Cada clase hace una sola cosa
- **Interface Segregation**: Interfaces pequeñas y específicas
- **Inmutabilidad**: Entidades del dominio son inmutables
- **Testabilidad**: Facilidad de testear con mocks/stubs

---

## Instalación

### Usando UV (recomendado)

```bash
# Instalar dependencias
uv sync

# Instalar con dependencias de desarrollo
uv sync --dev
```

### Usando pip

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instalar dependencias (si existe requirements.txt)
pip install -r requirements.txt
```

## Configuración

Copiar el archivo de ejemplo y configurar:

```bash
cp .env.example .env
```

Editar `.env` con los valores correspondientes.

Variables importantes:
- `DEBUG`: Modo de desarrollo (true/false)
- `DATABASE_URL`: URL de conexión a MongoDB
- `DATABASE_NAME`: Nombre de la base de datos
- `UPLOAD_PATH`: Directorio para subir archivos PDF

---

## Ejecución

### Desarrollo

```bash
# Usando UV
uv run python main.py

# O con uvicorn directamente
uv run uvicorn interface_adapters.http.main:app --reload
```

### Producción

```bash
uv run uvicorn interface_adapters.http.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en `http://localhost:8000`
- Documentación Swagger: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

---

## Tests

### Ejecutar todos los tests

```bash
uv run pytest
```

### Tests unitarios

```bash
uv run pytest tests/unit/ -v
```

### Tests de integracion

```bash
uv run pytest tests/integration/ -v
```

### Con cobertura

```bash
uv run pytest --cov=src --cov-report=html
```

---

## API Endpoints

### Items (Ejemplo CRUD)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/items` | Listar todos los items |
| GET | `/api/v1/items/{id}` | Obtener item por ID |
| POST | `/api/v1/items` | Crear nuevo item |
| PUT | `/api/v1/items/{id}` | Actualizar item |
| DELETE | `/api/v1/items/{id}` | Eliminar item |

---

## Desarrollo

### Flujo de Trabajo

1. **Domain**: Definir entidades y reglas de negocio en `domain/`
2. **Application**: Implementar casos de uso en `application/use_cases/`
3. **Interface Adapters**: Crear adaptadores HTTP en `interface_adapters/http/`
4. **Infrastructure**: Configurar presentadores y vistas en `infrastructure/`

### Convenciones

- Nombres de clases: `PascalCase`
- Nombres de funciones: `snake_case`
- Interfaces abstractas: Sin sufijo, solo el nombre descriptivo
- Implementaciones: Nombre descriptivo del tipo de implementación
- Tests: `test_<nombre>.py` con clases `Test<Componente>`

### Importantes notas sobre imports

Siguiendo **Dependency Inversion**:

```python
# En domain/repositories/item_repository.py
from domain.entities.item import Item  # ✅ Domain solo importa Domain

# En interface_adapters/database/in_memory_item_repository.py
from domain.entities.item import Item              # ✅ Importa Domain
from domain.repositories.item_repository import ItemRepository  # ✅ Importa Domain

# En application/services/item_service.py
from domain.repositories.item_repository import ItemRepository  # ✅ Solo importa Domain
from domain.entities.item import Item              # ✅ Solo importa Domain
```

---

## Licencia

MIT
