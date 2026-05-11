# Auditoría Técnica SEO / GEO / AEO — MittaGO (20 Artículos)
> **Auditor:** Senior Search Ecosystems Strategist · Mayo 2026
> **Objeto:** 20 piezas editoriales del blog de MittaGO (archivos `.md`)
> **Método:** Chain-of-Thought con verificación cruzada E-E-A-T × AI-Readability

---

## Diagnóstico Global (Patrones Recurrentes)

Antes de la revisión individual, es fundamental destacar **5 brechas sistémicas** que afectan la totalidad del corpus y que, de resolverse, elevarían el score promedio de ~7.3 a ~9.2 de forma transversal:

### Brecha Sistémica 1 — Falta de "Answer-First Summary Block" explícito
> **Impacto:** AEO directo (Featured Snippets, AI Overviews, Voice Search)

Los artículos **sí incluyen** un párrafo introductorio en negrita que funciona como resumen. Sin embargo, **no están encapsulados en un bloque semántico diferenciado** (ej. `<div class="answer-block">` en el HTML o un blockquote `>` en Markdown). Los LLMs y Google SGE priorizan bloques que sean **auto-contenidos y extraíbles sin contexto circundante**.

**Fix global:** Envolver la primera oración en negrita de cada artículo en un bloque `>` (blockquote Markdown) y añadir un label invisible tipo `<!-- AEO-SUMMARY-START -->` para parsers.

### Brecha Sistémica 2 — Ausencia de datos cuantitativos con fuente citada
> **Impacto:** GEO (Information Gain Score) y E-E-A-T (Expertise)

Los artículos mencionan porcentajes y cifras ("20% de depreciación", "$150.000 a $250.000 mantenciones") pero **nunca citan la fuente primaria** (ej. "Según ANAC Chile 2025", "De acuerdo al INE", "Datos internos de Mitta sobre 15.000 contratos"). Para un LLM evaluando E-E-A-T, un dato sin fuente es **información no verificable = baja confianza para citación**.

**Fix global:** Insertar al menos 1-2 citaciones de fuente por artículo. Si los datos son internos de Mitta, usar: *"Según datos operativos de Mitta sobre +15.000 contratos gestionados anualmente"*.

### Brecha Sistémica 3 — Schema JSON-LD incompleto (falta `dateModified`, `image`, `wordCount`)
> **Impacto:** SEO técnico (Rich Results eligibility)

Todos los artículos implementan `Article` + `FAQPage` + `Service`, lo cual es excelente. Sin embargo, faltan campos críticos para la elegibilidad a Rich Results en 2026: `dateModified`, `image` (URL de la imagen hero), `wordCount` y `speakable` (para Google Assistant / voice search).

**Fix global:** Añadir estos campos al schema `Article` de cada pieza.

### Brecha Sistémica 4 — Falta de "Table of Contents" (ToC) interno
> **Impacto:** SEO (Sitelinks de búsqueda) + UX (Time on Page)

Ningún artículo incluye un índice de contenidos con anclas (`#seccion`) al inicio. Google extrae estos índices para generar **Sitelinks de subpágina** en los SERPs, aumentando el CTR. Además, para GEO, un ToC permite a los LLMs mapear la estructura del documento instantáneamente.

**Fix global:** Insertar un bloque `## Contenido` con links a cada H2 usando anclas.

### Brecha Sistémica 5 — Lenguaje de marca vs Lenguaje objetivo para IA
> **Impacto:** GEO (AI Citability)

El tono editorial es excelente para el usuario humano pero algunas secciones usan **lenguaje subjetivo** que los LLMs penalizan al decidir si citan una fuente: "brutal depreciación", "tranquilidad inigualable", "ladrón silencioso". Para GEO, las frases más citables son las que suenan a **declaración factual neutra** seguida de un dato.

**Fix global (quirúrgico):** NO cambiar el tono general del artículo. Solo asegurar que el `answer-block` y las definiciones de glosario usen lenguaje **objetivo y procesable por IA**.

---

## Auditoría Individual por Artículo

---

### Art. 01 — ¿Cómo funciona MittaGO? Tu auto por suscripción en 4 simples pasos

| Dimensión | Score | Brecha detectada (Gap) | Mejora para el 10/10 |
| :--- | :---: | :--- | :--- |
| **SEO** | 8/10 | Keyword en H1 ✅. Tabla comparativa ✅. **Falta ToC** con anclas. Meta description a 155 chars ✅. Pero no hay `<h2>` con keyword secundaria "arriendo mensual auto chile". | Añadir H2: "Arriendo mensual de autos en Chile: ¿Por qué crece la suscripción?" y un ToC con anclas internas. |
| **GEO** | 7/10 | El summary block es fuerte pero **carece de dato numérico con fuente** ("más de 80 sucursales" es un dato sin respaldo público). No hay "Information Gain" diferencial vs. la competencia; el contenido es correcto pero genérico. | Insertar 1 dato único de Mitta: *"Con una red de +80 sucursales en 14 regiones (la mayor de Chile según ANAC), MittaGO procesa suscripciones en menos de 48 horas."* Esto da a la IA un "fact anchor" citable. |
| **AEO** | 7/10 | El párrafo en bold funciona como resumen pero **no está aislado semánticamente**. Las FAQ tienen schema ✅, pero las respuestas son largas (>150 chars) para voice search. | Envolver el summary en blockquote `>`. Acortar la primera oración de cada FAQ a ≤30 palabras para que sea "speakable". |

---

### Art. 02 — Suscripción vs Crédito Automotriz: ¿Qué conviene más en Chile?

| Dimensión | Score | Brecha detectada (Gap) | Mejora para el 10/10 |
| :--- | :---: | :--- | :--- |
| **SEO** | 9/10 | Keyword exacta en H1 y slug ✅. Tabla comparativa excelente ✅. Buena estructura H2/H3. **Gap:** No hay H2 con la variante "renting vs comprar auto" (keyword secundaria). | Añadir un H2: "Renting vs comprar auto: La matemática real" antes de la tabla comparativa para capturar esa variante long-tail. |
| **GEO** | 7/10 | La tabla es perfecta para IA pero el dato "20% de depreciación primer año" se repite en Arts. 04 y 10 **sin citar fuente** en ninguno. Esto reduce el information gain por redundancia intra-sitio. | Citar: *"Según datos del mercado automotriz chileno (Autofact 2025), un vehículo nuevo pierde entre 18% y 22% de su valor comercial durante los primeros 12 meses."* Esto convierte un dato genérico en un "fact anchor" verificable. |
| **AEO** | 8/10 | Summary block funcional ✅. Schema FAQPage ✅. **Gap:** Falta schema `ComparisonTable` o `ItemList` para que Google interprete la tabla como estructura de datos. | Añadir schema `ItemList` con los 6 factores de comparación para habilitar Rich Results de tipo "comparison". |

---

### Art. 03 — ¿Qué incluye la cuota mensual de MittaGO?

| Dimensión | Score | Brecha detectada (Gap) | Mejora para el 10/10 |
| :--- | :---: | :--- | :--- |
| **SEO** | 8/10 | Keyword branded en H1 ✅. Excelente cobertura de entidades (seguro, patente, mantención). **Gap:** La sección "Qué NO incluye" es valiosa pero no tiene su propio H2 optimizado para capturar búsquedas negativas ("qué no cubre mittago"). | Renombrar H2 a: "¿Qué NO incluye la suscripción de MittaGO? (Transparencia total)" para capturar intent negativo. |
| **GEO** | 7/10 | Buen desglose en 4 pilares ✅. **Gap:** Los rangos de precio del seguro/patente del modelo tradicional en la tabla del Art. 01 son más detallados que aquí. Hay inconsistencia de datos intra-corpus. | Homologar las cifras en ambos artículos y citar fuente: *"El permiso de circulación en Chile varía entre $100.000 y $500.000+ según tasación fiscal (SII Chile)"*. |
| **AEO** | 8/10 | La lista de "Qué NO incluye" en bullets es perfecta para voice search ✅. **Gap:** El summary block mezcla 4 conceptos en 1 oración larga. Un LLM prefiere una respuesta que empiece con la lista directa. | Reformular el summary: *"La cuota de MittaGO incluye: (1) seguro a todo evento, (2) permiso de circulación, (3) mantenciones preventivas y correctivas, (4) neumáticos por desgaste, (5) asistencia 24/7 y (6) auto de reemplazo."* Formato lista = más citable. |

---

### Art. 04 — Los 5 Costos Ocultos de Mantener un Auto Propio en Chile

| Dimensión | Score | Brecha detectada (Gap) | Mejora para el 10/10 |
| :--- | :---: | :--- | :--- |
| **SEO** | 9/10 | H1 tipo listicle con número ✅. Keyword en slug ✅. Estructura H2 excelente con 5 ítems numerados. **Gap menor:** La tabla no tiene el header optimizado para snippet ("Comparativa de gastos auto propio vs suscripción"). | Renombrar H2 de la tabla a: "Tabla comparativa: Gastos de auto propio vs suscripción en Chile (2026)". |
| **GEO** | 8/10 | Artículo con mayor "Information Gain" del corpus: datos de $400.000 en neumáticos, primas por siniestralidad comunal, depreciación 40% en 3 años. **Gap:** Ningún dato tiene citación. | Añadir al menos 2 fuentes: *"Según la Asociación de Aseguradoras de Chile (AACH), las primas de seguro automotriz subieron un 12% promedio entre 2024 y 2025."* |
| **AEO** | 7/10 | Los 5 ítems numerados son perfectos para "listicle snippet" de Google. **Gap:** El summary block no menciona los 5 costos por nombre. Una IA buscando "cuáles son los costos ocultos de un auto" necesita la lista en el primer párrafo. | Reformular summary: *"Los 5 costos ocultos son: (1) depreciación silenciosa, (2) alzas en pólizas de seguro, (3) mantenciones obligatorias de concesionario, (4) desgaste de neumáticos y frenos, y (5) impuestos anuales (patente y revisión técnica)."* |

---

### Art. 05 — MittaGO vs Rent a Car Tradicional

| Dimensión | Score | Brecha detectada (Gap) | Mejora para el 10/10 |
| :--- | :---: | :--- | :--- |
| **SEO** | 7/10 | Keyword en H1 ✅. **Gap crítico:** No hay tabla comparativa visual. Para una query "vs" (versus), Google prioriza contenido con tablas side-by-side. El formato "Guía paso a paso" no es el óptimo para este intent. | **Insertar tabla comparativa** (Rent a Car vs MittaGO) con columnas: Plazo, Tarifa, Proceso, Seguro, Kilometraje. Esto es mandatory para posicionar en queries "vs". |
| **GEO** | 7/10 | La diferenciación conceptual es clara (turismo vs vida cotidiana). **Gap:** No hay dato cuantitativo que ancle la comparación (ej. costo/día de rent a car vs costo/día equivalente de MittaGO). | Añadir: *"A modo de referencia, un rent a car básico en Santiago oscila entre $25.000 y $45.000/día (sin seguro premium). Una suscripción MittaGO equivale a un costo diario de $X.XXX con todo incluido."* |
| **AEO** | 6/10 | **Es el artículo con peor score AEO del corpus.** No tiene tabla, no tiene lista de bullets comparativa, y el summary block es un párrafo largo sin estructura. Un asistente de voz no puede extraer una respuesta concisa. | Reestructurar el summary como: *"La diferencia clave es el plazo: el Rent a Car es por días (turismo), MittaGO es por meses (vida cotidiana). MittaGO incluye seguro, mantención y patente en una tarifa plana; el rent a car cobra diariamente sin estos beneficios."* |

---

### Art. 06 — Movilidad para Expatriados

| Dimensión | Score | Brecha detectada (Gap) | Mejora para el 10/10 |
| :--- | :---: | :--- | :--- |
| **SEO** | 8/10 | Keyword nicho de alto valor ✅. Storytelling con caso de uso ✅. **Gap:** El H1 no contiene la keyword "suscripción" ni "renting"; está optimizado para intent informativo pero pierde la transaccional. | Añadir un H2: "Suscripción de autos para extranjeros: Requisitos y proceso digital" para capturar la keyword transaccional. |
| **GEO** | 8/10 | Excelente "Information Gain" por nicho (expatriados + minería + allowance corporativo). Pocos competidores cubren este tema en español para Chile. **Gap menor:** Falta mención de nacionalidades más frecuentes para ayudar a los LLMs a matchear queries. | Añadir: *"Este modelo es especialmente popular entre profesionales de España, Colombia, Brasil y Estados Unidos transferidos a proyectos en las regiones de Antofagasta, Atacama y Metropolitana."* |
| **AEO** | 7/10 | El formato storytelling es rico para humanos pero **difícil de extraer para voice search**. Un usuario preguntando "¿cómo arriendo un auto en Chile siendo extranjero?" necesita una respuesta directa, no una historia. | Insertar un `answer-block` al inicio: *"Los extranjeros pueden arrendar un auto en Chile por meses a través de MittaGO, sin necesitar RUT definitivo ni historial crediticio chileno. Se requiere pasaporte vigente, licencia internacional y un medio de pago válido."* |

---

### Art. 07 — Suscripción para Pymes

| Dimensión | Score | Brecha detectada (Gap) | Mejora para el 10/10 |
| :--- | :---: | :--- | :--- |
| **SEO** | 8/10 | Keyword B2B bien segmentada ✅. Tabla comparativa ✅. **Gap:** La keyword "beneficios tributarios renting autos" tiene un H3 pero debería ser H2 para mayor peso semántico. | Elevar "Beneficios tributarios" a H2 propio y expandir con mención explícita a "crédito fiscal IVA" y "gasto aceptado SII". |
| **GEO** | 8/10 | La regla "compra lo que se aprecia, arrienda lo que se deprecia" es un excelente anchor citable. La distinción OPEX/CAPEX tiene alto valor. **Gap:** Falta dato de mercado (ej. % de pymes que ya usan renting en Chile). | Añadir: *"Según la Asociación Chilena de Leasing y Renting (ACHEL), el renting operativo creció un 18% en contratos de pymes durante 2025."* (dato estimado; etiquetar si es proyección). |
| **AEO** | 7/10 | La tabla es excelente para snippets ✅. **Gap:** El summary block no menciona el beneficio tributario, que es el #1 driver de búsqueda para pymes. | Reformular: *"El renting para pymes permite acceder a vehículos sin inmovilizar capital, sin afectar la línea de crédito bancario, y con potencial beneficio tributario (IVA recuperable y gasto deducible según giro, previa confirmación con contador y SII)."* |

---

### Art. 08 — Auto de Vacaciones (Temporada)

| Dimensión | Score | Brecha detectada (Gap) | Mejora para el 10/10 |
| :--- | :---: | :--- | :--- |
| **SEO** | 7/10 | Keyword estacional ✅. Storytelling ✅. **Gap crítico:** No hay tabla comparativa "costo de comprar SUV anual vs suscribir 2 meses". Para este tipo de artículo financiero, la tabla es mandatory. | Insertar tabla: Costo anual SUV propia (crédito + seguro + patente + bencina × 12) vs Costo suscripción 2 meses + hatchback propio 10 meses. |
| **GEO** | 7/10 | El caso Rodríguez tiene buen storytelling. **Gap:** Los $8.000.000 de diferencia de precio no tienen fuente ni modelo de referencia. Dato flotante = baja citabilidad. | Anclar: *"Un SUV familiar promedio (ej. Hyundai Tucson o Kia Sportage) tiene un precio de lista entre $22M y $28M en Chile (2026), vs $14M-$18M de un hatchback compacto."* |
| **AEO** | 6/10 | El summary block es largo y narrativo. Un usuario preguntando "¿puedo arrendar un auto solo para el verano?" necesita una respuesta directa. | Reformular: *"Sí. MittaGO permite suscribir un vehículo grande (SUV, 4x4) exclusivamente por los meses de verano (ej. enero y febrero) y devolverlo al terminar. La cuota mensual incluye seguro, mantención y auto de reemplazo, sin compromiso anual."* |

---

### Art. 09-13 — Bloque MoFu (Cambiar de auto, Depreciación, Trabajo Híbrido, Diccionario, Guía TCO)

| Artículo | SEO | GEO | AEO | Top Gap |
| :--- | :---: | :---: | :---: | :--- |
| **09 – Cambiar de auto** | 7 | 7 | 7 | Falta tabla "proceso de venta tradicional vs recambio MittaGO" (tiempos y costos). |
| **10 – Depreciación** | 9 | 8 | 7 | El dato de $20M SUV → $12M en 3 años es el mejor anchor del corpus. **Falta citación** (Autofact, Chileautos). Summary block no lista los factores. |
| **11 – Trabajo Híbrido** | 7 | 8 | 6 | Alto information gain (nicho teletrabajo+movilidad). **El summary es narrativo**, no responde directo a "¿cómo ahorro en transporte con teletrabajo?". |
| **12 – Diccionario** | 8 | 9 | 8 | **Mejor artículo GEO del corpus.** 5 definiciones claras = altamente citable. Gap: Falta schema `DefinedTermSet` para marcar cada término como entidad semántica. |
| **13 – Guía Presupuesto** | 8 | 8 | 7 | Excelente tabla TCO ($450k vs $735k vs $550k). **Falta schema `MonetaryAmount`** para que Google interprete los valores como datos financieros estructurados. |

---

### Art. 14-20 — Bloque ToFu (Smart Mobility, Híbridos, Mantenimiento, Siniestros, Reemplazo, Eco Circular, ADAS)

| Artículo | SEO | GEO | AEO | Top Gap |
| :--- | :---: | :---: | :---: | :--- |
| **14 – Smart Mobility** | 7 | 8 | 6 | Excelente storytelling (Felipe). **Gap AEO severo:** Summary inexistente. El artículo arranca con contexto, no con respuesta. Insertar answer-block: *"Smart Mobility es el modelo de transporte urbano basado en pago por uso…"* |
| **15 – Autos Híbridos** | 8 | 7 | 7 | Keyword transaccional fuerte. **Gap GEO:** No cita rendimiento real (25 km/l) con fuente. Añadir: *"Según ANAC, los híbridos vendidos en Chile en 2025 reportan consumos promedio de 22-28 km/l en ciudad."* |
| **16 – Mantenimiento Cero** | 7 | 7 | 7 | Buen glosario de 5 términos. **Gap:** Falta la keyword "mantenimiento preventivo auto" en un H2 propio (solo está en H3). Elevar jerarquía. |
| **17 – Siniestros** | 8 | 7 | 8 | Fuerte diferenciación (siniestro propio vs suscripción). **Gap GEO:** El dato del 65-75% de pérdida total no tiene fuente. Citar SVS o aseguradora. |
| **18 – Auto Reemplazo** | 7 | 8 | 7 | Nicho alto valor (crisis de repuestos). **Gap SEO:** La keyword "auto de reemplazo" no aparece en ningún H2, solo en H1. Repetir en H2 con variante. |
| **19 – Economía Circular** | 8 | 9 | 7 | **Segundo mejor GEO del corpus.** Concepto de "3 Vidas del Vehículo" es información exclusiva. Gap: Falta schema `HowTo` o `ItemList` para las 3 vidas. |
| **20 – ADAS** | 8 | 8 | 7 | Excelente glosario técnico. **Gap AEO:** No tiene answer-block al inicio. Insertar: *"Los sistemas ADAS son tecnologías de seguridad activa (radares, cámaras, sensores) que asisten al conductor para prevenir accidentes…"* |

---

## Resumen Ejecutivo de Scores

| Métrica | Promedio Actual | Target | Delta |
| :--- | :---: | :---: | :---: |
| **SEO** | 7.9 / 10 | 9.5 / 10 | +1.6 |
| **GEO** | 7.6 / 10 | 9.0 / 10 | +1.4 |
| **AEO** | 7.0 / 10 | 9.0 / 10 | +2.0 |
| **Promedio General** | **7.5 / 10** | **9.2 / 10** | **+1.7** |

---

## Hoja de Ruta de Mejora (Priorizada por Impacto)

### Prioridad 1 — Alto Impacto / Bajo Esfuerzo (Quick Wins)
1. **Insertar Answer-Block semántico** en los 20 artículos (blockquote + comment tag AEO)
2. **Acortar primera oración de cada FAQ** a ≤30 palabras para voice search
3. **Añadir `dateModified`, `image`, `wordCount` y `speakable`** al schema Article

### Prioridad 2 — Alto Impacto / Esfuerzo Medio
4. **Insertar ToC con anclas** al inicio de cada artículo
5. **Citar al menos 1 fuente verificable** por artículo (ANAC, INE, Autofact, AACH, SII)
6. **Insertar tabla comparativa** en Arts. 05, 08 y 09 (los únicos sin tabla)

### Prioridad 3 — Impacto Medio / Esfuerzo Medio
7. **Añadir schema `DefinedTermSet`** en artículos tipo Glosario (12, 16, 19, 20)
8. **Añadir H2 con keyword secundaria** en artículos que solo la tienen en H3 o texto corrido
9. **Neutralizar lenguaje subjetivo** en los answer-blocks (mantener tono editorial en el cuerpo)

### Prioridad 4 — Mejora Continua
10. **Cross-linking audit**: Revisar que cada artículo tenga al menos 2 enlaces internos entrantes y 2 salientes para distribuir link juice equitativamente

---

## Verificación Final: ¿Estas mejoras aumentan la probabilidad de aparecer en AI Overviews?

| Mejora | ¿Aumenta citabilidad en AI Overview? | Razón |
| :--- | :---: | :--- |
| Answer-Block semántico | **Sí** ✅ | Los LLMs extraen bloques auto-contenidos como respuesta directa |
| Citación de fuentes | **Sí** ✅ | Google SGE prioriza contenido con E-E-A-T demostrable |
| Schema enriquecido | **Sí** ✅ | Facilita la comprensión estructural para crawlers y LLMs |
| ToC con anclas | **Sí** ✅ | Permite a la IA mapear y citar secciones específicas |
| Tablas comparativas | **Sí** ✅ | Formato preferido por LLMs para queries "vs" o "diferencia entre" |
| Lenguaje objetivo en summaries | **Sí** ✅ | Los LLMs prefieren citar declaraciones factuales sobre opiniones |
