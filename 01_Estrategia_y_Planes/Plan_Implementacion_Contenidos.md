# Plan de Implementacion v3.1: Fabrica de Contenidos SEO/GEO/AEO 2026

**Version:** 3.1
**Fecha:** 2026-05-08
**Responsable:** Agente INMedios
**Alcance:** 40 articulos (20 Mitta Rent a Car + 20 MittaGO)

Este documento es el protocolo operativo definitivo para la produccion de contenidos Evergreen optimizados para motores de busqueda tradicionales (SEO), motores de respuesta generativa (GEO) y motores de respuesta por voz (AEO).

> **Nota sobre formato:** Este documento de plan usa ASCII plano (sin tildes) por compatibilidad con sistemas de archivos y terminales. Los articulos finales destinados a publicacion deben usar ortografia completa con tildes y caracteres especiales del espanol de Chile.

---

## 1. Contexto de Marca Inmutable

Estos datos duros deben aparecer de forma natural en todos los articulos. Son la base de autoridad E-E-A-T de la marca.

| Dato | Valor | Uso editorial |
|------|-------|---------------|
| Nombre corporativo | Mitta (antes Salfa Rent a Car) | Mencion historica para construir trayectoria |
| Respaldo internacional | Mitsui & Co., Ltd. (Japon) | Citar como respaldo financiero y de gobernanza |
| Cobertura nacional | +80 sucursales en Chile | Usar en claims de accesibilidad geografica |
| Marcas del ecosistema | Mitta (Rent a Car), MittaGO (Renting/Suscripcion), First (Premium/Corporativo) | Diferenciar segun el pilar del articulo |
| Propuesta de valor B2C | Flexibilidad, cero tramites, tarifa plana predecible | Tono cercano, anti-burocracia |
| Propuesta de valor B2B | Continuidad operacional, beneficio tributario, externalizacion total | Tono corporativo, orientado a ROI |
| Diferenciadores clave | Asistencia en ruta 24/7, vehiculo de reemplazo inmediato, flota renovada | Usar como cierre de argumento en cada articulo |
| Idioma y registro | Espanol de Chile: "arriendo", "camioneta", "bencina", "pana", "sucursal" | Nunca usar "alquiler" ni "gasolina" |

---

## 2. Estructura de Directorios

```
/02_Contenidos_Redactados/
    MittaGO/
        01_Como_Funciona_MittaGO.md
        02_Suscripcion_vs_Credito.md
        ...
    Mitta_Rent_a_Car/
        01_Guia_Aeropuertos.md
        02_Requisitos_Extranjeros.md
        ...
    Registro_Memoria_Editorial.md
    Checklist_Calidad.md
```

---

## 3. Formato Signature por Pilar

Cada pilar tiene una estructura visual dominante que lo diferencia del resto, evitando monotonia editorial.

### MittaGO

| Pilar | Formato Signature | Elemento obligatorio | Tono |
|-------|-------------------|---------------------|------|
| Presupuestos | Comparativa numerica | Tabla de costos mensuales (suscripcion vs propiedad) | Racional, financiero |
| Suscripciones | Guia paso a paso | Flujo numerado del proceso (1, 2, 3...) | Claro, operativo |
| Smart Uses | Escenario narrativo (storytelling) | Caso de uso con persona ficticia ("Maria, 34 anos, trabaja hibrido...") | Aspiracional, moderno |
| Educacion | Glosario o explicacion tecnica | Definicion destacada en bloque (blockquote o recuadro) | Didactico, neutral |

### Mitta Rent a Car

| Pilar | Formato Signature | Elemento obligatorio | Tono |
|-------|-------------------|---------------------|------|
| Rent a Car (Turismo) | Guia practica geolocaliada | Mencion de ciudades y rutas especificas de Chile | Cercano, aventurero |
| Leasing Operativo (Flotas) | Caso de negocio (Business Case) | Tabla de ROI o simulacion financiera simplificada | Corporativo, tecnico |
| Renting (Suscripcion) | Comparativa de producto | Tabla "que incluye vs que no incluye" | Transparente, directo |
| Notas (Educacion/Tips) | Checklist o listicle | Lista de viñetas accionables ("Haz esto / Evita esto") | Util, practico |

---

## 4. Ciclo de Vida de cada Articulo (Flujo "1 a 1")

Por cada uno de los 40 temas, el Agente ejecutara los siguientes 7 pasos sin excepcion:

### Paso 0: Validacion de Keyword, Contexto e Intencion SERP

Antes de comenzar, el Agente revisara:
- La keyword principal asignada al articulo (desde la Propuesta de Contenidos).
- El segmento objetivo (B2B o B2C).
- La intencion de busqueda dominante: Informacional, Transaccional o Navegacional.
- **Analisis SERP competitivo:** El Agente utilizara la herramienta `search_web` para consultar la keyword principal en Google y extraer los angulos editoriales de los primeros resultados. Se registrara:
  - Angulo editorial que usan los 3 primeros resultados (tutorial, comparativa, listado).
  - Longitud promedio del contenido (corto, medio, largo).
  - Elementos que les faltan y que representan una oportunidad para Mitta (tablas, datos concretos, FAQ, Answer Block).
  - Preguntas del bloque "La gente tambien pregunta" (People Also Ask) si existen, para alimentar la seccion FAQ.
- **Output:** Ficha de contexto con keyword confirmada, intencion, angulo diferenciador y oportunidad detectada.

### Paso 1: Escaneo de Memoria (Prevencion de Redundancias)

Antes de escribir una sola palabra, el Agente leera el archivo `Registro_Memoria_Editorial.md`.
- **Objetivo:** Revisar de que trataron los articulos anteriores, que estadisticas se usaron, que ejemplos se dieron y que CTAs se aplicaron.
- **Beneficio SEO:** Permite planificar Enlazado Interno (Internal Linking). Si el Articulo 3 habla de Pymes, y el Articulo 1 hablaba de Presupuestos, se forzara un enlace natural del 3 al 1.
- **Regla:** Si un dato, ejemplo o CTA ya fue utilizado, queda PROHIBIDO repetirlo. Se debe buscar un dato alternativo o reformular el enfoque.

### Paso 2: Redaccion en Frio (Basado en Prompt Maestro)

Se generara el primer borrador aplicando estrictamente las reglas del `Prompt_Maestro_Contenidos.md`:
- **Answer Block inicial:** 40-60 palabras directo al grano (AEO). Debe responder a la intencion de busqueda principal del H1.
- **Estructura E-E-A-T:** Tono experto, oraciones cortas (15-20 palabras).
- **Riqueza Semantica:** Uso de H2 y H3 con variaciones de la Keyword principal.
- **Longitud objetivo:** 800-1.200 palabras (sin contar metadatos ni FAQ).
- **Formato Signature:** Aplicar el formato correspondiente al pilar del articulo (ver Seccion 3).
- **Regla de diferenciacion Answer Block vs FAQ:** Las 3 preguntas del FAQ deben abordar intenciones de busqueda secundarias que NO esten cubiertas por el Answer Block ni por los H2 principales del articulo. Queda PROHIBIDO que una pregunta del FAQ repita o reformule lo que ya dice el Answer Block.
- **Elementos obligatorios por articulo:**
  - Minimo 1 tabla o lista comparativa (segun Formato Signature).
  - Minimo 3 datos cuantitativos (cifras, porcentajes, rangos de precio).
  - Minimo 2 sugerencias de enlace interno a otros articulos o servicios de Mitta.
  - Mencion natural de al menos 1 dato del Contexto de Marca Inmutable (Seccion 1).

### Paso 3: Auditoria con Score Card (SEO/GEO/AEO)

El Agente auditara su propio borrador aplicando el siguiente checklist binario. Cada criterio vale 1 punto. Total: 18 puntos.

**Bloque SEO (5 puntos):**
- [ ] El H1 contiene la keyword principal o una variacion cercana.
- [ ] Hay al menos 3 H2 y 2 H3 con keywords secundarias.
- [ ] La keyword principal aparece en el primer parrafo (Answer Block).
- [ ] La meta description tiene entre 110-155 caracteres y contiene un CTA implicito.
- [ ] El slug sugerido es corto, descriptivo y sin stop-words.

**Bloque GEO (4 puntos):**
- [ ] Hay al menos 1 tabla HTML o lista comparativa estructurada.
- [ ] Hay al menos 3 negritas estrategicas en datos clave.
- [ ] El Answer Block funciona como parrafo independiente (se puede copiar y citar sin contexto).
- [ ] Los datos cuantitativos son especificos (no "muchos usuarios" sino "el 68% de los usuarios").

**Bloque AEO (3 puntos):**
- [ ] Al menos 2 H2 estan formulados como preguntas directas.
- [ ] La respuesta a cada H2-pregunta comienza inmediatamente debajo, sin rodeos.
- [ ] La seccion FAQ tiene exactamente 3 preguntas con respuestas de 40-60 palabras cada una.

**Bloque Comercial (3 puntos):**
- [ ] El tono es coherente con el segmento (B2B corporativo o B2C cercano).
- [ ] Hay un CTA final alineado al servicio (no generico).
- [ ] Se menciona al menos un diferenciador de marca (respaldo Mitsui, cobertura nacional, asistencia 24/7).

**Bloque Anti-Redundancia (3 puntos):**
- [ ] Ningun ejemplo, estadistica o CTA se repite respecto a articulos anteriores.
- [ ] Se incluyen al menos 2 enlaces internos a articulos ya publicados del mismo ecosistema.
- [ ] El Formato Signature del pilar se aplica correctamente.

**Umbral de Aprobacion:**

| Puntaje | Veredicto | Accion |
|---------|-----------|--------|
| 16-18 / 18 | Publicable | Pasar a Paso 4 |
| 13-15 / 18 | Revision menor | Corregir criterios fallidos y re-evaluar |
| 12 o menos / 18 | Reescritura | Volver al Paso 2 con nuevo angulo |

### Paso 4: Exportacion y Metadatos

Se creara un archivo `.md` individual con la siguiente estructura de Frontmatter YAML:

```yaml
---
titulo: "Como funciona MittaGO: Tu auto por mes sin amarras"
meta_title: "Como Funciona MittaGO | Arriendo Mensual de Autos en Chile"
meta_description: "Descubre como funciona MittaGO paso a paso: elige tu auto, suscribete online y recibelo en tu puerta. Sin pie, sin papeleos."
slug: /como-funciona-mittago/
keyword_principal: "como funciona mittago"
keywords_secundarias:
  - arriendo mensual auto chile
  - suscripcion auto santiago
  - renting autos mittago
segmento: B2C
marca: MittaGO
pilar: Suscripciones
formato_signature: Guia paso a paso
fecha_redaccion: 2026-05-08
score_card: 17/18
estado: borrador
enlaces_salientes:
  - /suscripcion-vs-credito-automotriz/
  - /que-incluye-cuota-mittago/
enlaces_entrantes: []
---
```

El campo `enlaces_entrantes` se llena retroactivamente: cuando un articulo posterior referencia a este, se agrega el slug del articulo que lo enlaza. Esto permite verificar en el Paso 6 (Checkpoint) que el mapa de enlaces internos es equilibrado y que ningun articulo queda huerfano (sin enlaces entrantes).

El contenido del articulo sigue inmediatamente despues del Frontmatter.

Al final del articulo se incluyen los bloques de Schema Markup:

**FAQ Schema (obligatorio en todos los articulos):**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Pregunta 1",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Respuesta directa de 40-60 palabras."
      }
    }
  ]
}
```

**Article Schema (obligatorio en todos los articulos):**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Titulo del articulo",
  "description": "Meta description del articulo",
  "author": {
    "@type": "Organization",
    "name": "Mitta",
    "url": "https://www.mitta.cl"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Mitta"
  },
  "datePublished": "2026-05-08",
  "mainEntityOfPage": "URL del articulo"
}
```

**Service Schema (solo para articulos de Suscripciones y Leasing Operativo):**
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "MittaGO Suscripcion de Vehiculos",
  "provider": {
    "@type": "Organization",
    "name": "Mitta"
  },
  "description": "Servicio de arriendo mensual de vehiculos en Chile.",
  "areaServed": "Chile"
}
```

### Paso 5: Actualizacion de Memoria

Se agregara la siguiente ficha al `Registro_Memoria_Editorial.md`:

```
## Articulo XX: [Titulo]
- Pilar: [Presupuestos / Suscripciones / Smart Uses / Educacion]
- Keyword: [keyword principal]
- Formato Signature: [Tabla comparativa / Guia paso a paso / Storytelling / Glosario]
- Datos usados: [lista de estadisticas o cifras citadas]
- Ejemplos usados: [ejemplos, analogias o personas ficticias utilizadas]
- CTA utilizado: [texto exacto del CTA final]
- Enlaces internos sugeridos: [lista de articulos referenciados]
- Score Card: [XX/18]
- Resumen (2 lineas): [sintesis del articulo]
```

### Paso 6: Checkpoint de Aprobacion (cada 5 articulos)

Al completar el articulo 5, 10, 15 y 20 de cada bloque, se realiza una pausa para:
- Revisar la coherencia narrativa del conjunto.
- Confirmar que no hay canibalismo de keywords entre articulos (dos articulos compitiendo por la misma keyword).
- Validar que el mapa de enlaces internos sea equilibrado (todos los articulos reciben y dan enlaces).
- Revisar que los Score Cards promedien 15/18 o mas en el bloque.

---

## 5. Orden de Prioridad de Redaccion

La prioridad se define por posicion en el embudo de conversion (Bottom of Funnel primero, Top of Funnel al final).

### Bloque MittaGO (20 articulos)

| Orden | Pilar | Titulo | Formato Signature | Prioridad |
|-------|-------|--------|-------------------|-----------|
| 1 | Suscripciones | Como funciona MittaGO | Guia paso a paso | BoFu - Alta conversion |
| 2 | Presupuestos | Suscripcion vs Credito Automotriz | Tabla comparativa | BoFu - Objecion principal |
| 3 | Suscripciones | Que incluye la cuota mensual | Guia paso a paso | BoFu - Confianza |
| 4 | Presupuestos | Costos ocultos de mantener un auto | Tabla comparativa | MoFu - Educacion financiera |
| 5 | Suscripciones | MittaGO vs Rent a Car tradicional | Guia paso a paso | MoFu - Diferenciacion |
| 6 | Smart Uses | Expatriados y extranjeros en Chile | Storytelling | MoFu - Nicho alto valor |
| 7 | Presupuestos | Suscripcion para Pymes | Tabla comparativa | MoFu - Segmento clave |
| 8 | Smart Uses | Suscripcion de temporada (verano) | Storytelling | MoFu - Estacional |
| 9 | Suscripciones | Cambiar de auto segun necesidad | Guia paso a paso | MoFu - UVP del producto |
| 10 | Presupuestos | El costo de la depreciacion | Tabla comparativa | MoFu - Educativo |
| 11 | Smart Uses | Trabajo hibrido y movilidad | Storytelling | ToFu - Tendencia |
| 12 | Educacion | Renting, Leasing y Compra: Diccionario | Glosario | ToFu - Alfabetizacion |
| 13 | Presupuestos | Guia de presupuesto de movilidad | Tabla comparativa | MoFu - Transaccional |
| 14 | Smart Uses | Smart Mobility urbana | Storytelling | ToFu - Aspiracional |
| 15 | Suscripciones | Autos hibridos por suscripcion | Guia paso a paso | ToFu - Electromovilidad |
| 16 | Educacion | Mantenimiento Cero | Glosario | ToFu - Emocional |
| 17 | Educacion | Siniestros sin estres | Glosario | ToFu - Confianza |
| 18 | Smart Uses | Auto de reemplazo larga estadia taller | Storytelling | ToFu - Urgencia |
| 19 | Educacion | Economia Circular Automotriz | Glosario | ToFu - PR/ESG |
| 20 | Educacion | Tecnologia ADAS a bordo | Glosario | ToFu - Educativo |

### Bloque Mitta Rent a Car (20 articulos)
Se definira al completar el bloque MittaGO, aplicando la misma logica de embudo y asignando Formatos Signature segun los pilares de Rent a Car.

---

## 6. Hoja de Ruta de Ejecucion

| Fase | Descripcion | Entregable | Criterio de exito |
|------|-------------|------------|-------------------|
| 1 | Set Up y Piloto | Articulo #1 de MittaGO redactado y aprobado | Score Card 16+/18, aprobacion del cliente |
| 2 | Bloque MittaGO | 19 articulos restantes con checkpoints en #5, #10, #15, #20 | Promedio Score Card 15+/18, cero redundancias |
| 3 | Bloque Rent a Car | 20 articulos con checkpoints en #5, #10, #15, #20 | Promedio Score Card 15+/18, cero redundancias |
| 4 | Consolidacion | 2 archivos HTML finales (uno por marca) con indice navegable | Todos los enlaces internos funcionales |
| 5 | Monitoreo 30-60-90 | Informe de rendimiento por articulo | KPIs definidos abajo |

---

## 7. Fase 5: Monitoreo Post-Publicacion (30-60-90 dias)

Una vez publicados los articulos en el CMS del cliente, se mediran los siguientes KPIs por articulo:

### KPIs SEO (Google Search Console)
- Posicion promedio para la keyword principal.
- Impresiones y clics organicos.
- CTR (Click-Through Rate) del snippet.

### KPIs GEO (Citacion por IA)
- Verificacion manual: buscar la keyword en ChatGPT, Gemini y Perplexity y registrar si Mitta aparece como fuente citada.
- Frecuencia de citacion: mensual.

### KPIs AEO (Featured Snippets)
- Verificacion: buscar la keyword en Google y registrar si el articulo aparece como Featured Snippet (posicion 0) o en el bloque "La gente tambien pregunta".

### KPIs Comerciales
- Trafico al CTA (via UTMs o eventos en GA4).
- Tasa de conversion del CTA (formularios, cotizaciones, llamadas).

### Ciclo de Retroalimentacion
- A los 30 dias: Identificar articulos con 0 impresiones y revisar si requieren ajuste de keyword o ampliacion de contenido.
- A los 60 dias: Identificar articulos con alto impresiones pero bajo CTR y optimizar meta titles y descriptions.
- A los 90 dias: Informe consolidado con recomendaciones de actualizacion o creacion de nuevos articulos derivados.
