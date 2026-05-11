import os

filepath = r'c:\Antigravity_2026\InMedios_Mitta\geo-seo-claude\scripts\generate_pdf_report.py'
with open(filepath, 'r', encoding='utf-8') as f:
    code = f.read()

replacements = {
    '"Example Company"': '"Empresa de Ejemplo"',
    '"This report presents the findings of a comprehensive GEO audit "': '"Este informe presenta los hallazgos de una auditoría GEO exhaustiva "',
    '"conducted on Example Company (https://example.com). The site achieved "': '"realizada a Empresa de Ejemplo (https://example.com). El sitio obtuvo "',
    '"an overall GEO Readiness Score of 58/100, placing it in the Moderate tier. "': '"una puntuación general de Preparación GEO de 58/100, ubicándolo en la categoría Moderado. "',
    '"The strongest area is Content Quality (70/100), while Structured Data (30/100) "': '"El área más fuerte es Calidad de Contenido (70/100), mientras que Datos Estructurados (30/100) "',
    '"represents the biggest opportunity for improvement. Implementing schema markup, "': '"representa la mayor oportunidad de mejora. Implementar el marcado schema, "',
    '"allowing AI crawlers, and optimizing content structure could increase the score "': '"permitir rastreadores de IA y optimizar la estructura del contenido podría aumentar el puntaje "',
    '"to approximately 78/100 within 90 days."': '"a aproximadamente 78/100 dentro de 90 días."',
    '"No Schema Markup Detected"': '"No se Detectó Marcado Schema"',
    '"The site has no JSON-LD structured data, making it difficult for AI models to understand entity relationships."': '"El sitio no tiene datos estructurados JSON-LD, lo que dificulta que los modelos de IA entiendan las relaciones de la entidad."',
    '"JavaScript-Only Rendering"': '"Renderizado Exclusivo con JavaScript"',
    '"Key content pages use client-side rendering, making them invisible to AI crawlers that don\'t execute JavaScript."': '"Las páginas de contenido clave utilizan renderizado del lado del cliente, haciéndolas invisibles para los rastreadores de IA que no ejecutan JavaScript."',
    '"Missing llms.txt"': '"Falta archivo llms.txt"',
    '"No llms.txt file exists to guide AI systems to the most important content."': '"No existe un archivo llms.txt para guiar a los sistemas de IA al contenido más importante."',
    '"Weak Brand Entity Presence"': '"Presencia de Entidad de Marca Débil"',
    '"Brand is not present on Wikipedia or Wikidata, limiting entity recognition by AI models."': '"La marca no está presente en Wikipedia o Wikidata, limitando el reconocimiento de la entidad por parte de los modelos de IA."',
    '"Content Not Optimized for Citability"': '"Contenido No Optimizado para Citabilidad"',
    '"Most content blocks are either too short or too long for optimal AI citation (target: 134-167 words)."': '"La mayoría de los bloques de contenido son demasiado cortos o demasiado largos para una citación óptima de IA (objetivo: 134-167 palabras)."',
    '"Allow all Tier 1 AI crawlers in robots.txt"': '"Permitir todos los rastreadores de IA de Nivel 1 en robots.txt"',
    '"Add publication dates to all content pages"': '"Agregar fechas de publicación a todas las páginas de contenido"',
    '"Create llms.txt file with key page references"': '"Crear archivo llms.txt con referencias clave de páginas"',
    '"Add author bylines with credentials"': '"Agregar firmas de autor con credenciales"',
    '"Fix meta descriptions on top 10 pages"': '"Corregir meta descripciones en las 10 páginas principales"',
    '"Implement Organization schema with sameAs linking"': '"Implementar esquema Organization con enlaces sameAs"',
    '"Add Article + Person schema to all blog posts"': '"Agregar esquema Article + Person a todas las entradas del blog"',
    '"Restructure content with question-based H2 headings"': '"Reestructurar contenido con encabezados H2 basados en preguntas"',
    '"Optimize content blocks for 134-167 word citability"': '"Optimizar bloques de contenido para citabilidad de 134-167 palabras"',
    '"Implement server-side rendering for content pages"': '"Implementar renderizado del lado del servidor para páginas de contenido"',
    '"Build Wikipedia/Wikidata entity presence"': '"Construir presencia de entidad en Wikipedia/Wikidata"',
    '"Develop Reddit community engagement strategy"': '"Desarrollar estrategia de participación en comunidades de Reddit"',
    '"Create YouTube content aligned with AI search queries"': '"Crear contenido de YouTube alineado con consultas de búsqueda de IA"',
    '"Establish original research publication program"': '"Establecer programa de publicación de investigación original"',
    '"Build comprehensive topical authority content clusters"': '"Construir clústeres de contenido completos para autoridad temática"',
    '"Allowed"': '"Permitido"',
    '"Blocked"': '"Bloqueado"',
    '"Keep allowed"': '"Mantener permitido"',
    '"Unblock for visibility"': '"Desbloquear para mayor visibilidad"',
    'f"Report generated: {result}"': 'f"Reporte generado: {result}"',
    '"ERROR: stdin input exceeds 10 MB limit"': '"ERROR: la entrada stdin excede el límite de 10 MB"',
}

for eng, esp in replacements.items():
    code = code.replace(eng, esp)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(code)
print("done")
