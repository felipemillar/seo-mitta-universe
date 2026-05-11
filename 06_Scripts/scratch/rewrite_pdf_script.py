# Script de traducción nativa
import os

filepath = r'c:\Antigravity_2026\InMedios_Mitta\geo-seo-claude\scripts\generate_pdf_report.py'
with open(filepath, 'r', encoding='utf-8') as f:
    code = f.read()

replacements = {
    'return "Excellent"': 'return "Excelente"',
    'return "Good"': 'return "Bueno"',
    'return "Moderate"': 'return "Moderado"',
    'return "Below Average"': 'return "Deficiente"',
    'return "Needs Attention"': 'return "Requiere Atención"',
    '"GEO Analysis Report"': '"Reporte de Análisis GEO"',
    '"Generative Engine Optimization Audit for <b>{brand_name}</b>"': '"Auditoría de Optimización para Motores Generativos de <b>{brand_name}</b>"',
    '"Website"': '"Sitio Web"',
    '"Analysis Date"': '"Fecha de Análisis"',
    '"GEO Score"': '"Puntuación GEO"',
    '"Executive Summary"': '"Resumen Ejecutivo"',
    '"This report presents the findings of a comprehensive Generative Engine Optimization (GEO) "': '"Este reporte presenta los hallazgos de una auditoría integral de Optimización para Motores Generativos (GEO) "',
    '"audit conducted on <b>{brand_name}</b> ({url}). The analysis evaluated the website\'s readiness "': '"realizada a <b>{brand_name}</b> ({url}). El análisis evaluó la preparación del sitio web "',
    '"for AI-powered search engines including Google AI Overviews, ChatGPT, Perplexity, Gemini, "': '"para motores de búsqueda impulsados por IA, incluyendo Google AI Overviews, ChatGPT, Perplexity, Gemini, "',
    '"and Bing Copilot. The overall GEO Readiness Score is <b>{geo_score}/100</b>, "': '"y Bing Copilot. La puntuación global de Preparación GEO es <b>{geo_score}/100</b>, "',
    '"placing the site in the <b>{get_score_label(geo_score)}</b> tier."': '"posicionando al sitio en la categoría <b>{get_score_label(geo_score)}</b>."',
    '"GEO Score Breakdown"': '"Desglose de Puntuación GEO"',
    '"Component", "Score", "Weight", "Weighted"': '"Componente", "Puntaje", "Peso", "Ponderado"',
    '"AI Citability & Visibility"': '"Citabilidad y Visibilidad IA"',
    '"Brand Authority Signals"': '"Señales de Autoridad de Marca"',
    '"Content Quality & E-E-A-T"': '"Calidad de Contenido y E-E-A-T"',
    '"Technical Foundations"': '"Bases Técnicas"',
    '"Structured Data"': '"Datos Estructurados"',
    '"Platform Optimization"': '"Optimización de Plataforma"',
    '"OVERALL"': '"GLOBAL"',
    '["Citability", "Brand", "Content", "Technical", "Schema", "Platform"]': '["Citabilidad", "Marca", "Contenido", "Técnico", "Schema", "Plataforma"]',
    '"AI Platform Readiness"': '"Disponibilidad en Plataformas IA"',
    '"These scores reflect how likely your content is to be cited by each AI search platform. "': '"Estos puntajes reflejan la probabilidad de que su contenido sea citado por cada plataforma de IA. "',
    '"A score below 50 indicates significant barriers to citation on that platform."': '"Un puntaje por debajo de 50 indica barreras significativas para la citación en esa plataforma."',
    '"AI Platform"': '"Plataforma IA"',
    '"AI Crawler Access Status"': '"Estado de Acceso de Rastreadores IA"',
    '"Blocking AI crawlers prevents AI platforms from citing your content. "': '"Bloquear los rastreadores de IA impide que las plataformas IA citen su contenido. "',
    '"The table below shows which AI crawlers can currently access your site."': '"La tabla a continuación muestra qué rastreadores pueden acceder a su sitio actualmente."',
    '"Crawler"': '"Rastreador"',
    '"Recommendation"': '"Recomendación"',
    '"<i>Run /geo crawlers to populate this section with AI crawler access data.</i>"': '"<i>Ejecute /geo crawlers para poblar esta sección con datos de acceso de rastreadores IA.</i>"',
    '"Key Findings"': '"Hallazgos Clave"',
    '"<i>Run a full /geo audit to populate findings.</i>"': '"<i>Ejecute una auditoría /geo completa para poblar los hallazgos.</i>"',
    '"Prioritized Action Plan"': '"Plan de Acción Priorizado"',
    '"Quick Wins (This Week)"': '"Victorias Rápidas (Esta Semana)"',
    '"High impact, low effort — can be implemented immediately."': '"Alto impacto, bajo esfuerzo — puede implementarse inmediatamente."',
    '"Medium-Term Improvements (This Month)"': '"Mejoras a Mediano Plazo (Este Mes)"',
    '"Significant impact, moderate effort — requires content or technical changes."': '"Impacto significativo, esfuerzo moderado — requiere cambios de contenido o técnicos."',
    '"Strategic Initiatives (This Quarter)"': '"Iniciativas Estratégicas (Este Trimestre)"',
    '"Long-term competitive advantage — requires ongoing investment."': '"Ventaja competitiva a largo plazo — requiere inversión continua."',
    '"Appendix: Methodology"': '"Anexo: Metodología"',
    '"This GEO audit was conducted on {date} analyzing {url}. "': '"Esta auditoría GEO se realizó el {date} analizando {url}. "',
    '"The analysis evaluated the website across six dimensions: AI Citability & Visibility (25%), "': '"El análisis evaluó el sitio web en seis dimensiones: Citabilidad y Visibilidad IA (25%), "',
    '"Brand Authority Signals (20%), Content Quality & E-E-A-T (20%), Technical Foundations (15%), "': '"Señales de Autoridad de Marca (20%), Calidad de Contenido y E-E-A-T (20%), Bases Técnicas (15%), "',
    '"Structured Data (10%), and Platform Optimization (10%)."': '"Datos Estructurados (10%), y Optimización de Plataforma (10%)."',
    '"<b>Platforms assessed:</b> Google AI Overviews, ChatGPT Web Search, Perplexity AI, "': '"<b>Plataformas evaluadas:</b> Google AI Overviews, ChatGPT Web Search, Perplexity AI, "',
    '"<b>Standards referenced:</b> Google Search Quality Rater Guidelines (Dec 2025), "': '"<b>Estándares de referencia:</b> Google Search Quality Rater Guidelines (Dic 2025), "',
    '"Schema.org specification, Core Web Vitals (2026 thresholds), "': '"Especificación de Schema.org, Core Web Vitals (umbrales 2026), "',
    '"llms.txt emerging standard, RSL 1.0 licensing framework"': '"estándar emergente llms.txt, marco de licenciamiento RSL 1.0"',
    '"Glossary"': '"Glosario"',
    '"Term", "Definition"': '"Término", "Definición"',
    '"Generative Engine Optimization — optimizing content for AI search citation"': '"Optimización para Motores Generativos — optimizar contenido para la citación de búsqueda IA"',
    '"AI Overviews — Google\'s AI-generated answer boxes in search results"': '"Vistas Generales de IA — cajas de respuesta generadas por IA de Google en los resultados"',
    '"Experience, Expertise, Authoritativeness, Trustworthiness"': '"Experiencia, Especialización, Autoridad, Confiabilidad"',
    '"Server-Side Rendering — generating HTML on the server for crawler access"': '"Renderizado del lado del servidor — generar HTML en el servidor para el acceso de los rastreadores"',
    '"Core Web Vitals — Google\'s page experience metrics (LCP, INP, CLS)"': '"Core Web Vitals — métricas de experiencia de página de Google (LCP, INP, CLS)"',
    '"Interaction to Next Paint — responsiveness metric (replaced FID March 2024)"': '"Interacción hasta el Siguiente Pintado — métrica de respuesta (reemplazó FID en marzo de 2024)"',
    '"JavaScript Object Notation for Linked Data — preferred structured data format"': '"Notación de Objetos de JavaScript para Datos Enlazados — formato de datos estructurados preferido"',
    '"Schema.org property linking an entity to its profiles on other platforms"': '"Propiedad de Schema.org que vincula una entidad a sus perfiles en otras plataformas"',
    '"Proposed standard file for guiding AI systems about site content"': '"Archivo estándar propuesto para guiar a los sistemas de IA sobre el contenido del sitio"',
    '"Protocol for instantly notifying search engines of content changes"': '"Protocolo para notificar instantáneamente a los motores de búsqueda sobre cambios de contenido"',
    '"This report was generated by the GEO-SEO Claude Code Analysis Tool. "': '"Este informe fue generado por el Motor de Análisis GEO-SEO de InMedios. "',
    '"Scores and recommendations are based on automated analysis and industry benchmarks. "': '"Las puntuaciones y recomendaciones se basan en análisis automatizados y puntos de referencia de la industria. "',
    '"Results should be validated with platform-specific testing."': '"Los resultados deben validarse con pruebas específicas de la plataforma."',
    'f"Page {doc.page}"': 'f"Página {doc.page}"',
    'f"Generated {datetime.now().strftime(\'%B %d, %Y\')}"': 'f"Generado el {datetime.now().strftime(\'%d-%m-%Y\')}"',
    '"Confidential"': '"Confidencial"',
    '"Unknown"': '"Desconocido"'
}

for eng, esp in replacements.items():
    code = code.replace(eng, esp)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(code)

print("Original script successfully modified to Spanish.")
