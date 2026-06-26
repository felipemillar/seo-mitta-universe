# Ticket Técnico #DEV-03: Datos Estructurados (Schema) e Identidad Semántica
**Cliente:** Mitta
**Agencia Consultora:** InMedios
**Fecha de Auditoría:** Abril 2026
**Prioridad:** CRÍTICA (Afecta Knowledge Graph e IA)

---

## 1. Diagnóstico de Entidades SEO (Entity Gap)

Actualmente, el sitio web `mitta.cl` carece por completo de marcado de datos estructurados (Schema.org) a nivel de la organización. 

Para los motores de búsqueda modernos y los modelos generativos de IA (LLMs), **si no hay código JSON-LD, la empresa "no existe" como entidad verificable**. 

La auditoría reveló que Mitta sí posee una entrada en **Wikipedia** (`en.wikipedia.org/wiki/Mitta`) y en **Wikidata** (`Q132544705`), pero la página web corporativa no está conectada a estas fuentes de autoridad. Esto está impidiendo que Google despliegue el "Panel de Conocimiento" (Knowledge Graph) al lado derecho de los resultados de búsqueda cuando los usuarios buscan la marca.

---

## 2. Acción Requerida (Código JSON-LD)

El equipo de Desarrollo Front-End debe inyectar el siguiente bloque de código en formato `<script type="application/ld+json">` dentro de la etiqueta `<head>` de **todas las páginas del dominio principal**.

Este script contiene la propiedad `sameAs` obligatoria que forzará a los crawlers a vincular la identidad corporativa de la página web con sus perfiles enciclopédicos y sociales.

### Bloque JSON-LD Optimizado para Copiar y Pegar

```html
<!-- Schema.org Organization inyectado por InMedios -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Mitta Rent a Car",
  "alternateName": "Mitta",
  "url": "https://mitta.cl/",
  "logo": "https://admin.mitta.cl/https://d3i52tl7vwsowh.cloudfront.net/media/original_images/original_imagesecomitta.png",
  "description": "Líder en Rent a Car para personas, arriendo de flotas para empresas y leasing operativo en Chile con respaldo de Mitsui & Co.",
  "sameAs": [
    "https://en.wikipedia.org/wiki/Mitta",
    "https://www.wikidata.org/wiki/Q132544705",
    "https://www.linkedin.com/company/mitta-rent-a-car-y-leasing-operativo/",
    "https://www.instagram.com/mitta.chile",
    "https://www.facebook.com/MittaRentACar/"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+56-2-2345-6789", 
    "contactType": "customer service",
    "areaServed": "CL",
    "availableLanguage": "Spanish"
  }
}
</script>
```

> **Instrucción de Calidad (QA):**
> Una vez que este script sea subido a producción (idealmente vía Tag Manager o directo en el core), pueden verificar su correcto funcionamiento ingresando la URL a la herramienta oficial: [Validador de Schema de Google](https://validator.schema.org/). Debe devolver CERO errores de sintaxis.
