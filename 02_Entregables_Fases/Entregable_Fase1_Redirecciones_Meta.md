# Ticket Técnico #DEV-01: Corrección de Redirecciones y Metadatos
**Cliente:** Mitta
**Agencia Consultora:** InMedios
**Fecha de Auditoría:** Abril 2026
**Prioridad:** ALTA

---

## 1. Corrección de Cadena de Redirección en Root Domain

### Diagnóstico Actual
Actualmente, cuando un usuario o bot ingresa al dominio raíz (`mitta.cl`), el servidor está ejecutando un rebote ineficiente en dos pasos que degrada el tiempo de carga (LCP) y desperdicia *Crawl Budget*:
1. `https://mitta.cl` ➔ Redirección Temporal (307)
2. `https://mitta.cl/rent-a-car-personas` ➔ Redirección Permanente (308)
3. `https://mitta.cl/rent-a-car-personas/` ➔ OK (200)

**Tiempo de pérdida medido:** ~1.4 segundos solo en redirecciones.

### Acción Requerida
Consolidar el enrutamiento a un único salto mediante una **redirección 301 (Permanente)** desde el dominio raíz hacia la URL final con el *trailing slash* (`/`).

### Implementación Sugerida (Ejemplos por Servidor)

Si utilizan **Nginx**:
```nginx
server {
    listen 80;
    listen 443 ssl;
    server_name mitta.cl www.mitta.cl;

    # Redirección directa de raíz a la subcarpeta final
    location = / {
        return 301 https://mitta.cl/rent-a-car-personas/;
    }
    
    # Manejo de trailing slash para evitar saltos 308
    rewrite ^(.*[^/])$ $1/ permanent;
}
```

Si utilizan **Apache / .htaccess**:
```apache
RewriteEngine On
# Redirigir el index raíz directamente a la carpeta final
RewriteRule ^/?$ https://mitta.cl/rent-a-car-personas/ [R=301,L]

# Forzar trailing slash (evita el salto 308)
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_URI} !(.*)/$
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1/ [L,R=301]
```

---

## 2. Estandarización de Metadatos Sociales (OpenGraph & Twitter Cards)

### Diagnóstico Actual
La auditoría de la URL final `https://mitta.cl/rent-a-car-personas/` arrojó errores de sintaxis que penalizan el despliegue del contenido al ser compartido en redes y aplicaciones de mensajería (WhatsApp, LinkedIn, Twitter).
- 🔴 Ausencia del campo obligatorio `og:type` (invalida el protocolo).
- 🟡 `og:title` excede el límite recomendado de 60 caracteres (actual: 64).
- 🟡 Ausencia de dimensiones de imagen, lo que retrasa el renderizado en aplicaciones móviles.

### Acción Requerida
Reemplazar el bloque actual en el `<head>` del HTML por el siguiente bloque optimizado.

### Bloque HTML Optimizado para Copiar y Pegar

```html
<!-- Open Graph optimizado por InMedios -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mitta">
<meta property="og:title" content="Rent a Car | Arriendo de Autos para Personas y Empresas">
<meta property="og:description" content="Reserva tu auto con MITTA Rent a Car en Chile: flota moderna, beneficios exclusivos como acumulación LATAM Pass y descuentos. ¡Arrienda online fácil y rápido!">
<meta property="og:url" content="https://mitta.cl/rent-a-car-personas/">
<meta property="og:locale" content="es_CL">
<meta property="og:image" content="https://admin.mitta.cl/https://d3i52tl7vwsowh.cloudfront.net/media/original_images/original_imagesecomitta.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Mitta Rent a Car Flota">

<!-- Twitter Card optimizado por InMedios -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Rent a Car | Arriendo de Autos para Personas y Empresas">
<meta name="twitter:description" content="Reserva tu auto con MITTA Rent a Car en Chile: flota moderna, beneficios exclusivos como acumulación LATAM Pass y descuentos. ¡Arrienda online fácil y rápido!">
<meta name="twitter:image" content="https://admin.mitta.cl/https://d3i52tl7vwsowh.cloudfront.net/media/original_images/original_imagesecomitta.png">
<meta name="twitter:image:alt" content="Mitta Rent a Car Flota">
```

> **Nota para QA:** Tras implementar este cambio, el Warning de `og:title` desaparecerá al haber sido reducido a 55 caracteres, y la renderización en WhatsApp será instantánea al especificar las dimensiones 1200x630.
