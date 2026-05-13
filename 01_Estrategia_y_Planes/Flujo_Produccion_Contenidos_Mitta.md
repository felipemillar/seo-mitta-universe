# Flujo de Producción de Contenidos — Mitta

**Versión:** 1.0  
**Fecha:** Mayo 2026  
**Autor:** INMedios — Estrategia de Contenidos  
**Alcance:** Pilares Mitta Rent a Car y MittaGO (40 artículos)

---

## Resumen Ejecutivo

Este documento describe el flujo completo de producción de contenidos para los pilares editoriales de Mitta. El proceso está diseñado en 8 fases secuenciales que integran tres capas de trabajo: **producción editorial con optimización técnica** (SEO, AEO, GEO), **validación directa del cliente** mediante un portal interactivo de feedback, y **análisis neurocientífico** de los activos visuales a través de Neurons Predict. El entregable final de cada artículo es un **documento PDF** listo para publicación que combina contenido aprobado, visuales optimizados y estructura técnica validada.

---

## Visión General del Flujo

```
FASE 1 ─── Estrategia y Planificación
   │
FASE 2 ─── Redacción y Optimización Técnica (SEO / AEO / GEO)
   │
FASE 3 ─── Validación de Contenido por el Cliente
   │
   ├── (Iteración Editorial si corresponde)
   │
FASE 4 ─── Producción de Activos Visuales
   │
FASE 5 ─── Análisis Neurocientífico — Primera Pasada
   │
FASE 6 ─── Iteración Visual Basada en Neurociencia
   │
FASE 7 ─── Validación Visual por el Cliente
   │
   ├── (Iteración Visual si corresponde)
   │
FASE 8 ─── Ensamblaje Final y Entrega PDF
```

---

## Fase 1 — Estrategia y Planificación

**Objetivo:** Definir la arquitectura editorial completa antes de escribir una sola línea.

**Actividades:**

- Definición de los pilares de contenido. En el caso actual: **Mitta Rent a Car** (arriendo tradicional) y **MittaGO** (suscripción vehicular).
- Selección de 20 temas por pilar, priorizados por volumen de búsqueda, intención del usuario y relevancia comercial.
- Asignación de una keyword principal y keywords secundarias a cada artículo.
- Clasificación de cada tema por intención de búsqueda: informacional, transaccional o navegacional.
- Elaboración del calendario editorial con fechas de entrega por fase.

**Entregables de esta fase:**

- Documento de Propuesta de Contenidos por pilar (ya existente: `Propuesta_Contenidos_RentACar_2026` y `Propuesta_Contenidos_MittaGO_2026`).
- Matriz de keywords asignadas.

---

## Fase 2 — Redacción y Optimización Técnica

**Objetivo:** Producir el contenido editorial y blindarlo estructuralmente para SEO, AEO y GEO.

**Actividades:**

### 2.1 Redacción del artículo (versión v1)

- Redacción del cuerpo del artículo siguiendo la estructura de 7 bloques definida en la guía maestra (`Estructura_Optima_SEO_GEO_AEO.md`):
  1. **Frontmatter YAML** — Metadata del artículo (título, descripción, keyword, autor, fecha, schema type).
  2. **Schema.org @graph (JSON-LD)** — Esquema estructurado con Organization, WebSite, WebPage, Article y FAQPage.
  3. **BreadcrumbList** — Navegación jerárquica para Google.
  4. **Bloque AEO** — Respuesta directa en las primeras 50 palabras, optimizada para ser citada por motores generativos (ChatGPT, Gemini, Perplexity).
  5. **Cuerpo del artículo** — Contenido con jerarquía H2/H3, listas, tablas comparativas y datos específicos.
  6. **Sección FAQ** — Preguntas frecuentes alineadas con el schema FAQPage.
  7. **Call to Action (CTA)** — Cierre orientado a la conversión.

### 2.2 Homologación estructural automatizada

- Ejecución de scripts de Node.js (`homologar.js`) que procesan los 40 artículos para garantizar paridad técnica entre ambos pilares.
- Validación automática de: existencia de Frontmatter, presencia de JSON-LD, formato de bloques AEO, inyección de BreadcrumbList.

**Entregables de esta fase:**

- 40 archivos Markdown (v1) con estructura técnica completa.
- Reporte de homologación confirmando paridad estructural.

---

## Fase 3 — Validación de Contenido por el Cliente

**Objetivo:** Obtener feedback directo del cliente sobre tono, claridad, enfoque comercial y preferencias visuales antes de avanzar a producción gráfica.

**Actividades:**

### 3.1 Despliegue del Portal de Feedback

- Se entrega al cliente el archivo `Portal_Feedback_Mitta.html`, un portal interactivo standalone (no requiere servidor) con las siguientes características:
  - Vista segmentada por pilar (Rent a Car / MittaGO).
  - Tarjetas resumen por artículo con título y descripción.
  - Modal de feedback con 5 preguntas de selección múltiple adaptadas al contenido específico de cada artículo.

### 3.2 Estructura de la encuesta por artículo

Cada artículo presenta 5 preguntas personalizadas que incorporan dinámicamente el título, keyword y pilar del artículo:

| Pregunta | Dimensión evaluada | Qué buscamos saber |
|---|---|---|
| 1. Impacto Inicial | Enganche | ¿La introducción atrapa al lector objetivo? |
| 2. Tono y Personalidad | Identidad de marca | ¿El texto suena como Mitta quiere comunicar? |
| 3. Claridad del Mensaje | Comprensión | ¿Un usuario sin contexto entiende el contenido? |
| 4. Enfoque Comercial | Conversión | ¿El texto motiva la reserva o suscripción? |
| 5. Acompañamiento Visual | Dirección de arte | ¿Qué tipo de imagen espera el cliente para este tema? |

Además, cada artículo incluye un campo de texto libre para comentarios adicionales.

### 3.3 Iteración editorial

- Se procesan las respuestas del cliente.
- Los artículos que recibieron observaciones (alternativas B, C o D en cualquier pregunta) se iteran en una versión v2.
- Los artículos aprobados (alternativa A en todas las preguntas) pasan directamente a Fase 4.

**Entregables de esta fase:**

- Respuestas consolidadas del cliente.
- Artículos iterados (v2) con los ajustes incorporados.

---

## Fase 4 — Producción de Activos Visuales

**Objetivo:** Generar los activos visuales iniciales de cada artículo, informados por las preferencias del cliente obtenidas en la Fase 3.

**Actividades:**

### 4.1 Diseño de prompts visuales

- Se construyen prompts de generación de imagen para cada artículo, considerando:
  - El tema y contexto del artículo.
  - La respuesta del cliente a la Pregunta 5 (tipo de visual preferido: fotografía de personas, vehículos, infografías o estilo corporativo abstracto).
  - Las guías de estilo de la marca Mitta (paleta de colores, tipografía, tono visual).

### 4.2 Generación de assets

- Por cada artículo se generan como mínimo 2 activos:
  - **Hero Image** (1200×630px) — Imagen principal del artículo, estilo editorial/cinematográfico.
  - **Human Element** (800×800px) — Elemento contextual con personas interactuando con el servicio.
- Los prompts siguen la estructura documentada en `prompts_imagenes_mittago.md` y su equivalente para Rent a Car.

**Entregables de esta fase:**

- 80 activos visuales iniciales (2 por artículo × 40 artículos).
- Archivo de prompts utilizado para trazabilidad.

---

## Fase 5 — Análisis Neurocientífico — Primera Pasada

**Objetivo:** Evaluar objetivamente el impacto cognitivo y atencional de cada activo visual mediante Neurons Predict.

**Actividades:**

### 5.1 Carga y análisis en Neurons Predict

- Se suben los activos visuales a la plataforma Neurons Predict.
- La herramienta evalúa cada imagen y entrega:
  - **NIS (Neurons Impact Score):** Puntuación general de impacto (escala 0–100).
  - **Mapa de calor de atención (Attention Heatmap):** Zonas donde el ojo se detiene.
  - **Mapa de carga cognitiva (Cognitive Load):** Áreas de complejidad visual excesiva.
  - **Mapa de claridad (Clarity):** Qué tan fácil es procesar la información visual.
  - **Mapa de enfoque (Focus):** Dónde converge la mirada primero.

### 5.2 Generación del diagnóstico

- Neurons Predict genera un PDF diagnóstico por activo analizado.
- Se documenta el NIS de referencia (primera pasada) para cada artículo.

**Entregables de esta fase:**

- Reporte PDF de Neurons Predict por activo.
- Tabla comparativa de NIS por artículo (línea base).

---

## Fase 6 — Iteración Visual Basada en Neurociencia

**Objetivo:** Traducir las recomendaciones de Neurons Predict en intervenciones concretas de diseño y validar la mejora.

**Actividades:**

### 6.1 Traducción PDF-to-Prompt

- Se aplica el protocolo documentado de traducción: cada hallazgo del diagnóstico de Neurons se convierte en una instrucción de diseño accionable.
- Ejemplos de traducciones:

| Diagnóstico Neurons | Intervención de Diseño |
|---|---|
| Atención dispersa en la zona del CTA | Aumentar contraste del botón, agregar flecha direccional |
| Carga cognitiva alta en el centro | Simplificar elementos, reducir texto superpuesto |
| Claridad baja en el headline | Aumentar tamaño tipográfico, agregar fondo sólido detrás del texto |
| Foco atencional lejos del producto | Reposicionar el vehículo/servicio al punto focal |

### 6.2 Regeneración de activos

- Se regeneran o ajustan los activos visuales incorporando las intervenciones.
- Se produce la versión v2 de cada activo.

### 6.3 Segunda pasada en Neurons Predict

- Se vuelven a cargar los activos v2 en Neurons Predict.
- Se compara el NIS de la segunda pasada contra la línea base de la primera.
- Se documenta el delta de mejora (ej: NIS 62 → NIS 78 = +16 puntos).

**Criterio de aprobación:** Un activo se considera optimizado cuando alcanza un NIS igual o superior a 70, o cuando demuestra una mejora sostenida respecto a la primera pasada.

**Entregables de esta fase:**

- Activos visuales v2 optimizados.
- Tabla comparativa de NIS (primera pasada vs. segunda pasada).
- Documentación del protocolo PDF-to-Prompt aplicado.

---

## Fase 7 — Validación Visual por el Cliente

**Objetivo:** Obtener la aprobación del cliente sobre los activos visuales finales antes del ensamblaje del PDF.

**Actividades:**

### 7.1 Presentación de visuales

- Se presentan al cliente los activos optimizados (v2) junto con un resumen visual del análisis neurocientífico:
  - Imagen final propuesta.
  - Heatmap de atención simplificado (para que el cliente entienda dónde mira el usuario).
  - NIS obtenido y qué significa.

### 7.2 Feedback visual del cliente

- El cliente aprueba, solicita ajustes menores o rechaza el visual.
- Si se solicitan ajustes, se ejecuta una iteración adicional (v3) y se repasa por Neurons si el cambio es significativo.

**Entregables de esta fase:**

- Aprobación formal del cliente por cada activo visual.
- Activos finales confirmados.

---

## Fase 8 — Ensamblaje Final y Entrega PDF

**Objetivo:** Compilar el contenido aprobado y los visuales optimizados en el documento PDF final de cada artículo.

**Actividades:**

### 8.1 Composición del PDF

- Cada PDF incluye:
  - Hero image aprobada.
  - Título y subtítulo del artículo.
  - Cuerpo del contenido (texto aprobado en Fase 3).
  - Elementos visuales secundarios (human element, infografías si aplica).
  - Sección FAQ.
  - CTA de cierre.
  - Footer con datos de contacto y branding Mitta.

### 8.2 Revisión de calidad final

- Verificación de ortografía y formato.
- Validación de que todos los datos operativos (precios, políticas, procesos) son correctos.
- Confirmación de que la estructura técnica (metadata, schemas) está lista para la publicación web posterior.

### 8.3 Entrega

- Se entrega el paquete completo al cliente: 40 documentos PDF finales, organizados por pilar.

**Entregables de esta fase:**

- 40 PDFs finales (20 Rent a Car + 20 MittaGO).
- Carpeta de activos visuales en alta resolución.
- Documentación técnica de respaldo (schemas, keywords, NIS scores).

---

## Resumen de Fases, Responsables y Checkpoints

| Fase | Nombre | Responsable | Checkpoint de Salida |
|---|---|---|---|
| 1 | Estrategia y Planificación | INMedios | Propuesta aprobada por el cliente |
| 2 | Redacción y Optimización Técnica | INMedios | 40 artículos homologados (v1) |
| 3 | Validación de Contenido | Cliente | Feedback completado en portal |
| 4 | Producción Visual | INMedios | 80 activos generados (v1) |
| 5 | Análisis Neurocientífico (1ra pasada) | INMedios + Neurons | NIS baseline documentado |
| 6 | Iteración Visual + Neurociencia (2da pasada) | INMedios + Neurons | NIS mejorado, activos v2 listos |
| 7 | Validación Visual | Cliente | Aprobación visual formal |
| 8 | Ensamblaje y Entrega PDF | INMedios | 40 PDFs entregados |

---

## Herramientas del Flujo

| Herramienta | Uso en el flujo |
|---|---|
| Node.js Scripts | Homologación estructural automatizada (Fase 2) |
| Portal_Feedback_Mitta.html | Validación del cliente — contenido (Fase 3) |
| Generación IA de imágenes | Producción de Hero Images y Human Elements (Fase 4) |
| Neurons Predict | Análisis neuro-biométrico de activos visuales (Fases 5 y 6) |
| Protocolo PDF-to-Prompt | Traducción de diagnóstico Neurons a intervenciones de diseño (Fase 6) |

---

*Documento generado por INMedios — Estrategia de Contenidos Digitales*
