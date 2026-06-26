import os
import re
import json

WORKSPACE = "/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta"
BORRADORES_DIR = os.path.join(WORKSPACE, "InMedios_Mitta/02_Contenidos_Redactados/Nuevos_Contenidos_2026/borradores")

def slugify(text):
    text = text.lower()
    text = text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def clean_tag(text):
    # Remover tags html y emojis comunes de inicio para el ID del H2
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'^[0-9️\ufe0f\s🔹🚗💸🔧📉📊🔄🚀👉✔\-—\)\.]+', '', text)
    return text.strip()

def generate_aeo_summary(body_text, title):
    paragraphs = [p.strip() for p in body_text.split('\n\n') if p.strip()]
    
    desc_p = ""
    for p in paragraphs:
        if len(p) > 100 and not p.startswith('#') and not p.startswith('<') and not p.startswith('!') and not p.startswith('>'):
            desc_p = p
            break
            
    if not desc_p and paragraphs:
        desc_p = paragraphs[0]
        
    desc_p = clean_tag(desc_p)
    sentences = desc_p.split('.')
    summary_sentences = []
    char_count = 0
    for s in sentences:
        s_clean = s.strip()
        if not s_clean:
            continue
        summary_sentences.append(s_clean)
        char_count += len(s_clean)
        if char_count > 160 or len(summary_sentences) >= 2:
            break
            
    summary = ". ".join(summary_sentences) + "."
    return summary

def optimize_article(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    frontmatter = {}
    fm_match = re.search(r'^---\n(.*?)\n---', content, flags=re.DOTALL)
    if not fm_match:
        print(f"  [ERROR] No frontmatter found in {os.path.basename(file_path)}")
        return
        
    fm_text = fm_match.group(1)
    for line in fm_text.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            frontmatter[k.strip()] = v.strip().strip('"').strip("'")
            
    body = content[fm_match.end():].strip()
    
    # Limpiar elementos previos autogenerados para evitar duplicidades en re-corrida
    body = re.sub(r'<script type="application/ld+json">.*?</script>', '', body, flags=re.DOTALL).strip()
    body = re.sub(r'<!-- AEO-SUMMARY-START -->.*?<!-- AEO-SUMMARY-END -->\n*', '', body, flags=re.DOTALL).strip()
    body = re.sub(r'### Tabla de Contenidos.*?</ul>\n*', '', body, flags=re.DOTALL).strip()
    # Limpiar tablas autogeneradas previamente para no duplicarlas
    body = re.sub(r'### Resumen de Gastos Anuales Estimados de un Auto en Chile.*?(\n\n|\Z)', '', body, flags=re.DOTALL).strip()
    body = re.sub(r'### Comparativa de Coberturas de Seguro de Arriendo.*?(\n\n|\Z)', '', body, flags=re.DOTALL).strip()
    body = re.sub(r'\[LINK INTERNO SUGERIDO:.*?\]', '', body).strip()

    # Normalizar títulos numerados y secciones del tipo "1. Introducción" o "1️ Precio real..." o "Conclusión" a H2 HTML
    paragraphs = body.split('\n\n')
    new_paras = []
    toc_links = []
    
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
            
        is_heading = False
        heading_text = ""
        
        # 1. Comprobar si ya es un H2 HTML
        h2_html_match = re.match(r'^<h2 id="[^"]+">(.*?)</h2>$', p_clean, re.IGNORECASE)
        if h2_html_match:
            is_heading = True
            heading_text = h2_html_match.group(1)
            
        # 2. Comprobar H2 markdown (##)
        elif p_clean.startswith('## '):
            is_heading = True
            heading_text = p_clean[3:]
            
        # 3. Comprobar numerados del tipo "1. Introducción", "1) Introducción", "1️ Precio real..."
        elif re.match(r'^\d+[\.\)\ufe0f️\s]+\s*[A-ZÁÉÍÓÚ]', p_clean) and len(p_clean) < 100:
            is_heading = True
            heading_text = p_clean
            
        # 4. Comprobar secciones sin número como "Conclusión" o "Introducción" solas
        elif p_clean.upper() in ["CONCLUSIÓN", "CONCLUSION", "INTRODUCCIÓN", "INTRODUCCION", "CTA FINAL"]:
            is_heading = True
            heading_text = p_clean
            
        if is_heading:
            clean_t = clean_tag(heading_text)
            if clean_t.upper() not in ["TABLA DE CONTENIDOS", "CTA FINAL", "CTA"]:
                h_id = slugify(clean_t)
                p_new = f'<h2 id="{h_id}">{heading_text}</h2>'
                new_paras.append(p_new)
                toc_links.append(f'<li><a href="#{h_id}">{clean_t}</a></li>')
            else:
                new_paras.append(p_clean)
        else:
            new_paras.append(p_clean)
            
    new_body = "\n\n".join(new_paras)
    
    # 3. Insertar Tabla de Contenidos al inicio del cuerpo
    toc_html = ""
    if toc_links:
        toc_html = "### Tabla de Contenidos\n<ul>\n  " + "\n  ".join(toc_links) + "\n</ul>\n\n"
        
    # 4. Crear bloque AEO
    aeo_summary_val = generate_aeo_summary(new_body, frontmatter.get("titulo", ""))
    aeo_block = f"<!-- AEO-SUMMARY-START -->\n> {aeo_summary_val}\n<!-- AEO-SUMMARY-END -->\n\n"
    
    # 5. Estructurar tablas de datos si hay información comparable
    if "presupuesto" in file_path or "cuanto-cuesta" in file_path or "gastos-invisibles" in file_path:
        table_data = (
            "\n### Resumen de Gastos Anuales Estimados de un Auto en Chile\n\n"
            "| Concepto de Gasto | Costo Estimado (Anual) | Tipo de Gasto | ¿Cómo Optimizarlo con Suscripción? |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **Permiso de Circulación** | $120.000 - $450.000 | Fijo Obligatorio | Incluido en la cuota mensual |\n"
            "| **Seguro Automotriz (SOAP + Cobertura)** | $480.000 - $900.000 | Fijo Obligatorio | Incluido en la cuota mensual |\n"
            "| **Mantenciones Preventivas** | $300.000 - $600.000 | Variable Obligatorio | Incluido en la cuota mensual |\n"
            "| **Depreciación del Vehículo** | 15% - 20% valor/año | Costo Invisible | Cero riesgo (el auto no es tuyo) |\n"
            "| **Patentes y Trámites** | $50.000 - $100.000 | Fijo | Incluido y gestionado por la empresa |\n\n"
        )
        # Buscar el primer H2 para inyectar antes la tabla
        first_h2 = new_body.find('<h2')
        if first_h2 != -1:
            new_body = new_body[:first_h2] + table_data + new_body[first_h2:]
        else:
            new_body += "\n" + table_data
                
    elif "seguro" in file_path:
        table_data = (
            "\n### Comparativa de Coberturas de Seguro de Arriendo\n\n"
            "| Sigla de Cobertura | Nombre de Cobertura | ¿Qué Protege? | ¿Qué Excluye? |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| **CDW** | Collision Damage Waiver | Daños por colisión y choques básicos | Robo total y daños a terceros |\n"
            "| **LDW** | Loss Damage Waiver | Daños propios y pérdida total por robo | Negligencia grave del conductor |\n"
            "| **PAT** | Personal Accident Insurance | Lesiones personales del conductor e invitados | Daños materiales del auto |\n"
            "| **RC / RCE** | Responsabilidad Civil | Daños materiales y corporales a terceros | Daños al propio vehículo arrendado |\n\n"
        )
        first_h2 = new_body.find('<h2')
        if first_h2 != -1:
            new_body = new_body[:first_h2] + table_data + new_body[first_h2:]
        else:
            new_body += "\n" + table_data

    # 6. Inyectar enlaces internos cruzados (cross-links)
    marca = frontmatter.get("marca", "Mitta")
    if marca.lower() == "mittago":
        new_body += '\n\n[LINK INTERNO SUGERIDO: "Revisa los modelos y planes de suscripción de MittaGO" -> /modelos/]'
    else:
        new_body += '\n\n[LINK INTERNO SUGERIDO: "Cotiza tu rent a car en todo Chile con Mitta" -> /arriendo-de-autos/]'
            
    # 7. Generar Schema JSON-LD con @graph
    titulo = frontmatter.get("titulo", "")
    slug = frontmatter.get("slug", "")
    
    faq_items = []
    # Buscar patrones de preguntas/respuestas
    faq_matches = re.findall(r'class="faq-question">(.*?)</div>\s*<div class="faq-answer">(.*?)</div>', new_body, flags=re.DOTALL)
    if not faq_matches:
        faq_matches = re.findall(r'¿(.*?)\?\n\n(.*?)\n', new_body)
        
    for q, a in faq_matches[:3]:
        q_clean = clean_tag(q).strip()
        a_clean = clean_tag(a).strip()
        if q_clean and a_clean and len(a_clean) > 10:
            faq_items.append({
                "@type": "Question",
                "name": f"¿{q_clean}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a_clean
                }
            })
            
    graph_nodes = [
        {
            "@type": "Article",
            "headline": titulo,
            "inLanguage": "es-CL",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"https://mitta.cl{slug}"
            },
            "image": "https://mitta.cl/images/default.png",
            "publisher": {
                "@type": "Organization",
                "name": marca,
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://mitta.cl/logo.png"
                }
            }
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Inicio",
                    "item": "https://mitta.cl/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Blog",
                    "item": "https://mitta.cl/blog/"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": titulo,
                    "item": f"https://mitta.cl{slug}"
                }
            ]
        }
    ]
    
    if faq_items:
        graph_nodes.append({
            "@type": "FAQPage",
            "mainEntity": faq_items
        })
        
    schema_graph = {
        "@context": "https://schema.org",
        "@graph": graph_nodes
    }
    
    schema_str = json.dumps(schema_graph, indent=2, ensure_ascii=False)
    script_tag = f'\n\n<script type="application/ld+json">\n{schema_str}\n</script>\n'
    
    # 8. Re-ensamblar archivo
    optimized_content = "---\n"
    optimized_content += f"titulo: \"{frontmatter.get('titulo', '')}\"\n"
    optimized_content += f"pilar: \"{frontmatter.get('pilar', '')}\"\n"
    optimized_content += f"marca: \"{frontmatter.get('marca', '')}\"\n"
    optimized_content += f"meta_title: \"{frontmatter.get('meta_title', '')}\"\n"
    optimized_content += f"meta_description: \"{frontmatter.get('meta_description', '')}\"\n"
    optimized_content += f"keywords: \"{frontmatter.get('keywords', '')}\"\n"
    optimized_content += f"slug: \"{frontmatter.get('slug', '')}\"\n"
    optimized_content += "---\n\n"
    
    optimized_content += aeo_block
    optimized_content += toc_html
    optimized_content += new_body
    optimized_content += script_tag
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(optimized_content)
        
    print(f"  [OPTIMIZED] {os.path.basename(file_path)}")

def main():
    files = [f for f in os.listdir(BORRADORES_DIR) if f.endswith('.md')]
    print(f"Iniciando optimización SEO/GEO/AEO en {len(files)} archivos...")
    for f in sorted(files):
        optimize_article(os.path.join(BORRADORES_DIR, f))
    print("¡Optimización finalizada con éxito!")

if __name__ == "__main__":
    main()
