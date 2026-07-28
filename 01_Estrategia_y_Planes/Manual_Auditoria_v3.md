# Manual de Auditoría Integral v3.0: Ecosistema de Contenidos MITTA & MittaGO

**Versión:** 3.0  
**Fecha:** Julio 2026  
**Autor:** INMedios — Estrategia de Contenidos Digitales  
**Alcance:** 20 artículos MITTA + 29 artículos MittaGO (49 artículos totales)  
**Consolidado de:** 12 fuentes documentales del proyecto

---

## 🎯 Objetivo

Este manual establece el marco metodológico **definitivo** para auditar la totalidad de los contenidos redactados para las marcas MITTA y MittaGO. Está diseñado para ser ejecutado como **gate de calidad final** al cierre de cada ciclo de producción, garantizando que ningún artículo se publique sin cumplir los 15 parámetros de verificación.

### Cuándo ejecutar esta auditoría

1. Al completar un lote nuevo de artículos (Fase 2 del Flujo de Producción).
2. Después de incorporar feedback del cliente (Fase 5).
3. Antes del ensamblaje final y entrega PDF (Fase 6).
4. Al realizar modificaciones masivas a artículos ya aprobados.

### Principio rector

> **Todo dato del artículo debe ser rastreable a una fuente documental específica. Si no puede rastrearse, no se publica.**

---

## 📐 Las 15 Capas del Protocolo de Auditoría

```text
 ╔══════════════════════════════════════════════════════════════════════╗
 ║                    BLOQUE A: INTEGRIDAD FÁCTICA                     ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║  C1:  Marco Cerrado y Anti-Alucinación                              ║
 ║  C2:  Verificación Fáctica de Datos Duros ★                         ║
 ║  C3:  Trazabilidad a Base de Conocimiento ★                         ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║                BLOQUE B: OPTIMIZACIÓN PARA IA                       ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║  C4:  AEO (Answer Engine Optimization)                              ║
 ║  C5:  GEO (Generative Engine Optimization)                          ║
 ║  C6:  Schema.org JSON-LD y Rich Snippets                            ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║              BLOQUE C: SEO TÉCNICO Y CONVERSIÓN                     ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║  C7:  Metadatos SEO (Title, Description, Slug, Keywords)            ║
 ║  C8:  Navegación y Conversión (Breadcrumbs, CTA)                    ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║                 BLOQUE D: CALIDAD EDITORIAL                         ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║  C9:  Redacción, Legibilidad y Escaneabilidad                       ║
 ║  C10: Tono de Marca y Glosario Localizado ★                         ║
 ║  C11: Autoridad de Marca E-E-A-T                                    ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║                BLOQUE E: ARQUITECTURA WEB                           ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║  C12: Enlazado Interno (Internal Linking)                           ║
 ║  C13: Accesibilidad y HTML Semántico                                ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║              BLOQUE F: COHERENCIA SISTÉMICA                         ║
 ╠══════════════════════════════════════════════════════════════════════╣
 ║  C14: Anti-Canibalización y Consistencia Cross-Pilar                ║
 ║  C15: Producción Visual (Matriz Neurocientífica Digital Predict)     ║
 ╚══════════════════════════════════════════════════════════════════════╝
   ★ = Capa nueva respecto al protocolo v2.0
```

---

## Flujo de Ejecución de la Auditoría

```text
 INICIO ──► Ejecutar Script Automatizado (audit_final.js)
                │
                ▼
           ¿0 errores?  ──NO──► Corregir hallazgos ──► RE-EJECUTAR
                │
               SÍ
                │
                ▼
           Auditoría Manual: BLOQUE A (C1-C3)
                │
                ▼
           Auditoría Manual: BLOQUE D (C9-C11)
                │
                ▼
           Auditoría Manual: BLOQUE F (C14-C15)
                │
                ▼
           ¿Todos los checks pasan?  ──NO──► Remediar ──► RE-EJECUTAR
                │
               SÍ
                │
                ▼
           ✅ Artículos aprobados para Fase 6
```

> **Regla:** Los bloques B, C y E son 100% automatizables. Los bloques A, D y F requieren revisión humana con asistencia del agente.

---

# BLOQUE A: INTEGRIDAD FÁCTICA

---

## C1: Marco Cerrado y Anti-Alucinación

### 1.1 Regla del Marco Cerrado

- [ ] **Sin Alucinaciones:** Toda la información proviene exclusivamente de los documentos de la base de conocimiento del proyecto (ver Apéndice D para el listado completo de fuentes válidas).
- [ ] **Sin Cifras Inventadas:** Cada número, porcentaje o monto debe ser rastreable a un documento fuente específico. Si no se encuentra la fuente, usar el formato placeholder: `[PRECIO ESTIMADO $XX.XXX]`.
- [ ] **Sin Fuentes Externas No Verificadas:** Si un dato proviene de una fuente externa (ley, normativa, estadística), debe estar validada y no ser especulativa.

### 1.2 Diferenciación de Marcas

- [ ] **Aislamiento MITTA:** Los artículos de MITTA Rent a Car no contienen ninguna mención a reglas exclusivas de MittaGO (opción de compra residual, 60.000 KM neumáticos, suscripción mensual sin pie, etc.).
- [ ] **Aislamiento MittaGO:** Los artículos de MittaGO no contienen referencias a tarifas diarias, garantías con tarjeta de crédito, horas de gracia, ni otros elementos exclusivos de Rent a Car.
- [ ] **Sin Contaminación de CTA:** Los CTA de artículos MITTA apuntan a `https://www.mitta.cl/` y los de MittaGO a `https://www.mittago.cl/`. Cero cruce.

### 1.3 Precisión por Segmento

**MITTA — Rent a Car (B2C):**
- [ ] Retención de garantía en tarjeta de crédito: $450.000 base / $700.000 SUV-Camioneta / $1.500.000 zona norte 4x4.
- [ ] Atención 24/7 en Aeropuerto AMB (Arturo Merino Benítez).
- [ ] Cancelación gratis a 48 horas antes.
- [ ] Seguro CDW incluido (con excepciones regionales documentadas).
- [ ] 3 horas de gracia (30 min para Part-Time).

**MITTA — Leasing Operativo (B2B):**
- [ ] Tratamiento contable OPEX vs. CAPEX.
- [ ] Deducción 100% Impuesto Primera Categoría.
- [ ] $0 pie inicial.
- [ ] Continuidad operacional con auto de reemplazo.
- [ ] Equipamiento minero homologado.

**MittaGO — Suscripción Vehicular:**
- [ ] Cuota mensual fija todo incluido (seguro, mantención, patente, revisión técnica, asistencia en ruta, auto de reemplazo).
- [ ] Sin crédito ni pie inicial.
- [ ] No afecta capacidad crediticia (no es deuda).
- [ ] Opciones al término: renovar, extender o devolver.

---

## C2: Verificación Fáctica de Datos Duros ★

> Esta capa valida que cada cifra o dato específico mencionado en los artículos corresponda exactamente al valor documentado en las fuentes oficiales.

### 2.1 Datos MITTA Rent a Car (Fuente: Términos y Condiciones)

| Dato | Valor correcto | Fuente |
|---|---|---|
| Garantía base tarjeta crédito | $450.000 | T&C §I |
| Garantía SUV/Camioneta/Minivan | $700.000 | T&C §I |
| Garantía 4x4 zona norte (Arica-La Serena) | $1.500.000 | T&C §I |
| Garantía Coyhaique/P.Arenas/P.Natales | 20 UF + IVA + costo arriendo | T&C §I |
| Edad mínima conductor | 22 años | T&C §I |
| Tarjetas aceptadas (retail) | CMR Falabella, Cencosud Scotiabank, Banco Ripley, Líder BCI | T&C §I |
| Cancelación sin costo | Hasta 48 horas antes | T&C Importante |
| Horas de gracia estándar | 3 horas | T&C §II |
| Horas de gracia Part-Time | 30 minutos | T&C §II |
| Km libres arriendo mensual | 4.000 km ($100+IVA por km extra) | T&C §II |
| Km libres P.Arenas/P.Natales (1 día) | 300 km ($300+IVA por km extra) | T&C §II |
| Deducible colisión XI y XII región | UF 20 + IVA | T&C §III |
| Deducible robo/hurto/pérdida total | UF 80 + IVA | T&C §III |
| Deducible volcamiento 4x4 | UF 20 + IVA | T&C §III |
| Tope cobertura daños materiales | UF 500 | T&C §III |
| Tope responsabilidad civil | UF 10.000 | T&C §III |
| Deducible furgones cabina fría | UF 5 + IVA | T&C §III |
| CDW zona norte adicional (Calama/Antofagasta) | $3.000+IVA/día (tope 15 días = $45.000+IVA) | T&C §III |

### 2.2 Datos Corporativos (Fuente: Material LOP)

| Dato | Valor correcto | Fuente |
|---|---|---|
| Presencia global Mitsui & Co. | 66 países, 138 oficinas, 5 continentes | LOP Slide 3 |
| Certificaciones | ISO Calidad, Seguridad, Medio Ambiente, Compliance | LOP Slide 5 |
| Certificación CarbonNeutral® | 4.701 ton CO2e compensadas (año 2022) | LOP Slide 9 |
| Red de sucursales | Presencia en 15 regiones de Chile | LOP Slide 13 |

### 2.3 Datos MittaGO (Fuente: Marco Teórico Renting)

| Dato | Valor correcto | Fuente |
|---|---|---|
| Cuota incluye | Seguro, mantenciones, permisos, revisión técnica, asistencia en ruta, auto de reemplazo | Marco Teórico §Qué es |
| Opciones al término del contrato | Renovar, extender, devolver | Marco Teórico §Al finalizar |
| Modelo de negocio | NO es arriendo, NO es financiamiento, NO amortiza deuda | Marco Teórico §Qué NO es |

### 2.4 Protocolo de verificación

- [ ] **Check 1:** Buscar todas las cifras numéricas en el artículo.
- [ ] **Check 2:** Cruzar cada cifra con la tabla de datos duros de esta sección.
- [ ] **Check 3:** Si una cifra no aparece en ninguna fuente, marcarla como `[VERIFICAR: $XX.XXX — fuente no encontrada]`.

---

## C3: Trazabilidad a Base de Conocimiento ★

### 3.1 Fuentes válidas por tipo de contenido

| Tipo de afirmación | Fuentes válidas |
|---|---|
| Estructura de pilares y servicios | `Pilares_Estrategicos_Mitta.md` |
| Cifras, montos y restricciones Rent a Car | `Terminos_y_Condiciones_Rent_a_Car.md` |
| Datos B2B, certificaciones, sucursales, minería | `Material_Leasing_Operativo_LOP.md` |
| Propuesta de valor MittaGO, tono, terminología | `Marco_Teorico_Renting_MittaGO.md` |
| Directrices GEO, keywords, calendario editorial | `Base_Conocimiento_Milanote.md` |
| Reglas de formato y estructura HTML | `Estructura_Optima_SEO_GEO_AEO.md` |

### 3.2 Checks de trazabilidad

- [ ] **Fuente identificable:** Cada afirmación fáctica del artículo puede rastrearse a un documento de la tabla anterior.
- [ ] **Ninguna fuente externa no verificada:** Si un dato proviene de fuera (ley, normativa), debe ser comprobable en la legislación chilena vigente.
- [ ] **Coherencia entre fuentes:** Si dos documentos mencionan el mismo dato con valores distintos, prevalece el T&C oficial o el de fecha más reciente.

---

# BLOQUE B: OPTIMIZACIÓN PARA IA

---

## C4: AEO (Answer Engine Optimization)

### 4.1 Ubicación y formato

- [ ] **Ubicación del bloque:** El contenedor `.answer-block` se encuentra **inmediatamente después del `<h1>`**.
- [ ] **Conteo de palabras:** El texto del bloque AEO contiene entre **30 y 46 palabras**.
- [ ] **Keyword en las primeras 10 palabras:** La keyword principal del artículo aparece dentro de las primeras 10 palabras del bloque AEO.

### 4.2 Calidad del contenido AEO

- [ ] **Respuesta directa:** Sintetiza la respuesta fáctica exacta a la intención principal de búsqueda en un solo párrafo auto-contenido.
- [ ] **Formato Answer-First:** Inicia con el dato directo sin preámbulos.
- [ ] **Cero lenguaje promocional:** 100% factual — sin adjetivos superlativos, sin CTAs, sin lenguaje de ventas.

### 4.3 Validación con Cuestionario de Feedback (Pregunta 2)

> Si el validador elige **B** ("No entrega la respuesta de inmediato") o **C** ("Se lee como introducción") → Reescribir el bloque AEO.

---

## C5: GEO (Generative Engine Optimization)

### 5.1 Estructura semántica

- [ ] **H1 único:** Exactamente 1 `<h1>` por artículo.
- [ ] **Jerarquía H2/H3:** Secciones con `<h2>` y subsecciones con `<h3>` sin saltos de nivel.
- [ ] **IDs en H2:** Cada `<h2>` tiene un atributo `id` slugificado para anclar respuestas de IA.
- [ ] **Modularidad GEO:** Cada sección H2 funciona independientemente si una IA la extrae. Sin frases como "Como mencionamos antes".

### 5.2 Formatos de datos nativos

- [ ] **Tablas comparativas:** Al menos una tabla HTML (`<table>`) por artículo.
- [ ] **Listas estructuradas:** Pasos secuenciales en `<ol>`, beneficios en `<ul>` — nunca párrafos narrativos para datos enumerables.
- [ ] **Speakable:** Schema JSON-LD incluye `SpeakableSpecification` apuntando a `.answer-block` y `.faq-answer`.

---

## C6: Schema.org JSON-LD y Rich Snippets

### 6.1 Estructura del @graph

- [ ] **Nodo Article:** `@type: Article` con headline, description, author, publisher, dates, image, inLanguage.
- [ ] **Nodo FAQPage:** `@type: FAQPage` con las 3 preguntas FAQ del artículo.
- [ ] **Nodo BreadcrumbList:** Al menos 3 niveles (Inicio → Blog → Pilar → Artículo).
- [ ] **JSON válido:** `JSON.parse()` sin errores.

### 6.2 Consistencia de dominio por marca

| Marca | Dominio en `@id` | Dominio en `logo.url` | Dominio en `image` |
|---|---|---|---|
| **MITTA** | `https://www.mitta.cl/...` | `https://www.mitta.cl/logo.png` | `https://www.mitta.cl/blog/images/...` |
| **MittaGO** | `https://www.mittago.cl/...` | `https://www.mittago.cl/logo.png` | `https://www.mittago.cl/blog/images/...` |

- [ ] **Check dominio cruzado:** Ningún artículo de MITTA contiene `mittago.cl` en su Schema, y viceversa.

---

# BLOQUE C: SEO TÉCNICO Y CONVERSIÓN

---

## C7: Metadatos SEO

- [ ] **YAML Frontmatter:** Campos `title`, `description`, `keywords`, `pilar`, `brand`, `slug` presentes.
- [ ] **Meta Title:** 50-60 caracteres, incluye keyword principal y marca.
- [ ] **Meta Description:** 110-155 caracteres, persuasiva, con keyword y diferenciador.
- [ ] **Keywords:** 5 keywords (1 principal + 4 long-tail).
- [ ] **Slug limpio:** Lowercase, guiones, sin caracteres especiales ni tildes.

---

## C8: Navegación y Conversión

### 8.1 Breadcrumbs

- [ ] **`<nav class="breadcrumb">`** con `aria-label="Ruta de navegación"`.
- [ ] Ruta coherente con el pilar del artículo.

### 8.2 Call to Action (CTA)

- [ ] **Presencia:** Al menos 1 CTA visible antes del cierre.
- [ ] **Destino correcto:** MITTA → `mitta.cl` | MittaGO → `mittago.cl`.
- [ ] **Texto accionable:** Verbos directos ("Cotiza", "Suscríbete", "Reserva").
- [ ] **Integración natural:** No parece un "banner pegado" al texto.

### 8.3 Validación con Cuestionario de Feedback (Pregunta 3)

> Si el validador elige **B** ("Parece un banner") → Integrar el CTA en el texto.
> Si elige **C** ("No sabría qué hacer") → Rediseñar el cierre.

---

# BLOQUE D: CALIDAD EDITORIAL

---

## C9: Redacción, Legibilidad y Escaneabilidad

### 9.1 Estructura de párrafos

- [ ] **Longitud de párrafos:** Máximo **80 palabras** por párrafo.
- [ ] **Ritmo de alternancia:** Alternancia formato cada 2-3 secciones (párrafo → lista → tabla → párrafo).
- [ ] **Hook post-AEO:** Las primeras 2 frases después del AEO contextualizan el problema, no repiten el AEO.

### 9.2 Variedad léxica y anti-repetición

- [ ] **Anti-repetición keyword:** La keyword principal aparece máximo 4-5 veces en el cuerpo (excluyendo metadata, AEO y FAQ).
- [ ] **Variación de apertura:** No 3+ frases consecutivas con la misma estructura gramatical.
- [ ] **Eliminación de muletillas IA:** Cero ocurrencias de:
  - "Es importante destacar que..."
  - "Cabe mencionar que..."
  - "En este sentido..."
  - "Por otro lado..."
  - "Sin lugar a dudas..."
  - "En la actualidad..."
  - "Es fundamental señalar..."
  - "No hay que olvidar que..."
  - "Vale la pena mencionar..."

### 9.3 Extensión y FAQ

- [ ] **Rango de extensión:** 800-1.500 palabras de contenido editorial.
- [ ] **FAQ:** Exactamente **3 preguntas** con respuestas de 1-3 oraciones.
- [ ] **Cero emojis:** Formato corporativo y prístino.

### 9.4 Estilo

- [ ] **Oraciones cortas:** 15-20 palabras predominantes.
- [ ] **Segunda persona:** "puedes", "tu empresa", no "se puede".
- [ ] **Sin promesas absolutas:** Cero superlativos no sustentados.

### 9.5 Validación con Cuestionario de Feedback (Pregunta 1)

> Si el validador elige **B** ("Algunas partes densas") → Acortar párrafos o agregar viñetas.
> Si elige **C** ("Muy corto o superficial") → Expandir el artículo.

---

## C10: Tono de Marca y Glosario Localizado ★

### 10.1 Tono de voz por marca

| Dimensión | MITTA Rent a Car | MittaGO Suscripción |
|---|---|---|
| **Tono dominante** | Práctico, confiable, seguro, resolutivo | Vanguardista, anti-trámite, moderno |
| **Tagline mental** | "Viaja seguro, arrienda fácil" | "No lo compres, suscríbete" |
| **B2C** | Lenguaje directo y logístico | Cercano, positivo, aspiracional |
| **B2B** | Técnico-financiero | Profesional, racional, eficiencia |

- [ ] **Tono acorde a la marca:** El artículo refleja el tono correcto.
- [ ] **Voz de asesor, no de vendedor:** Tono dominante de asesor técnico.

### 10.2 Glosario chileno obligatorio (ambas marcas)

| Término correcto ✅ | Término prohibido ❌ |
|---|---|
| arriendo (MITTA) / suscripción (MittaGO) | alquiler |
| bencina | gasolina |
| camioneta | pickup |
| patente | matrícula / placa |
| sucursal | oficina / sede |
| mantención | mantenimiento (en B2C) |
| auto | carro / coche |

### 10.3 Terminología diferencial por marca

| Contexto | MITTA ✅ | MittaGO ✅ | Prohibido MittaGO ❌ |
|---|---|---|---|
| El servicio | "arriendo" | "suscripción" / "Renting" | "arriendo" / "alquiler" / "traslados" |
| Duración | "por día/s" | "mensual" | "por día" |
| Vehículo B2C | "auto" o "vehículo" | "auto" | "vehículo" (en B2C) |
| Vehículo B2B | "flota" / "unidad" | "vehículo" / "flota" | — |
| Producto | "MITTA Rent a Car" | "MittaGO Suscripción Vehicular" | "MittaGO Arriendo" |

- [ ] **Check terminología MITTA:** Sin términos exclusivos MittaGO.
- [ ] **Check terminología MittaGO:** Sin "arriendo"/"alquiler" como servicio.

### 10.4 Validación con Cuestionario de Feedback (Pregunta 4)

> Si el validador elige **B** ("Podría ser de cualquier empresa") → Inyectar diferenciadores (Mitsui, sucursales, 65 años).
> Si elige **C** ("Suena robótico") → Reescribir con matices humanos y tono de marca.

---

## C11: Autoridad de Marca E-E-A-T

### 11.1 Diferenciadores propietarios (mínimo 3 por artículo)

- [ ] **Mitsui & Co.:** Al menos 1 mención al respaldo corporativo.
- [ ] **Red nacional:** Referencia a 80+ sucursales / 15 regiones.
- [ ] **Dato único no replicable:** Al menos 1 dato exclusivo de la marca.
- [ ] **Asistencia 24/7:** Mención a la asistencia en ruta.

### 11.2 Señales de experiencia

- [ ] **Contexto chileno auténtico:** Realidades locales verificables (TAG, CMF, sillas infantiles, permisos RCI).
- [ ] **Sin contenido genérico globalizado.**

### 11.3 Transparencia

- [ ] **Condiciones explícitas:** Beneficios con sus restricciones ("cancelación gratis hasta 48 horas antes").
- [ ] **Sin omisión de restricciones:** Edad mínima, garantías y exclusiones visibles.

---

# BLOQUE E: ARQUITECTURA WEB

---

## C12: Enlazado Interno (Internal Linking)

- [ ] **Cantidad mínima:** Al menos **2 enlaces internos** por artículo.
- [ ] **Anchor text descriptivo:** Sin "haz clic aquí" ni "ver más".
- [ ] **Enlace intra-pilar (obligatorio):** Al menos 1 enlace al mismo pilar.
- [ ] **Enlace cross-pilar (recomendado):** 1 enlace a pilar complementario cuando aplica.
- [ ] **Bloque sugerencia:** `<!-- LINK INTERNO SUGERIDO: "texto" -> /slug/ -->` si la URL no existe.

---

## C13: Accesibilidad y HTML Semántico

### 13.1 Estructura HTML5

- [ ] **`<article class="article-content">`:** Envuelve todo el contenido editorial.
- [ ] **`<nav class="breadcrumb">`:** Con `aria-label="Ruta de navegación"`.
- [ ] **`<header class="meta-header">`:** Ficha técnica del artículo.
- [ ] **`<main class="container">`:** Contenido principal.

### 13.2 Imágenes

- [ ] **Alt text descriptivo:** Cada `<img>` con `alt` contextual.
- [ ] **Formato WebP:** Imágenes de producción en WebP.

### 13.3 Contraste

- [ ] **Ratio de contraste AA:** Texto (#2D2D2D / #FAFAFA) cumple 4.5:1 WCAG AA.
- [ ] **Tamaño mínimo fuente:** ≥14px (0.875rem).

### 13.4 Tablas accesibles

- [ ] **Scope en headers:** `<th>` con `scope="col"` o `scope="row"`.
- [ ] **Caption o aria-label:** Cada `<table>` con descripción.

---

# BLOQUE F: COHERENCIA SISTÉMICA

---

## C14: Anti-Canibalización y Consistencia Cross-Pilar

### 14.1 Anti-canibalización de keywords

- [ ] **Keyword principal única:** Ninguna keyword principal duplicada entre artículos del mismo dominio.
- [ ] **Intent match:** Sin 2 artículos compitiendo por la misma intención sobre el mismo topic.

### 14.2 Consistencia terminológica

- [ ] **Glosario unificado:**
  - "Renting Flexible" (no "Renting Mensual")
  - "Leasing Operativo" (no "Leasing Financiero")
  - "CDW" para seguro de colisión (no "seguro todo riesgo")
  - "AMB" o "Aeropuerto Arturo Merino Benítez" (no "Pudahuel")
- [ ] **Nombres oficiales:** "MITTA Rent a Car", "MittaGO Suscripción Vehicular".

### 14.3 Detección de patrones IA

- [ ] **Anti-pattern estructuras clonadas:** No 2+ artículos con la misma secuencia de H2.
- [ ] **Unicidad de cierres:** Párrafo pre-CTA único por artículo.
- [ ] **FAQ no duplicadas:** Ninguna pregunta FAQ repetida entre artículos del mismo pilar.

---

## C15: Producción Visual (Matriz Neurocientífica)

- [ ] **Bloque visual final:** `.visual-prompt-matrix` al cierre del artículo.
- [ ] **Hero Image (16:9):** Prompt visual con justificación neurocientífica.
- [ ] **In-Text Image (1:1):** Prompt para infografías con justificación atencional.
- [ ] **Coherencia marca-visual:** Sin logotipos de competidores.
- [ ] **Contexto chileno:** Paisajes y entornos relevantes para Chile.

### 15.1 Validación con Cuestionario de Feedback (Pregunta 5)

> Si el validador elige **B** ("No generan emoción") → Aplicar sesgos visuales (Gaze Cuing, Contraste Espacial).
> Si elige **C** ("Sin relación con la preocupación del cliente") → Re-alinear con el Job-to-be-Done.

---

# APÉNDICES

---

## Apéndice A: Tabla Maestra de Datos Duros

### A.1 — MITTA Rent a Car

| ID | Dato | Valor | Unidad | Fuente |
|:---:|---|---|---|---|
| M01 | Garantía base | 450.000 | CLP | T&C §I |
| M02 | Garantía SUV/Camioneta | 700.000 | CLP | T&C §I |
| M03 | Garantía 4x4 zona norte | 1.500.000 | CLP | T&C §I |
| M04 | Garantía Coyhaique/P.Arenas | 20+IVA+arriendo | UF | T&C §I |
| M05 | Edad mínima | 22 | años | T&C §I |
| M06 | Cancelación gratis | 48 | horas | T&C Imp. |
| M07 | Gracia estándar | 3 | horas | T&C §II |
| M08 | Gracia Part-Time | 30 | min | T&C §II |
| M09 | Km libres mensual | 4.000 | km | T&C §II |
| M10 | Km extra mensual | 100+IVA | CLP/km | T&C §II |
| M11 | Km libres P.Arenas 1d | 300 | km | T&C §II |
| M12 | Km extra P.Arenas | 300+IVA | CLP/km | T&C §II |
| M13 | Deducible XI-XII | 20+IVA | UF | T&C §III |
| M14 | Deducible robo | 80+IVA | UF | T&C §III |
| M15 | Deducible volc. 4x4 | 20+IVA | UF | T&C §III |
| M16 | Tope daños | 500 | UF | T&C §III |
| M17 | Tope resp. civil | 10.000 | UF | T&C §III |
| M18 | Deducible furgón frío | 5+IVA | UF | T&C §III |
| M19 | CDW norte/día | 3.000+IVA | CLP | T&C §III |
| M20 | CDW norte tope | 45.000+IVA | CLP | T&C §III |

### A.2 — Datos Corporativos

| ID | Dato | Valor | Fuente |
|:---:|---|---|---|
| C01 | Presencia Mitsui | 66 países, 138 oficinas | LOP Slide 3 |
| C02 | CarbonNeutral® | 4.701 ton CO2e (2022) | LOP Slide 9 |
| C03 | Red sucursales | 15 regiones | LOP Slide 13 |
| C04 | Antigüedad | +65 años | Validado |

---

## Apéndice B: Pilares Estratégicos por Marca

### B.1 — MITTA (4 pilares)

| Pilar | Segmento | Artículos |
|---|---|:---:|
| Rent a Car (B2C y Turismo) | B2C | 01-05 |
| Leasing Operativo (B2B y Flotas) | B2B | 06-10 |
| Renting Flexible (Puente B2C/Pymes) | B2C/B2B | 11-15 |
| Notas de Utilidad (Evergreen & Tips) | B2C | 16-20 |

### B.2 — MittaGO (4 pilares)

| Pilar | Segmento | Artículos |
|---|---|---|
| Presupuestos (Finanzas Inteligentes) | B2C/Pymes | 02,04,05,10,13,21,23 |
| Suscripciones (Claridad Operativa) | B2C | 01,03,09,22,24,25,26 |
| Smart Uses (Estilos de Vida) | B2C | 06,07,08,11 |
| Educación (Cultura de Movilidad) | B2C | 12,14,15,16,17,18,19,20,27,28,29 |

---

## Apéndice C: Especificación del Script de Auditoría

### `audit_final.js` — Checks automatizados

| Capa | Check | Criterio | Tipo |
|:---:|---|---|:---:|
| C4 | Bloque AEO | `.answer-block` existe tras `<h1>` | ❌ |
| C4 | Extensión AEO | 30-50 palabras | ⚠️ |
| C5 | H1 único | Exactamente 1 `<h1>` | ❌ |
| C5 | IDs en H2 | Todos `<h2>` tienen `id` | ⚠️ |
| C5 | Tabla HTML | ≥1 `<table>` | ⚠️ |
| C6 | JSON-LD válido | `JSON.parse()` OK | ❌ |
| C6 | Nodos @graph | Article + FAQPage + Breadcrumb | ❌ |
| C6 | Dominio Schema | Correcto por marca | ❌ |
| C7 | Frontmatter | title, description, keywords | ❌ |
| C7 | Meta title | 50-60 chars | ⚠️ |
| C7 | Meta description | 110-155 chars | ⚠️ |
| C8 | Breadcrumbs | `<nav class="breadcrumb">` | ❌ |
| C8 | CTA | Enlace a dominio correcto | ❌ |
| C9 | Extensión | 800-1.500 palabras | ❌ |
| C9 | Párrafos ≤80 | Ninguno supera 80 | ⚠️ |
| C9 | Muletillas IA | 0 de lista negra | ⚠️ |
| C9 | FAQ count | Exactamente 3 | ❌ |
| C10 | Términos prohibidos | 0 "arriendo" en MittaGO | ❌ |
| C11 | E-E-A-T markers | ≥3 diferenciadores | ⚠️ |
| C12 | Enlaces internos | ≥2 | ❌ |
| C13 | `<main>` wrapper | Presente | ⚠️ |
| C13 | `aria-label` | En breadcrumbs | ⚠️ |
| C13 | `<article>` wrapper | Presente | ⚠️ |

### Uso

```bash
# Auditar MITTA
node audit_final.js --brand mitta --dir ./02_Contenidos_Redactados/Mitta/finales/

# Auditar MittaGO
node audit_final.js --brand mittago --dir ./02_Contenidos_Redactados/MittaGO/finales/
```

---

## Apéndice D: Tabla de Fuentes y Trazabilidad

| Código | Documento | Ruta | Contenido clave |
|:---:|---|---|---|
| F01 | Pilares Estratégicos | `Pilares_Estrategicos_Mitta.md` | Definición de 8 pilares |
| F02 | Estructura SEO/GEO/AEO | `Estructura_Optima_SEO_GEO_AEO.md` | Anatomía de 7 bloques |
| F03 | Base Conocimiento | `Base_Conocimiento_Milanote.md` | Directrices GEO, keywords |
| F04 | Cuestionario Feedback | `Cuestionario_Feedback_Cliente.md` | 5 preguntas validación |
| F05 | Flujo Producción | `Flujo_Produccion_Contenidos_Mitta.md` | 6 fases workflow |
| F06 | Términos y Condiciones | `Terminos_y_Condiciones_Rent_a_Car.md` | Montos, deducibles |
| F07 | Material LOP | `Material_Leasing_Operativo_LOP.md` | Datos corporativos |
| F08 | Marco Teórico MittaGO | `Marco_Teorico_Renting_MittaGO.md` | Propuesta de valor |
| F09 | Prompt Maestro RaC | `Prompt_Maestro_RentACar.md` | Formato MITTA |
| F10 | Prompt Maestro MittaGO | `Prompt_Maestro_MittaGO.md` | Formato MittaGO |
| F11 | Guía Ficha Técnica | `Guia_Lectura_Ficha_Tecnica.md` | Campos frontmatter |
| F12 | Milanote Raw Export | `Milanote_Raw_Export.md` | Datos brutos SEO |

---

## Tabla de Verificación: MITTA (20 artículos)

| N° | Archivo | Pilar | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | C13 | C14 | C15 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 01_Guia_Arriendo_Aeropuerto | RaC | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 2 | 02_Arriendo_Autos_Norte | RaC | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 3 | 03_Arriendo_Puerto_Montt | RaC | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 4 | 04_Categoria_Vehiculo | RaC | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 5 | 05_Cruce_Argentina | RaC | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 6 | 06_Ventajas_Tributarias | LOP | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 7 | 07_Leasing_vs_Compra | LOP | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 8 | 08_Continuidad_Reemplazo | LOP | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 9 | 09_Flotas_Mineras | LOP | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 10 | 10_Electromovilidad_ESG | LOP | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 11 | 11_Arriendo_Mensual_Pymes | RF | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 12 | 12_Renting_vs_Credito | RF | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 13 | 13_Movilidad_Sin_Pie | RF | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 14 | 14_Renovacion_Unidades | RF | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 15 | 15_Evaluacion_Comercial | RF | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 16 | 16_Asistencia_Ruta | NdU | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 17 | 17_Sillas_Infantiles | NdU | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 18 | 18_Conduccion_Eficiente | NdU | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 19 | 19_Mascotas_Pet_Friendly | NdU | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 20 | 20_Manual_vs_Automatica | NdU | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

**Leyenda:** RaC=Rent a Car | LOP=Leasing Operativo | RF=Renting Flexible | NdU=Notas de Utilidad

---

## Tabla de Verificación: MittaGO (29 artículos)

| N° | Archivo | Pilar | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | C13 | C14 | C15 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 01_Como_Funciona_MittaGO | Susc | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 2 | 02_Suscripcion_vs_Credito | Pres | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 3 | 03_Que_Incluye_Cuota | Susc | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 4 | 04_Costos_Ocultos | Pres | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 5 | 05_MittaGO_vs_Rent_a_Car | Pres | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 6 | 06_Expatriados | Smart | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 7 | 07_Pymes_Emprendedores | Smart | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 8 | 08_Suscripcion_Temporada | Smart | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 9 | 09_Cambiar_de_Auto | Susc | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 10 | 10_Costo_Depreciacion | Pres | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 11 | 11_Trabajo_Hibrido | Smart | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 12 | 12_Diccionario_Movilidad | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 13 | 13_Guia_Presupuesto | Pres | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 14 | 14_Smart_Mobility | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 15 | 15_Autos_Hibridos | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 16 | 16_Mantenimiento_Cero | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 17 | 17_Siniestros_Sin_Estres | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 18 | 18_Auto_Reemplazo | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 19 | 19_Economia_Circular | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 20 | 20_Sistemas_ADAS | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 21 | 21_Presupuesto_Movilidad | Pres | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 22 | 22_Evaluacion_Onboarding | Susc | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 23 | 23_Opcion_Compra | Pres | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 24 | 24_Suscripcion_Independ. | Susc | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 25 | 25_Startups_Microempresas | Susc | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 26 | 26_SUV_Familias | Susc | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 27 | 27_Auto_Reemplazo_Cont. | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 28 | 28_Cuidado_Neumaticos | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 29 | 29_Protocolo_Siniestros | Edu | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

**Leyenda:** Pres=Presupuestos | Susc=Suscripciones | Smart=Smart Uses | Edu=Educación

---

*Manual generado por INMedios — Protocolo de Auditoría v3.0*
*Consolidado de 12 fuentes documentales del proyecto MITTA/MittaGO*
