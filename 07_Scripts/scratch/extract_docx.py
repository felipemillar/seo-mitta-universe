import zipfile
import xml.etree.ElementTree as ET
import os
import re
import shutil

# Rutas del proyecto
WORKSPACE = "/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta"
DEST_ROOT = os.path.join(WORKSPACE, "InMedios_Mitta/02_Contenidos_Redactados/Nuevos_Contenidos_2026")
BORRADORES_DIR = os.path.join(DEST_ROOT, "borradores")
FINALES_DIR = os.path.join(DEST_ROOT, "finales")
ORIGINALES_DIR = os.path.join(DEST_ROOT, "docx_originales")

# Asegurar directorios limpios
shutil.rmtree(BORRADORES_DIR, ignore_errors=True)
os.makedirs(BORRADORES_DIR, exist_ok=True)
os.makedirs(FINALES_DIR, exist_ok=True)
os.makedirs(ORIGINALES_DIR, exist_ok=True)

def docx_to_paragraphs(docx_path):
    try:
        with zipfile.ZipFile(docx_path) as z:
            xml_content = z.read('word/document.xml')
            root = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            paragraphs = []
            for p in root.findall('.//w:p', ns):
                p_text = []
                for t in p.findall('.//w:t', ns):
                    if t.text:
                        p_text.append(t.text)
                text = "".join(p_text).strip()
                if text:
                    paragraphs.append(text)
            return paragraphs
    except Exception as e:
        print(f"Error leyendo {docx_path}: {e}")
        return []

def clean_title(title):
    title = title.replace('“', '').replace('”', '').replace('"', '').replace("'", "")
    title = re.sub(r'^(CONTENIDO|ARTÍCULO|ARTICULO)\s+\d+[:—\-]?\s*', '', title, flags=re.IGNORECASE)
    return title.strip()

def slugify(text):
    text = text.lower()
    text = text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# --- PARSERS ESPECÍFICOS ---

def parse_mittago_1(paragraphs):
    articles = []
    current_art = []
    
    for p in paragraphs:
        if p.strip().startswith("CONTENIDO "):
            if current_art:
                articles.append(current_art)
                current_art = []
        current_art.append(p)
    if current_art:
        articles.append(current_art)
        
    parsed = []
    for art in articles:
        meta = {"titulo": "", "pilar": "", "marca": "MittaGO", "meta_title": "", "meta_description": "", "keywords": "", "slug": ""}
        body = []
        i = 0
        in_body = False
        
        while i < len(art):
            line = art[i].strip()
            if in_body:
                if line.startswith("H1:"):
                    body.append(f"# {line[3:].strip()}")
                elif line.startswith("H2:"):
                    body.append(f"## {line[3:].strip()}")
                elif line.startswith("H3:"):
                    body.append(f"### {line[3:].strip()}")
                else:
                    body.append(line)
                i += 1
                continue
                
            if line.upper().startswith("CONTENIDO"):
                pass
            elif line.upper().startswith("PILAR"):
                parts = re.split(r'[:–-]', line, 1)
                meta["pilar"] = parts[1].strip() if len(parts) > 1 else line
            elif line.startswith("H1:"):
                meta["titulo"] = clean_title(line[3:])
            elif line.upper().startswith("SLUG:"):
                if i + 1 < len(art):
                    i += 1
                    meta["slug"] = art[i].strip().strip('/')
            elif line.upper().startswith("META DESCRIPTION:"):
                if i + 1 < len(art):
                    i += 1
                    meta["meta_description"] = art[i].strip().strip('"')
            elif line.upper().startswith("KEYWORD PRINCIPAL:"):
                if i + 1 < len(art):
                    i += 1
                    meta["keywords"] = art[i].strip()
            elif line.upper().startswith("KEYWORDS SECUNDARIAS:"):
                if i + 1 < len(art):
                    i += 1
                    meta["keywords"] += ", " + art[i].strip()
            elif line.upper() == "ARTÍCULO" or line.upper() == "ARTICULO":
                in_body = True
            else:
                in_body = True
                body.append(line)
            i += 1
            
        meta["meta_title"] = meta["titulo"]
        parsed.append((meta, "\n\n".join(body)))
    return parsed

def parse_mittago_2(paragraphs):
    articles = []
    current_art = []
    
    for p in paragraphs:
        if "ARTÍCULO " in p.upper() or "ARTICULO " in p.upper():
            if current_art:
                articles.append(current_art)
                current_art = []
        current_art.append(p)
    if current_art:
        articles.append(current_art)
        
    parsed = []
    for art in articles:
        meta = {"titulo": "", "pilar": "Finanzas y presupuesto", "marca": "MittaGO", "meta_title": "", "meta_description": "", "keywords": "costo tener auto, mittago, rent a car mensual, auto suscripcion chile", "slug": ""}
        body = []
        
        if len(art) > 1:
            meta["titulo"] = clean_title(art[1].strip())
            meta["meta_title"] = meta["titulo"]
            meta["slug"] = slugify(meta["titulo"])
            
            desc_candidates = [p for p in art[2:5] if len(p) > 50 and not p.startswith("📷")]
            if desc_candidates:
                meta["meta_description"] = desc_candidates[0][:155].strip()
                
            for line in art[2:]:
                if line.startswith("📷"):
                    match = re.search(r'\[(.*?)\]', line)
                    img_name = match.group(1) if match else "imagen"
                    body.append(f"![hero_image]({img_name})")
                elif line.startswith("👉") or line.startswith("✔"):
                    body.append(line)
                elif re.match(r'^\d+[\.\)\s]+\s*[A-Z]', line) or line.startswith("🚗") or line.startswith("💸") or line.startswith("🔧") or line.startswith("📉") or line.startswith("📊") or line.startswith("🔄") or line.startswith("🚀") or line.startswith("👉"):
                    body.append(f"## {line}")
                else:
                    body.append(line)
                    
        parsed.append((meta, "\n\n".join(body)))
    return parsed

def parse_mitta_febrero(paragraphs):
    articles = []
    current_art = []
    
    for p in paragraphs:
        if "CONTENIDO " in p.upper() and "FEBRERO 2026" in p.upper():
            if current_art:
                articles.append(current_art)
                current_art = []
        current_art.append(p)
    if current_art:
        articles.append(current_art)
        
    parsed = []
    for art in articles:
        meta = {"titulo": "", "pilar": "Rent a Car", "marca": "Mitta", "meta_title": "", "meta_description": "", "keywords": "", "slug": ""}
        body = []
        i = 0
        in_body = False
        cta = ""
        
        while i < len(art):
            line = art[i].strip()
            if in_body:
                if line.startswith("H1:"):
                    body.append(f"# {line[3:].strip()}")
                elif line.startswith("H2:"):
                    body.append(f"## {line[3:].strip()}")
                elif line.startswith("H3:"):
                    body.append(f"### {line[3:].strip()}")
                else:
                    body.append(line)
                i += 1
                continue
                
            if line.startswith("📅"):
                pass
            elif line.startswith("🔹 Título:") or line.startswith("🔹 Titulo:") or line.startswith("Título:") or line.startswith("Titulo:"):
                parts = line.split(':', 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(art):
                    i += 1
                    val = art[i].strip()
                meta["titulo"] = clean_title(val)
            elif line.upper().startswith("SLUG:"):
                parts = line.split(':', 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(art):
                    i += 1
                    val = art[i].strip()
                meta["slug"] = val.strip('/')
            elif line.upper().startswith("META-DESCRIPTION:") or line.upper().startswith("META DESCRIPTION:"):
                parts = line.split(':', 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(art):
                    i += 1
                    val = art[i].strip()
                meta["meta_description"] = val.strip('"')
            elif line.upper().startswith("KEYWORDS:"):
                parts = line.split(':', 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(art):
                    i += 1
                    val = art[i].strip()
                meta["keywords"] = val
            elif line.upper().startswith("CTA:"):
                parts = line.split(':', 1)
                val = parts[1].strip() if len(parts) > 1 else ""
                if not val and i + 1 < len(art):
                    i += 1
                    val = art[i].strip()
                cta = val
            elif line.upper() == "📝 CONTENIDO" or line.upper() == "CONTENIDO":
                in_body = True
            else:
                in_body = True
                body.append(line)
            i += 1
            
        if cta:
            body.append(f"\n> **CTA sugerido:** {cta}\n")
            
        meta["meta_title"] = meta["titulo"]
        parsed.append((meta, "\n\n".join(body)))
    return parsed

def parse_mitta_enero(paragraphs):
    articles = []
    current_art = []
    
    for p in paragraphs:
        if p.strip() == "🚗":
            continue
        if p.strip().startswith("CONTENIDO "):
            if current_art:
                articles.append(current_art)
                current_art = []
        current_art.append(p)
    if current_art:
        articles.append(current_art)
        
    parsed = []
    for art in articles:
        meta = {"titulo": "", "pilar": "Rent a Car", "marca": "Mitta", "meta_title": "", "meta_description": "", "keywords": "", "slug": ""}
        body = []
        i = 0
        in_body = False
        
        while i < len(art):
            line = art[i].strip()
            if in_body:
                if line.startswith("H1:"):
                    body.append(f"# {line[3:].strip()}")
                elif line.startswith("H2:"):
                    body.append(f"## {line[3:].strip()}")
                elif line.startswith("H3:"):
                    body.append(f"### {line[3:].strip()}")
                else:
                    body.append(line)
                i += 1
                continue
                
            if line.upper().startswith("CONTENIDO"):
                parts = line.split(':', 1)
                meta["titulo"] = clean_title(parts[1].strip())
            elif line.upper().startswith("EVERGREEN:"):
                pass
            elif line.upper().startswith("SLUG:"):
                meta["slug"] = line.split(':', 1)[1].strip().strip('/')
            elif line.upper().startswith("META DESCRIPCIÓN"):
                meta["meta_description"] = line.split(':', 1)[1].strip().strip('"').strip('“').strip('”')
            elif line.upper().startswith("POWER KEYWORDS:"):
                if i + 1 < len(art):
                    i += 1
                    meta["keywords"] = art[i].strip()
            elif re.match(r'^\d+\.\s+Introducción', line, re.IGNORECASE) or line.startswith("1. Introducción"):
                in_body = True
                body.append(line)
            else:
                if len(line) > 50:
                    in_body = True
                    body.append(line)
            i += 1
            
        meta["meta_title"] = meta["titulo"]
        parsed.append((meta, "\n\n".join(body)))
    return parsed

# --- PROCESO PRINCIPAL ---

def main():
    files_to_process = [
        ("Contenidos_Mittago_Enero2025_3-4-5-6.docx", "MittaGO", parse_mittago_1),
        ("Mittago_Articulos1y2_Enero2026 (1).docx", "MittaGO", parse_mittago_2),
        ("📅 CONTENIDO_mitta_Febrero_2026.docx", "Mitta", parse_mitta_febrero),
        ("🚗contenidos_Mitta_Enero2026.docx", "Mitta", parse_mitta_enero)
    ]
    
    article_index = 1
    
    for f_name, brand, parser_func in files_to_process:
        src_path = os.path.join(WORKSPACE, f_name)
        if not os.path.exists(src_path):
            src_path = os.path.join(ORIGINALES_DIR, f_name)
            if not os.path.exists(src_path):
                print(f"No se encontró el archivo {f_name} en la raíz ni en docx_originales.")
                continue
                
        print(f"\nProcesando con parser especializado: {f_name} ({brand})...")
        paragraphs = docx_to_paragraphs(src_path)
        if not paragraphs:
            print(f"No se pudieron extraer párrafos de {f_name}")
            continue
            
        articles = parser_func(paragraphs)
        print(f"Parser retornó {len(articles)} artículos.")
        
        for meta, body in articles:
            if not meta["titulo"]:
                meta["titulo"] = f"Articulo sin titulo {article_index}"
            if not meta["slug"]:
                meta["slug"] = slugify(meta["titulo"])
                
            # Limpiar el slug para usarlo en el nombre de archivo
            slug_for_filename = meta["slug"].strip('/').split('/')[-1]
            slug_for_filename = slugify(slug_for_filename)
            
            # Garantizar que el slug en frontmatter empiece con '/'
            frontmatter_slug = meta["slug"]
            if not frontmatter_slug.startswith('/'):
                frontmatter_slug = '/' + frontmatter_slug
                
            file_name = f"{article_index:02d}_{slug_for_filename}.md"
            dest_path = os.path.join(BORRADORES_DIR, file_name)
            
            with open(dest_path, "w", encoding="utf-8") as out_f:
                out_f.write("---\n")
                out_f.write(f"titulo: \"{meta['titulo']}\"\n")
                out_f.write(f"pilar: \"{meta['pilar']}\"\n")
                out_f.write(f"marca: \"{meta['marca']}\"\n")
                out_f.write(f"meta_title: \"{meta['meta_title']}\"\n")
                out_f.write(f"meta_description: \"{meta['meta_description']}\"\n")
                out_f.write(f"keywords: \"{meta['keywords']}\"\n")
                out_f.write(f"slug: \"{frontmatter_slug}\"\n")
                out_f.write("---\n\n")
                out_f.write(body)
                
            print(f"  [OK] Creado: {file_name} -> {meta['titulo'][:50]}...")
            article_index += 1
            
        src_path_root = os.path.join(WORKSPACE, f_name)
        if os.path.exists(src_path_root):
            dest_original = os.path.join(ORIGINALES_DIR, f_name)
            shutil.move(src_path_root, dest_original)
            print(f"  [MOVE] Guardado en docx_originales/")
            
    dup_path = os.path.join(WORKSPACE, "🚗contenidos_Mitta_Enero2026 (1).docx")
    if os.path.exists(dup_path):
        os.remove(dup_path)
        print(f"\nRemovido duplicado: 🚗contenidos_Mitta_Enero2026 (1).docx")
        
    print(f"\n¡Extracción especializada finalizada con éxito! Total de {article_index - 1} artículos creados en borradores/.")

if __name__ == "__main__":
    main()
