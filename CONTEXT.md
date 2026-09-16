# Contexto del Dominio

## Vocabulario

| Término | Definición |
| --- | --- |
| **PDF** | Formato de documento portable (`%PDF-` magic number) que se procesa siempre en memoria, nunca en disco. |
| **Documento** | Entidad raíz del dominio: `id`, `content` (texto extraído) y `checksum` (hash SHA-256 del PDF). |
| **Checksum SHA-256** | Hash del contenido binario del PDF; identifica duplicados de forma inequívoca. |
| **Extracción** | Operación que convierte bytes de un PDF en texto plano (`str`), una página por línea. |
| **Validación** | Operación que verifica magic number y tamaño máximo antes de procesar; protege contra bytes arbitrarios y DoS por memoria. |
| **Persistencia** | Guardado/recuperación de documentos en MongoDB vía `DocumentRepository`. |
| **Puerto** | Abstracción/interfaz (`TextExtractorPort`, `DocumentRepository`) que el dominio expone y la infraestructura implementa. |
| **Adaptador** | Implementación concreta de un puerto (`PyPdfTextExtractor`, `InMemoryItemRepository`). |

## Ubicación del dominio compartido

- `shared/domain/` es la **única fuente de verdad** para `PdfValidator`, `PyPdfTextExtractor` y las excepciones de dominio.
- `src/` re-exporta desde `shared/domain/` para no romper imports existentes.
- `services/*` importan directamente desde `shared/domain/` (ya no duplican código).