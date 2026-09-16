# ADR 002 — Migración a Microservicios con Dominio Compartido

**Estado:** Aceptado
**Fecha:** 2026-09-16

## Contexto

El sistema se estructuró en servicios de extracción, validación y
persistencia. Al evolucionar, cada servicio duplicaba lógica de dominio
(validador, extractor, excepciones), generando divergencia y mantenimiento
costoso.

## Decisión

Extraer a **microservicios independientes** que comparten una única fuente
de verdad en `shared/domain/`.

- Cada servicio es **independiente** (no comparten runtime ni base de datos).
- La comunicación entre perímetros ocurre por **HTTP**.
- La duplicación anterior fue eliminada: los servicios importan directamente
  desde `shared/domain/`.

## Consecuencias

- Cambios de dominio se aplican una sola vez y se propagan a todos los
  servicios.
- Cada microservicio puede escalar, desplegarse y versionarse de forma
  independiente.
- Se requiere disciplina para no reintroducir duplicación en los servicios.