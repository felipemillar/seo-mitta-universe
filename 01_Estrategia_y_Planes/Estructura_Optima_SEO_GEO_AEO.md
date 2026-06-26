# Anatomía de un Documento Óptimo: SEO + GEO + AEO

Esta guía define la estructura técnica y de contenido para lograr la máxima visibilidad en motores de búsqueda tradicionales (Google Search) y motores generativos/IA (ChatGPT, Perplexity, Gemini, Google AI Overviews).

---

## 1. Frontmatter (Metadatos Estructurales)
El documento debe iniciar con un bloque YAML limpio. Esto es esencial para que los CMS (WordPress, Astro, Hugo) procesen correctamente los metadatos de la página.

```yaml
---
titulo: "Título Atractivo y Click-bait (H1)"
slug: /url-amigable-corta/
meta_title: "Título SEO optimizado (Max 60 caracteres)"
meta_description: "Descripción persuasiva que incluya la keyword principal (Max 155 caracteres)."
keywords: [keyword principal, keyword secundaria, long tail]
categoria: "Categoría del Blog"
---
```

## 2. Bloque AEO (Answer Engine Optimization)
**Propósito:** Ser citado directamente por IAs como ChatGPT o Google AI Overviews cuando un usuario hace una pregunta directa.
**Reglas:**
- Debe estar inmediatamente después del título/frontmatter.
- Lenguaje 100% factual, neutral y directo (cero "fluff" o lenguaje comercial).
- Debe responder el **"Qué", "Quién", "Cómo" o "Cuánto"** en 2-3 líneas máximo.

```markdown
<!-- AEO-SUMMARY-START -->
> El servicio de arriendo One-Way permite retirar un vehículo en una ciudad y devolverlo en otra distinta dentro de Chile. Este servicio incluye un recargo logístico de drop-off que se calcula automáticamente según la distancia en kilómetros entre ambas sucursales.
<!-- AEO-SUMMARY-END -->
```

## 3. Navegación Interna (GEO & Experiencia de Usuario)
Los motores de IA usan los enlaces ancla para entender la estructura jerárquica y generar resúmenes estructurados.

```markdown
### Tabla de Contenidos
1. <a href="#que-es">¿Qué es el servicio?</a>
2. <a href="#como-funciona">¿Cómo funciona paso a paso?</a>
3. <a href="#precios">Precios y Tarifas</a>
```

## 4. Estructura de Encabezados (Jerarquía HTML)
**Propósito:** Facilitar el parseo del contenido.
**Reglas:**
- Solo un H1 por página (generalmente inyectado por el CMS usando el `titulo` del frontmatter).
- Los H2 deben tener IDs explícitos (slugificados) que coincidan con la Tabla de Contenidos.
- Usar palabras clave transaccionales o informativas en los H2.

```markdown
<h2 id="como-funciona">¿Cómo funciona paso a paso?</h2>
```

## 5. Formateo de Datos Nativos (GEO - Generative Engine Optimization)
A las IAs (como Perplexity o Gemini) les cuesta procesar "muros de texto". Prefieren datos estructurados visualmente.

**Reemplaza párrafos largos con:**
1. **Listas Markdown:** Para pasos secuenciales, checklists o requisitos.
2. **Tablas Markdown:** Para comparar precios, categorías, distancias o características.
3. **Negritas:** Para resaltar entidades nombradas (nombres de marcas, ubicaciones, métricas exactas).

```markdown
| Categoría | Precio Base | Capacidad | Recomendado para |
| :--- | :--- | :--- | :--- |
| SUV 4x2 | $45.000 / día | 5 Pasajeros | Ciudad y carretera |
| Camioneta 4x4 | $65.000 / día | 5 Pasajeros | Caminos rurales (Ej: Carretera Austral) |
```

## 6. Enlazado Interno (Flujo de Autoridad)
**Propósito:** Distribuir el *Link Juice* y mantener al usuario/crawler en tu ecosistema.
- Se deben incluir al menos **2 enlaces internos** hacia otros artículos pilar o páginas de producto.
- El *anchor text* debe ser descriptivo (nunca "haz clic aquí").

```markdown
[LINK INTERNO SUGERIDO: "Conoce más sobre nuestros seguros y coberturas" -> /seguros-y-coberturas/]
```

## 7. Schema JSON-LD (El "Motor" Oculto)
**Propósito:** Entregar la data pre-digerida a los bots de Google en su idioma nativo. Esto desbloquea "Rich Snippets" (estrellas, FAQs desplegables, carruseles).
**Reglas:**
- Todo debe ir dentro de una etiqueta `<script type="application/ld+json">`.
- Usar un `@graph` para agrupar múltiples schemas (Article, FAQPage, BreadcrumbList) sin crear conflictos.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "Título del Artículo",
      "inLanguage": "es-CL",
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://tusitio.com/url-del-articulo/"
      },
      "image": "https://tusitio.com/imagen.jpg",
      "publisher": {
        "@type": "Organization",
        "name": "Nombre Marca",
        "logo": {
          "@type": "ImageObject",
          "url": "https://tusitio.com/logo.png"
        }
      }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "¿Pregunta frecuente 1?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Respuesta directa y clara."
          }
        }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Inicio",
          "item": "https://tusitio.com/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "https://tusitio.com/blog/"
        }
      ]
    }
  ]
}
</script>
```

---

### Resumen del Flujo de Lectura del Bot/IA:
1. Lee el YAML para entender la **metadata**.
2. Lee el `AEO-SUMMARY` para extraer la **respuesta rápida** a la intención de búsqueda.
3. Lee el `BreadcrumbList` y el HTML para entender la **arquitectura**.
4. Lee las `Tablas/Listas` para usar como datos **citables**.
5. Lee el `@graph` JSON-LD para validar todo lo anterior y decidir si **mereces el Rich Snippet**.
