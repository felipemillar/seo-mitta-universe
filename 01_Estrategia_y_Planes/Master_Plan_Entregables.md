# Documento Maestro: Reestructuración y Estandarización de Entregables SEO

Este documento establece la línea base operativa y los requerimientos técnicos necesarios para la generación profesional de los entregables de la agencia, asegurando el estricto cumplimiento de la propuesta comercial y elevando el estándar corporativo frente a la gerencia del cliente.

---

## 1. Parámetros Contractuales y Alcance Operativo
Basado en las especificaciones de la propuesta comercial "SEO-2025-001":
*   **Presupuesto Asignado:** 25 horas cronológicas mensuales, estandarizadas operativamente bajo un modelo de gestión de 100 Créditos SEO (donde 1 crédito = 15 minutos de ejecución).
*   **Alcance del Ecosistema Digital:** 
    *   Dominio Principal: Mitta.
    *   Plataforma de Renting: MittaGO.
    *   Plataforma Adicional: First.
*   **Entregables Obligatorios:** 
    1. Reporte Mensual de Rendimiento Integral.
    2. Reunión Mensual de Seguimiento y Planificación.

---

## 2. Capa Estructural: Adquisición de Datos e Infraestructura Técnica

Para garantizar la automatización, precisión y rigor técnico del Portal SEO mensual, es imperativo levantar y consolidar la siguiente **Capa Estructural**. Esto erradicará el trabajo manual esclavo y asegurará la obtención sistemática de los parámetros operativos:

### 2.1. Infraestructura de Analítica y Etiquetado (Data Analytics)
*   **Google Tag Manager (GTM):** 
    *   Implementación de un contenedor maestro con configuración de **Cross-Domain Tracking**. Esto es crítico para unificar el recorrido del usuario que navega entre `mitta.cl` y transacciona en `mittago.cl`.
*   **Google Analytics 4 (GA4):** 
    *   Configuración avanzada de Eventos de Conversión personalizados (ej. tracking de clics en "Cotizar Renting", envíos de formulario B2B).
    *   Requerimiento de extracción: Exportación vía API o CSV automatizado detallando Sesiones Orgánicas, Engagement Rate y Tasa de Rebote segmentada por dominio.
*   **Integración CRM (Feedback Requerido):** 
    *   Necesidad de conectar GA4 con el CRM del cliente (ej. Hubspot) para medir la calidad del lead orgánico (Closed-Won) y no únicamente el volumen de tráfico crudo.

### 2.2. Infraestructura de Herramientas SEO y Crawling (Técnica)
*   **Métricas de Autoridad (Ahrefs / Semrush):**
    *   Creación de *Campaigns* específicas en la herramienta para monitorear el *Share of Voice* frente a la competencia directa y trackeo automatizado de las 50 palabras clave transaccionales e industriales.
*   **Monitoreo Técnico y WPO (Web Performance):**
    *   **Automatización de Crawling:** Configuración de rastreos recurrentes en la nube (Screaming Frog Cloud o Sitebulb) para alertar sobre la generación de nuevos errores 404 de manera preventiva antes de fin de mes.
    *   **API de PageSpeed Insights:** Implementación de la API de Lighthouse para obtener extracciones reales y promedios móviles de LCP, CLS e INP semana a semana, eliminando la dependencia de la revisión manual en Search Console.

### 2.3. Infraestructura de Gestión Operativa (Workflow del Equipo)
*   **Estandarización en SharePoint:** 
    *   Creación de un árbol de directorios estricto como única fuente de verdad: `/01_Auditorias_Tecnicas`, `/02_Contenidos_Aprobados`, `/03_Reportes_Mensuales_Portal`.
*   **Sistema de Ticketing y Trazabilidad (Jira / Trello):** 
    *   Configuración de un tablero Kanban con campos personalizados obligatorios: `Responsable` (Gestión vs. Técnica), `Prioridad`, `Estado`, y fundamentalmente `Créditos SEO Consumidos`. Este tablero actuará como la base de datos que alimentará automáticamente el Nivel 3 del Portal de Entregables.
*   **Flujo de Derivación Técnica (Interacción con Desarrollo):**
    *   **Línea Lógica:** InMedios **no** interviene el código fuente del cliente. Toda anomalía estructural detectada (ej. LCP degradado, errores de servidor, optimización de imágenes) debe consolidarse en un **Informe de Tickets Detallado**. Este documento estructurado se entrega a la gerencia de Mitta, quien asume la responsabilidad de derivar las directrices operativas a su encargado de sitio (Agencia de TI / Desarrollo).

---

## 3. Arquitectura Estratégica: SEO Tradicional y Generative Engine Optimization (GEO)

Para asegurar la dominancia en los motores de búsqueda clásicos y la correcta asimilación por parte de las nuevas Inteligencias Artificiales (Search Generative Experience, Perplexity, ChatGPT), la infraestructura de la agencia debe cubrir estrictamente los siguientes parámetros:

### 3.1. Requerimientos para SEO Tradicional (Búsqueda Heurística)
*   **Rendimiento y Experiencia de Usuario (WPO):** 
    *   Exigencia técnica de mantener los Core Web Vitals en umbrales óptimos (LCP < 2.5s, CLS < 0.1). El código del sitio debe comprimir imágenes nativamente (formato WebP) y aplicar *Lazy Loading*.
*   **Arquitectura de Información (Siloing):** 
    *   Auditoría de *Interlinking* profundo. Las páginas informativas del blog deben transferir autoridad (*Link Juice*) directamente a las categorías transaccionales (Ej. De un artículo de "Electromovilidad" a la landing de "Renting de Autos Eléctricos").
*   **Perfil de Autoridad (Backlinks):** 
    *   Monitoreo estricto del perfil de enlaces para identificar menciones de alta autoridad en sectores industriales, mineros y logísticos que fortalezcan el *Domain Rating*.

### 3.2. Requerimientos para Generative Engine Optimization (GEO)
*   **Marcado Semántico Avanzado (Schema.org):** 
    *   Es mandatorio que el equipo de desarrollo implemente marcado estructurado tipo `Organization`, `Product`, `FAQPage`, y `Article`. Esto traduce el sitio a un lenguaje que los Large Language Models (LLMs) procesan sin ambigüedad.
*   **Modelado de Entidades (Entity SEO):** 
    *   Consolidación de la marca como una "Entidad de Conocimiento". El contenido debe forzar la asociación semántica de **Mitta** con la entidad "Continuidad Operacional B2B", y de **MittaGO** con "Renting Anti-Trámite B2C".
*   **Redacción Orientada a la Extracción (Featured Snippets):** 
    *   Todo Topic Cluster redactado por el equipo debe incluir párrafos introductorios de 40-50 palabras y listas HTML (`<ul>`/`<ol>`) diseñadas algorítmicamente para responder preguntas directas y adueñarse de la "Posición Cero".
*   **Control de Rastreo para IA (Robots.txt):** 
    *   Configuración de directivas específicas (como el bloqueo/permiso a `CCBot` o `GPTBot`) para asegurar que la IA se alimente exclusivamente de nuestro contenido estratégico de valor, evitando que rastree áreas privadas (carritos, portales de clientes) que puedan generar alucinaciones en las respuestas generadas.

---

## 4. Anexo A: Protocolo de Mejora Continua y Estandarización de Entregables Corporativos

En respuesta directa a las observaciones de la gerencia sobre la falta de planes de acción en los reportes previos y la caída en métricas clave, se establecen las siguientes normativas estructurales para la presentación de los resultados:

### 4.1. Segmentación de la Información por Perfil de Usuario
Todo entregable debe presentar una arquitectura de la información jerarquizada. La información técnica cruda no debe presentarse de primera línea a la gerencia. Se establece un modelo de visualización segmentado: 
*   **C-Level:** Acceso exclusivo a resúmenes ejecutivos y consolidación de métricas de negocio (Niveles 1 y 2 del Portal).
*   **TI / Implementadores:** Acceso al repositorio de datos crudos y anexos técnicos detallados, consolidado en un Informe de Tickets Detallado (Nivel 4).

### 4.2. Estandarización de Reportes Orientados a la Resolución (Accionabilidad)
Queda estrictamente prohibido emitir reportes de anomalías que no incluyan su correspondiente estrategia de mitigación. Todo hallazgo técnico o caída de métricas debe estructurarse metodológicamente:
*   **Diagnóstico:** Identificación de la métrica afectada (ej. Reducción del 15% en sesiones orgánicas).
*   **Análisis Causal:** Identificación técnica del origen (ej. Degradación del LCP a 4.5 segundos).
*   **Plan de Mitigación Inmediato:** Creación de ticket en el Informe Detallado para derivación a la agencia de desarrollo.

### 4.3. Consolidación de Métricas del Ecosistema Digital
Para demostrar un soporte integral, los reportes deben evidenciar el monitoreo constante de los tres dominios involucrados en el contrato. Se deben destacar los crecimientos aislados de plataformas satélites para balancear y contextualizar caídas estacionales en el dominio principal.

---

## 5. Dependencias Críticas (Feedback y Carencias Detectadas)

Para poder ejecutar la construcción de esta **Capa Estructural**, InMedios requiere el desbloqueo o confirmación de los siguientes puntos:

1.  **Accesos de Administración GTM / GA4:** ¿Contamos actualmente con los privilegios de Administrador requeridos para configurar el Cross-Domain Tracking y los eventos de conversión entre Mitta y MittaGO?
2.  **Presupuesto de Licencias SEO:** ¿La agencia dispone de licencias corporativas activas de herramientas como Screaming Frog o Ahrefs (nivel "Advanced") para conectar estas APIs, o el equipo (Hugo) continuará realizando extracciones manuales?
