# PDF ExtractExt

API para extracción y procesamiento de PDFs construida con **FastAPI** y **Clean Architecture**.

## Descripción

Extraer un texto de un PDF que es proporcionado por el usuario. Después se hace un resumen gracias a un modelo de IA.

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

## Principios de Programación

- **KISS** (Keep It Simple, Stupid)
- **DRY** (Don't Repeat Yourself)
- **YAGNI** (You Aren't Gonna Need It)
- **SOLID**

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

### Tests de integración

```bash
uv run pytest tests/integration/ -v
```

### Con cobertura

```bash
uv run pytest --cov=. --cov-report=html
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
