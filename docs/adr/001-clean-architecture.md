# ADR 001 — Clean Architecture + Hexagonal

**Estado:** Aceptado
**Fecha:** 2026-09-16

## Contexto

La aplicación creció con duplicación de lógica y capas ambiguas (DTOs
redundantes, mappers vacíos, `services_external` sin uso). Se necesita una
declaración explícita de la arquitectura para guiar decisiones futuras y
eliminar código muerto (YAGNI/KISS).

## Decisión

Arquitectura declarada: **Clean Architecture + Hexagonal**.

- **Dominio** (`shared/domain/`) es la única fuente de verdad para
  `PdfValidator`, `PyPdfTextExtractor` y las excepciones de dominio.
- **Puertos** (`DocumentRepository`, `TextExtractorPort`) se definen en la
  capa de aplicación y el dominio.
- **Adaptadores** (infraestructura y base de datos) implementan los puertos.
- La entidad `Document` **no se filtra al cliente**: el border DTO
  `DocumentResponse.from_entity()` es la traducción canónica hacia las
  respuestas HTTP.

## Consecuencias

- El código duplicado en `services/*` fue eliminado en favor de
  `shared/domain/`.
- No se agregan DTOs/mappers intermedios salvo que un caso de uso lo exija.
- Todo lo que no esté justificado por un puerto o caso de uso se considera
  dead code y se elimina.