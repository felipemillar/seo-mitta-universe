# Flujo de Producción de Contenidos — Mitta

**Versión:** 1.2  
**Fecha:** Mayo 2026  
**Autor:** INMedios — Estrategia de Contenidos  
**Alcance:** Pilares Mitta Rent a Car y MittaGO

---

## Resumen Ejecutivo

Este documento describe el flujo completo de producción de contenidos para los pilares editoriales de Mitta. El proceso está diseñado en 6 fases secuenciales que integran tres capas de trabajo: **producción editorial con optimización técnica** (SEO, AEO, GEO), **producción y análisis neurocientífico** de los activos visuales a través de la herramienta **Digital Predict**, y **validación directa del cliente** del contenido y los visuales. El entregable final de cada artículo es un **documento PDF** listo para publicación.

---

## Visión General del Flujo

```text
FASE 1 ─── Estrategia y Planificación
   │
FASE 2 ─── Redacción y Optimización Técnica (SEO / AEO / GEO)
   │
FASE 3 ─── Producción de Activos Visuales
   │
FASE 4 ─── Análisis Neurocientífico (1ra pasada) e Iteración Visual
   │
FASE 5 ─── Validación de Contenido y Visual por el Cliente
   │        ├── Feedback del cliente
   │        └── Última Iteración de Ajustes (Redacción y Visuales)
   │
FASE 6 ─── Ensamblaje Final y Entrega en Documento PDF
```

---

## Fase 1 — Estrategia y Planificación

**Objetivo:** Definir la arquitectura editorial completa antes de escribir una sola línea.

**Actividades:**

- Definición de los pilares de contenido. En el caso actual: **Mitta Rent a Car** (arriendo tradicional) y **MittaGO** (suscripción vehicular).
- Selección de temas por pilar, priorizados por volumen de búsqueda, intención del usuario y relevancia comercial.
- Asignación de una keyword principal y keywords secundarias a cada artículo.
- Clasificación de cada tema por intención de búsqueda: informacional, transaccional o navegacional.
- Elaboración del calendario editorial con fechas de entrega por fase.

**Entregables de esta fase:**

- Documento de Propuesta de Contenidos por pilar.
- Matriz de keywords asignadas.

---

## Fase 2 — Redacción y Optimización Técnica

**Objetivo:** Producir el contenido editorial y blindarlo estructuralmente para SEO, AEO y GEO.

**Actividades:**

### 2.1 Redacción del artículo (versión v1)

- Redacción del cuerpo del artículo siguiendo la estructura de 7 bloques definida en la guía maestra (`Estructura_Optima_SEO_GEO_AEO.md`):
  1. **Frontmatter YAML** — Metadata del artículo.
  2. **Schema.org @graph (JSON-LD)** — Esquema estructurado.
  3. **BreadcrumbList** — Navegación jerárquica.
  4. **Bloque AEO** — Respuesta directa en las primeras 50 palabras.
  5. **Cuerpo del artículo** — Contenido con jerarquía H2/H3, listas y tablas.
  6. **Sección FAQ** — Preguntas frecuentes alineadas.
  7. **Call to Action (CTA)** — Cierre orientado a la conversión.

### 2.2 Homologación estructural automatizada

- Ejecución de scripts automatizados (`homologar.js`) que procesan los artículos para garantizar paridad técnica entre ambos pilares.

**Entregables de esta fase:**

- Archivos Markdown (v1) con estructura técnica completa.
- Reporte de homologación confirmando paridad estructural.

---

## Fase 3 — Producción de Activos Visuales

**Objetivo:** Generar los activos visuales iniciales de cada artículo.

**Actividades:**

### 3.1 Diseño de prompts visuales

- Se construyen prompts de generación de imagen para cada artículo, considerando el tema, contexto y guías de estilo de la marca Mitta.

### 3.2 Generación de assets

- Por cada artículo se generan como mínimo 2 activos:
  - **Hero Image** (1200×630px) — Imagen principal.
  - **Human Element** (800×800px) — Elemento contextual con personas.

**Entregables de esta fase:**

- Activos visuales iniciales para cada artículo.

---

## Fase 4 — Análisis Neurocientífico e Iteración Visual

**Objetivo:** Evaluar objetivamente el impacto cognitivo y atencional de cada activo visual mediante **Digital Predict**, y aplicar intervenciones de diseño.

**Actividades:**

### 4.1 Carga y análisis en Digital Predict (Primera Pasada)

- Carga de los activos a Digital Predict para obtener métricas clave: **Puntuación de Impacto**, **Heatmaps de Atención**, **Carga Cognitiva** y **Claridad**.
- Generación de diagnóstico y registro del puntaje base (baseline).

### 4.2 Iteración Visual (Traducción de Diagnóstico a Diseño)

- Cada hallazgo del diagnóstico se convierte en una instrucción de diseño accionable (ej. "Aumentar contraste", "Simplificar elementos").
- Se ajustan los activos visuales (v2) y se someten a una **segunda pasada** en Digital Predict.
- Se documenta el delta de mejora, buscando un puntaje de impacto igual o superior al objetivo (70+).

**Entregables de esta fase:**

- Reportes PDF de Digital Predict.
- Activos visuales v2 optimizados (listos para validación).

---

## Fase 5 — Validación de Contenido y Visual por el Cliente

**Objetivo:** Obtener feedback unificado del cliente sobre el contenido editorial y los activos visuales, y realizar la iteración final de ambos componentes.

**Actividades:**

### 5.1 Despliegue del Portal de Feedback y Visuales

- Se entrega al cliente el `Portal_Feedback_Mitta.html` para la validación de texto (tono, claridad, comercial).
- Se presentan los visuales optimizados (v2) acompañados del reporte simplificado de Digital Predict.

### 5.2 Recolección de Feedback

- El cliente responde la encuesta de 5 preguntas por artículo para el texto.
- El cliente aprueba o solicita ajustes sobre los visuales propuestos.

### 5.3 Última Iteración de Ajustes

- **Ajuste de Redacción y Optimización:** Se incorpora el feedback editorial en una versión final del contenido.
- **Ajuste de Activos Visuales:** Se aplican los retoques solicitados a las imágenes (versión final).

**Entregables de esta fase:**

- Feedback documentado del cliente.
- Artículos y activos visuales finales y aprobados.

---

## Fase 6 — Ensamblaje Final y Entrega PDF

**Objetivo:** Compilar el contenido aprobado y los visuales optimizados en el documento PDF final de cada artículo.

**Actividades:**

### 6.1 Composición del PDF

- Cada PDF integra la *Hero Image*, cuerpo de texto, *Human Element*, esquemas técnicos, FAQ y CTA.

### 6.2 Revisión y Entrega

- Revisión de calidad (ortografía, exactitud de datos).
- Entrega de los documentos PDF.

**Entregables de esta fase:**

- PDFs finales listos para publicación.
- Carpeta de activos visuales en alta resolución.
- Documentación técnica de respaldo.

---

## Resumen de Fases, Responsables y Checkpoints

| Fase | Nombre | Responsable | Checkpoint de Salida |
|---|---|---|---|
| 1 | Estrategia y Planificación | INMedios | Propuesta de contenidos y keywords |
| 2 | Redacción y Optimización Técnica | INMedios | Artículos homologados (v1) |
| 3 | Producción de Activos Visuales | INMedios | Activos visuales iniciales generados |
| 4 | Análisis Neurocientífico e Iteración | INMedios + Digital Predict | Activos v2 optimizados con puntaje de impacto validado |
| 5 | Validación de Cliente + Última Iteración | Cliente / INMedios | Contenido y visuales 100% aprobados |
| 6 | Ensamblaje Final y Entrega PDF | INMedios | PDFs finales entregados |

---

## Herramientas del Flujo

| Herramienta | Uso en el flujo |
|---|---|
| Node.js Scripts | Homologación estructural automatizada (Fase 2) |
| Portal_Feedback_Mitta.html | Validación del cliente — contenido (Fase 5) |
| Generación IA de imágenes | Producción de Hero Images y Human Elements (Fase 3) |
| Digital Predict | Análisis neuro-biométrico de activos visuales (Fase 4) |
| Protocolo de Intervención | Traducción de diagnóstico Digital Predict a diseño (Fase 4) |

---

*Documento generado por INMedios — Estrategia de Contenidos Digitales*
