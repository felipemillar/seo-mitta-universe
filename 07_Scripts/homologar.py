import os
import re
import json

DIR_MGO = "/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta/02_Contenidos_Redactados/MittaGO"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

for filename in os.listdir(DIR_MGO):
    if not filename.endswith("_v2.md"):
        continue

    filepath = os.path.join(DIR_MGO, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Frontmatter: remove ```yaml and ```
    content = re.sub(r'^```yaml\n---\n(.*?)\n---\n```\n', r'---\n\1\n---\n', content, flags=re.DOTALL)

    # 2. Extract YAML properties to use later
    yaml_match = re.search(r'^---\n(.*?)\n---', content, flags=re.DOTALL)
    yaml_text = yaml_match.group(1) if yaml_match else ""
    
    slug = ""
    title = ""
    for line in yaml_text.split('\n'):
        if line.startswith('slug:'):
            slug = line.split('slug:')[1].strip()
        elif line.startswith('titulo:') or line.startswith('meta_title:'):
            if not title: # prefer titulo if it exists, fallback to meta_title
                title = line.split(':', 1)[1].strip().strip('"').strip("'")

    # 3. AEO Answer Block
    content = content.replace('> <!-- AEO-SUMMARY-START -->', '<!-- AEO-SUMMARY-START -->')
    content = content.replace('> <!-- AEO-SUMMARY-END -->', '<!-- AEO-SUMMARY-END -->')

    # 4 & 5. Table of contents and Headings
    # MittaGO TOC: ## Contenido\n- [Paso a paso para elegir el modelo correcto](#elegir-modelo)
    content = content.replace('## Contenido', '### Tabla de Contenidos')
    
    # We will let the TOC list as standard markdown, or we can replace it.
    # To keep it safe, let's leave TOC as a markdown list (it's perfectly fine for rendering).
    # But let's fix Headings. Many MittaGO headings are `## Title` or `<h2 id="...">Title</h2>`.
    # Let's ensure H2s have IDs if they are markdown.
    # Let's write a simple replacement for markdown headings to HTML headings, but only if they don't have IDs.
    
    def heading_replacer(match):
        level = len(match.group(1))
        if level == 2:
            heading_text = match.group(2).strip()
            heading_id = slugify(heading_text)
            return f'<h2 id="{heading_id}">{heading_text}</h2>'
        return match.group(0)

    # Replace markdown h2s with html h2s
    content = re.sub(r'^(##)\s+(.+)$', heading_replacer, content, flags=re.MULTILINE)

    # 6. JSON-LD Schemas
    # Find all ```json blocks
    json_blocks = re.findall(r'```json\n(.*?)\n```', content, flags=re.DOTALL)
    
    if json_blocks:
        # Remove old json blocks
        content = re.sub(r'```json\n.*?\n```\n?', '', content, flags=re.DOTALL)
        
        graph_items = []
        has_article = False
        
        for jb in json_blocks:
            try:
                obj = json.loads(jb)
                if "@context" in obj:
                    del obj["@context"]
                
                if obj.get("@type") == "Article":
                    has_article = True
                    # Add missing fields
                    obj["inLanguage"] = "es-CL"
                    
                    if "mainEntityOfPage" in obj and isinstance(obj["mainEntityOfPage"], str):
                        obj["mainEntityOfPage"] = {
                            "@type": "WebPage",
                            "@id": obj["mainEntityOfPage"]
                        }
                    elif "mainEntityOfPage" not in obj:
                        obj["mainEntityOfPage"] = {
                            "@type": "WebPage",
                            "@id": f"https://mitta.cl/blog{slug}" if slug else "https://mitta.cl/"
                        }
                    
                    if "image" not in obj:
                        obj["image"] = "https://www.mitta.cl/images/default.png"
                        
                    if "publisher" in obj and "logo" not in obj["publisher"]:
                        obj["publisher"]["logo"] = {
                            "@type": "ImageObject",
                            "url": "https://mitta.cl/logo.png"
                        }
                
                graph_items.append(obj)
            except Exception as e:
                print(f"Error parsing JSON in {filename}: {e}")
        
        # Add BreadcrumbList
        breadcrumb = {
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
                    "name": title,
                    "item": f"https://mitta.cl/blog{slug}" if slug else ""
                }
            ]
        }
        graph_items.append(breadcrumb)

        schema = {
            "@context": "https://schema.org",
            "@graph": graph_items
        }

        schema_str = json.dumps(schema, indent=2, ensure_ascii=False)
        # Format the script tag exactly
        script_tag = f'<script type="application/ld+json">\n{schema_str}\n</script>\n'
        
        content = content.strip() + "\n\n---\n" + script_tag

    # 7. Cross-links
    # Find enlaces_salientes in YAML
    links = []
    in_links = False
    for line in yaml_text.split('\n'):
        if line.startswith('enlaces_salientes:'):
            in_links = True
            continue
        if in_links:
            if line.startswith('  -'):
                link = line.split('-')[1].strip()
                links.append(link)
            elif not line.startswith(' ') and line.strip() != '':
                in_links = False
                
    if links and "LINK INTERNO SUGERIDO" not in content:
        link_str = "\n".join([f'[LINK INTERNO SUGERIDO: "Revisa más detalles aquí" -> {l}]' for l in links])
        # Inject before the first horizontal rule at the bottom, or just before the schema
        if '<script type="application/ld+json">' in content:
            content = content.replace('<script type="application/ld+json">', f'{link_str}\n\n<script type="application/ld+json">')

    # Save modified content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Homologation completed successfully!")
