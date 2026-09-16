# ADR 003 — Infraestructura por-servicio, sin paquete compartido de infraestructura

**Estado:** Aceptado
**Fecha:** 2026-09-16

## Contexto

El análisis de Clean Code (DRY) señaló duplicación de `MongoDBConnection`
(singleton + env + ping) y de la lógica de retries HTTP entre `src/` y los
microservicios. Se evaluó extraer ambos a un paquete `shared/` para tener una
única fuente de verdad.

## Decisión

No se crea un paquete compartido de infraestructura ni de capa de aplicación.
`shared/` únicamente aloja el **dominio puro** decidido en el ADR 001 y 002.
La conexión a Mongo y la orquestación HTTP con retries permanecen **dentro de
cada microservicio**, porque:

- Cada servicio es un **deployable independiente** (ADR 002): no comparten
  runtime, config ni ciclo de vida. Sus clases de conexión difieren en el
  contrato de configuración (`Settings` del monolith vs `MongoSettings` del
  servicio de persistencia).
- Consolidar infraestructura en `shared/` acoplaría los despliegues entre sí
  y mezclaría configuraciones por-servicio, violando la independencia.
- La lógica de retries (≈10 líneas) es orquestación de la capa de aplicación,
  específica de cada servicio, no regla de negocio.

## Alternativas consideradas

1. **Paquete `shared/infrastructure`**: descartada — acopla deployables y
   rompe la frontera de dominio puro del ADR 001.
2. **Unificar configuración en un solo `Settings`**: descartada — los env vars
   y defaults por servicio difieren (hosts internos de red, puertos).

## Consecuencias

- La duplicación de infraestructura entre servicios es **deliberadamente
  aceptada** y no debe re-litigarse en revisiones futuras.
- Los cambios de **dominio** (validator, extractor, excepciones, constantes,
  validación de filename) se siguen aplicando una sola vez en `shared/domain/`.
- Cualquier nueva regla de negocio compartida debe vivir en `shared/domain/`;
  cualquier pieza de infraestructura debe quedar en el servicio que la usa.