# Ticket Técnico #DEV-06 y #CONT-02: Contenido y Hreflang
**Cliente:** Mitta
**Agencia Consultora:** InMedios
**Fecha de Auditoría:** Abril 2026
**Prioridad:** MEDIA

---

## 1. Optimización de Citabilidad de Contenido (Redacción)

### Diagnóstico Actual
La auditoría de legibilidad del contenido corporativo arrojó un score "Flesch" de **8.5**. Este nivel es considerado "Extremadamente Difícil (Post-Grado)". 
Para el SEO tradicional esto puede no ser grave, pero para **GEO (Generative Engine Optimization)** es fatal. Los modelos de lenguaje como ChatGPT y Claude prefieren citar párrafos cortos, concisos y con alta densidad de datos (Self-Containment).

**Problema Detectado:** El promedio actual es de **31 palabras por oración**.

### Acción Requerida (Equipo de Contenidos)
Reducir la complejidad sintáctica de los textos "Pilar" (Renting, Leasing, Home) siguiendo este estándar:
1. **Reducir oraciones:** El límite máximo debe ser **15-20 palabras por oración**. Usar puntos seguidos en lugar de comas y conectores largos.
2. **Evitar lenguaje de marketing vacío:** Eliminar oraciones como *"Soluciones de movilidad con más de 30.000 vehículos disponibles en Chile, asegurando flexibilidad y cobertura para cada tipo de viaje."*
3. **Reemplazar por Párrafos de Respuesta (Answer Blocks):** *"Mitta opera una flota de 30.000 vehículos en Chile. Proveemos cobertura nacional a través de 80 sucursales."*

---

## 2. Corrección de Etiquetas Hreflang (SEO Internacional)

### Diagnóstico Actual
Mitta tiene una versión en español y una en inglés (`/en/rent-a-car-individuals/`), y el mapeo `hreflang` básico existe. Sin embargo, faltan dos etiquetas críticas para cumplir con el estándar de Google:
- Falla Crítica: No hay etiqueta `self_reference` apuntando a la propia página.
- Falla Alta: No hay etiqueta `x-default` (necesaria para usuarios que llegan desde un idioma no definido).

### Acción Requerida (Código)
El equipo de desarrollo debe actualizar el bloque de etiquetas `<link rel="alternate" hreflang="...">` en el `<head>` del sitio, agregando el `x-default` apuntando a la versión en español, y asegurándose de que la página se referencie a sí misma.

**Bloque de Código HTML a Implementar (Ejemplo para el Home de Personas):**
```html
<!-- Enlaces hacia las versiones de idioma -->
<link rel="alternate" hreflang="es" href="https://mitta.cl/rent-a-car-personas/">
<link rel="alternate" hreflang="en" href="https://mitta.cl/en/rent-a-car-individuals/">

<!-- Etiqueta X-Default (Faltante) apuntando a la versión principal -->
<link rel="alternate" hreflang="x-default" href="https://mitta.cl/rent-a-car-personas/">
```
