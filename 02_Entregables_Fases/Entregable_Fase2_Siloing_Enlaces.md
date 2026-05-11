# Ticket Técnico #DEV-02 y #CONT-01: Siloing SEO y Anchor Texts
**Cliente:** Mitta
**Agencia Consultora:** InMedios
**Fecha de Auditoría:** Abril 2026
**Prioridad:** MEDIA-ALTA (Afecta Flujo Transaccional)

---

## 1. Rescate de Páginas Huérfanas (Orphan Pages)

### Diagnóstico Actual
La auditoría de rastreo detectó **19 páginas huérfanas** (páginas con 0 enlaces internos apuntando hacia ellas). Para Google y para los motores de IA (ChatGPT, Claude), si una página no recibe enlaces internos, se considera contenido "sin importancia" y frecuentemente es desindexado.

La mayoría de estas páginas huérfanas son artículos clave del blog que deberían estar captando tráfico informacional para empujarlo hacia la venta (Leasing y Renting).

**Ejemplo de Páginas Críticas Aisladas:**
1. `/blog/que-es-el-renting-de-vehiculos/`
2. `/blog/renting-de-autos-0km-con-un-plan-flexible-en-chile/`
3. `/blog/leasing-operativo-ideal-para-la-gestin-de-transporte-en-empresas/`
4. `/rent-a-car-personas/latampass-arrienda-y-vuela/`

### Plan de Acción Requerido (Siloing)
El equipo de Contenidos/Desarrollo debe implementar las siguientes reconexiones para restaurar el flujo de autoridad (Link Juice):

**A. Inyección de Enlaces de Rescate (Hacia los artículos):**
- Agregar un enlace hacia `/blog/que-es-el-renting-de-vehiculos/` desde la página principal de `/renting-mittago/` (Ejemplo de texto: *"¿Dudas sobre cómo funciona? Lee nuestra guía de Renting"*).
- Agregar un bloque de "Artículos Relacionados" al final de `/leasing-operativo/` que enlace hacia los artículos huérfanos de Leasing.

**B. Flujo Transaccional (Desde los artículos hacia la venta):**
- Ingresar al editor de WordPress/CMS de los 19 artículos huérfanos y asegurar que dentro del primer párrafo exista un **enlace directo y en negrita** hacia la landing comercial correspondiente (`/renting-mittago/` o `/leasing-operativo/`).

---

## 2. Optimización de Anchor Texts Ciegos

### Diagnóstico Actual
Nuestros scripts detectaron **33 enlaces estructurales** (en botones, menús o imágenes) que no poseen "Anchor Text" (texto ancla) o atributos legibles.
Cuando un enlace no tiene texto (por ejemplo, un botón que solo tiene un ícono o una imagen sin atributo `alt`), los motores de búsqueda no pueden entender de qué trata la página destino, perdiendo oportunidad de rankeo semántico.

### Acción Requerida (Código)
El equipo de Desarrollo Front-End debe auditar los botones de llamada a la acción (CTAs) y los banners de imagen, asegurando que todos cumplan el siguiente estándar HTML:

**❌ Código Incorrecto (Actual detectado):**
```html
<!-- Enlace en imagen sin atributo ALT -->
<a href="/leasing-operativo/">
    <img src="banner-leasing.jpg">
</a>

<!-- Botón ciego -->
<a href="/rent-a-car-personas/cotizar/" class="btn-primary"></a>
```

**✅ Código Optimizado (Estándar InMedios):**
```html
<!-- Enlace en imagen con ALT descriptivo (El ALT actúa como Anchor Text) -->
<a href="/leasing-operativo/">
    <img src="banner-leasing.jpg" alt="Cotizar Leasing Operativo Corporativo Mitta">
</a>

<!-- Botón con atributo Title en caso de no llevar texto visible -->
<a href="/rent-a-car-personas/cotizar/" class="btn-primary" title="Cotizar Rent a Car para Personas">
    <span class="sr-only">Cotizar Arriendo de Auto</span>
    <i class="icon-car"></i>
</a>
```

> **Directriz de Palabras Clave:** Al aplicar los atributos `title` o `alt`, no usen textos genéricos como "Haga clic aquí" o "Ver más". Utilicen Keywords exactas: "Leasing Operativo", "Renting 0KM", "Rent a Car Santiago".
