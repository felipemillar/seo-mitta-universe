#!/usr/bin/env python3
"""
=================================================================
 MITTA SEO/GEO/AEO IMPROVEMENT ENGINE
 Ejecuta las 4 fases del plan de mejora
=================================================================
"""

import os
import re
import json
import html
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta/02_Contenidos_Redactados")

stats = {"phase1": 0, "phase2": 0, "phase3": 0, "phase4": 0, "errors": []}


def strip_tags(s):
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s).strip()


# ═══════════════════════════════════════════════════════════════
# PHASE 1: Inject Schema JSON-LD into MittaGO (20 articles)
# ═══════════════════════════════════════════════════════════════

def phase1_inject_schema_mittago():
    print("\n" + "="*60)
    print("  FASE 1: Inyectar Schema JSON-LD → MittaGO (20 arts)")
    print("="*60)
    
    mittago_dir = BASE_DIR / "MittaGO" / "finales"
    
    for fpath in sorted(mittago_dir.glob("*.html")):
        content = fpath.read_text(encoding='utf-8')
        
        # Skip if already has schema
        if 'application/ld+json' in content:
            print(f"  ⏭️  {fpath.name}: ya tiene schema, skip")
            continue
        
        # Extract data for schema
        # Headline from H1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        headline = strip_tags(h1_match.group(1)) if h1_match else fpath.stem
        
        # Description from meta
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        description = desc_match.group(1) if desc_match else headline
        
        # Slug from meta-header
        slug_match = re.search(r'Ruta/Slug.*?href=["\']([^"\']+)["\']', content, re.DOTALL)
        slug = slug_match.group(1) if slug_match else f"/blog/mittago/{fpath.stem}/"
        
        # Extract FAQ items
        faq_questions = re.findall(
            r'class=["\']faq-question["\'][^>]*>(.*?)</div>',
            content, re.IGNORECASE | re.DOTALL
        )
        faq_answers = re.findall(
            r'class=["\']faq-answer["\'][^>]*>(.*?)</div>',
            content, re.IGNORECASE | re.DOTALL
        )
        
        faq_entities = []
        for q, a in zip(faq_questions, faq_answers):
            q_clean = strip_tags(q).replace('"', '\\"')
            a_clean = strip_tags(a).replace('"', '\\"')
            faq_entities.append({
                "@type": "Question",
                "name": q_clean,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a_clean
                }
            })
        
        # Build @graph schema
        graph = [
            {
                "@type": "Article",
                "inLanguage": "es-CL",
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": f"https://mitta.cl{slug}"
                },
                "headline": headline,
                "description": description,
                "author": {
                    "@type": "Organization",
                    "name": "Mitta"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Mitta Chile",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://mitta.cl/logo.png"
                    }
                },
                "datePublished": "2026-05-15",
                "dateModified": datetime.now().strftime("%Y-%m-%d"),
                "image": f"https://mitta.cl/blog/images/mittago-{fpath.stem.split('_', 1)[0]}.jpg",
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [".answer-block", ".faq-answer"]
                }
            }
        ]
        
        if faq_entities:
            graph.append({
                "@type": "FAQPage",
                "mainEntity": faq_entities
            })
        
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://mitta.cl/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://mitta.cl/blog/"},
                {"@type": "ListItem", "position": 3, "name": "MittaGO", "item": "https://mitta.cl/blog/mittago/"},
                {"@type": "ListItem", "position": 4, "name": headline[:50], "item": f"https://mitta.cl{slug}"}
            ]
        })
        
        schema_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, 
                                  ensure_ascii=False, indent=2)
        schema_block = f'\n<script type="application/ld+json">\n{schema_json}\n</script>\n'
        
        # Inject before </body>
        if '</body>' in content:
            content = content.replace('</body>', f'{schema_block}\n</body>')
        else:
            content += schema_block
        
        fpath.write_text(content, encoding='utf-8')
        stats["phase1"] += 1
        print(f"  ✅ {fpath.name}: schema inyectado ({len(faq_entities)} FAQs)")
    
    print(f"\n  📊 Fase 1 completada: {stats['phase1']} archivos modificados")


# ═══════════════════════════════════════════════════════════════
# PHASE 2: Add H1 tag to Rent a Car (30 articles)
# ═══════════════════════════════════════════════════════════════

def phase2_inject_h1_rac():
    print("\n" + "="*60)
    print("  FASE 2: Agregar H1 → Rent a Car (30 arts)")
    print("="*60)
    
    rac_dir = BASE_DIR / "Mitta_Rent_a_Car" / "finales"
    
    for fpath in sorted(rac_dir.glob("*.html")):
        content = fpath.read_text(encoding='utf-8')
        
        # Skip if already has H1
        if re.search(r'<h1[^>]*>', content, re.IGNORECASE):
            print(f"  ⏭️  {fpath.name}: ya tiene H1, skip")
            continue
        
        # Extract title from meta-header
        title_match = re.search(
            r'<strong>Titulo:</strong>\s*(.*?)(?:</div>|<br)',
            content, re.IGNORECASE | re.DOTALL
        )
        if not title_match:
            # Fallback to <title> tag
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        
        if not title_match:
            print(f"  ⚠️  {fpath.name}: no se encontró título para H1")
            stats["errors"].append(f"Phase2: no title found in {fpath.name}")
            continue
        
        title = strip_tags(title_match.group(1)).strip()
        h1_tag = f'\n        <h1>{title}</h1>\n'
        
        # Insert H1 after <article class="article-content"> 
        # or before the aeo-summary div
        if '<article class="article-content">' in content:
            # Insert right after the article tag
            content = content.replace(
                '<article class="article-content">',
                f'<article class="article-content">{h1_tag}'
            )
        elif 'class="aeo-summary"' in content:
            content = content.replace(
                '<div class="aeo-summary">',
                f'{h1_tag}\n<div class="aeo-summary">'
            )
        else:
            print(f"  ⚠️  {fpath.name}: no se encontró punto de inserción")
            stats["errors"].append(f"Phase2: no insertion point in {fpath.name}")
            continue
        
        fpath.write_text(content, encoding='utf-8')
        stats["phase2"] += 1
        print(f"  ✅ {fpath.name}: H1 insertado → \"{title[:50]}...\"")
    
    print(f"\n  📊 Fase 2 completada: {stats['phase2']} archivos modificados")


# ═══════════════════════════════════════════════════════════════
# PHASE 3: Standardize AEO markers (70 articles)
# ═══════════════════════════════════════════════════════════════

def phase3_standardize_aeo_markers():
    print("\n" + "="*60)
    print("  FASE 3: Estandarizar marcadores AEO (70 arts)")
    print("="*60)
    
    all_dirs = [
        BASE_DIR / "MittaGO" / "finales",
        BASE_DIR / "Mitta_Rent_a_Car" / "finales",
        BASE_DIR / "Nuevos_Contenidos_2026" / "finales",
        BASE_DIR / "Cyber_2026" / "finales",
    ]
    
    for d in all_dirs:
        for fpath in sorted(d.glob("*.html")):
            content = fpath.read_text(encoding='utf-8')
            modified = False
            
            # Already has both markers
            if '<!-- AEO-SUMMARY-START -->' in content and '<!-- AEO-SUMMARY-END -->' in content:
                print(f"  ⏭️  {fpath.name}: ya tiene marcadores AEO")
                continue
            
            # Pattern 1: <div class="aeo-summary">...(content)...</div>
            # Wrap with AEO markers
            aeo_match = re.search(
                r'(<div\s+class=["\']aeo-summary["\'][^>]*>.*?</div>\s*(?:</div>)?)',
                content, re.IGNORECASE | re.DOTALL
            )
            
            if aeo_match:
                original = aeo_match.group(0)
                # Check if there's a nested </div> we need to handle
                # The aeo-summary div typically contains aeo-label + blockquote + closing div
                # Find the full aeo-summary block including its closing tag
                start_pos = aeo_match.start()
                
                # Better: find the full div block
                div_start = content.find('<div class="aeo-summary">')
                if div_start == -1:
                    div_start = content.find("<div class='aeo-summary'>")
                
                if div_start >= 0:
                    # Count opening/closing divs to find the matching close
                    depth = 0
                    pos = div_start
                    div_end = -1
                    while pos < len(content):
                        open_match = re.match(r'<div[\s>]', content[pos:], re.IGNORECASE)
                        close_match = re.match(r'</div>', content[pos:], re.IGNORECASE)
                        
                        if open_match:
                            depth += 1
                            pos += len(open_match.group())
                        elif close_match:
                            depth -= 1
                            if depth == 0:
                                div_end = pos + len(close_match.group())
                                break
                            pos += len(close_match.group())
                        else:
                            pos += 1
                    
                    if div_end > 0:
                        original_block = content[div_start:div_end]
                        wrapped = f'<!-- AEO-SUMMARY-START -->\n{original_block}\n<!-- AEO-SUMMARY-END -->'
                        content = content[:div_start] + wrapped + content[div_end:]
                        modified = True
            
            # Pattern 2: <div class="answer-block"> (MittaGO pattern)
            if not modified:
                ab_match = re.search(r'<div\s+class=["\']answer-block["\']', content, re.IGNORECASE)
                if ab_match:
                    div_start = ab_match.start()
                    # Find closing div
                    depth = 0
                    pos = div_start
                    div_end = -1
                    while pos < len(content):
                        open_match = re.match(r'<div[\s>]', content[pos:], re.IGNORECASE)
                        close_match = re.match(r'</div>', content[pos:], re.IGNORECASE)
                        
                        if open_match:
                            depth += 1
                            pos += len(open_match.group())
                        elif close_match:
                            depth -= 1
                            if depth == 0:
                                div_end = pos + len(close_match.group())
                                break
                            pos += len(close_match.group())
                        else:
                            pos += 1
                    
                    if div_end > 0:
                        original_block = content[div_start:div_end]
                        # Check if AEO-SUMMARY-START already wraps it
                        pre_check = content[max(0, div_start-50):div_start]
                        if 'AEO-SUMMARY-START' not in pre_check:
                            wrapped = f'<!-- AEO-SUMMARY-START -->\n        {original_block}\n        <!-- AEO-SUMMARY-END -->'
                            content = content[:div_start] + wrapped + content[div_end:]
                            modified = True
            
            if modified:
                fpath.write_text(content, encoding='utf-8')
                stats["phase3"] += 1
                print(f"  ✅ {fpath.name}: marcadores AEO insertados")
            else:
                print(f"  ⚠️  {fpath.name}: no se encontró bloque AEO para envolver")
    
    print(f"\n  📊 Fase 3 completada: {stats['phase3']} archivos modificados")


# ═══════════════════════════════════════════════════════════════
# PHASE 4: Add FAQ Schema to NC2026 missing (4 articles)
# ═══════════════════════════════════════════════════════════════

def phase4_inject_faq_schema_nc2026():
    print("\n" + "="*60)
    print("  FASE 4: FAQ Schema → NC2026 faltantes")
    print("="*60)
    
    nc_dir = BASE_DIR / "Nuevos_Contenidos_2026" / "finales"
    
    for fpath in sorted(nc_dir.glob("*.html")):
        content = fpath.read_text(encoding='utf-8')
        
        # Check if already has FAQPage schema
        if '"FAQPage"' in content:
            continue
        
        # Check if has FAQ HTML items
        faq_questions = re.findall(
            r'class=["\']faq-question["\'][^>]*>(.*?)</(?:div|p|h\d)',
            content, re.IGNORECASE | re.DOTALL
        )
        faq_answers = re.findall(
            r'class=["\']faq-answer["\'][^>]*>(.*?)</(?:div|p)',
            content, re.IGNORECASE | re.DOTALL
        )
        
        if not faq_questions:
            print(f"  ⏭️  {fpath.name}: sin FAQ HTML, skip")
            continue
        
        faq_entities = []
        for q, a in zip(faq_questions, faq_answers):
            q_clean = strip_tags(q).replace('"', '\\"')
            a_clean = strip_tags(a).replace('"', '\\"')
            faq_entities.append({
                "@type": "Question",
                "name": q_clean,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a_clean
                }
            })
        
        if not faq_entities:
            continue
        
        faq_schema = {
            "@type": "FAQPage",
            "mainEntity": faq_entities
        }
        
        # Find existing @graph and append FAQPage
        graph_match = re.search(r'"@graph"\s*:\s*\[', content)
        if graph_match:
            # Find the closing of the @graph array (the last ] before the closing })
            # Insert FAQPage as a new item in @graph
            # Find the last schema script
            schemas = list(re.finditer(r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.IGNORECASE | re.DOTALL))
            
            if schemas:
                last_schema = schemas[-1]
                try:
                    schema_data = json.loads(last_schema.group(1))
                    if "@graph" in schema_data:
                        schema_data["@graph"].append(faq_schema)
                        new_json = json.dumps(schema_data, ensure_ascii=False, indent=2)
                        new_block = f'<script type="application/ld+json">\n{new_json}\n</script>'
                        content = content[:last_schema.start()] + new_block + content[last_schema.end():]
                    else:
                        # No @graph, add as separate script
                        faq_block = f'\n<script type="application/ld+json">\n{json.dumps({"@context": "https://schema.org", **faq_schema}, ensure_ascii=False, indent=2)}\n</script>'
                        content = content.replace('</body>', f'{faq_block}\n</body>')
                except json.JSONDecodeError:
                    # JSON parse error, add as separate block
                    faq_block = f'\n<script type="application/ld+json">\n{json.dumps({"@context": "https://schema.org", **faq_schema}, ensure_ascii=False, indent=2)}\n</script>'
                    content = content.replace('</body>', f'{faq_block}\n</body>')
        else:
            # No existing schema, add standalone
            faq_full = {"@context": "https://schema.org", **faq_schema}
            faq_block = f'\n<script type="application/ld+json">\n{json.dumps(faq_full, ensure_ascii=False, indent=2)}\n</script>'
            content = content.replace('</body>', f'{faq_block}\n</body>')
        
        fpath.write_text(content, encoding='utf-8')
        stats["phase4"] += 1
        print(f"  ✅ {fpath.name}: FAQPage schema inyectado ({len(faq_entities)} Qs)")
    
    print(f"\n  📊 Fase 4 completada: {stats['phase4']} archivos modificados")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("="*60)
    print("  MITTA SEO/GEO/AEO IMPROVEMENT ENGINE")
    print("  4 Fases de Mejora Automatizada")
    print("="*60)
    
    phase1_inject_schema_mittago()
    phase2_inject_h1_rac()
    phase3_standardize_aeo_markers()
    phase4_inject_faq_schema_nc2026()
    
    print("\n" + "="*60)
    print("  RESUMEN FINAL")
    print("="*60)
    print(f"  Fase 1 (Schema MittaGO):  {stats['phase1']} archivos")
    print(f"  Fase 2 (H1 RAC):          {stats['phase2']} archivos")
    print(f"  Fase 3 (AEO markers):     {stats['phase3']} archivos")
    print(f"  Fase 4 (FAQ Schema NC26): {stats['phase4']} archivos")
    total = stats['phase1'] + stats['phase2'] + stats['phase3'] + stats['phase4']
    print(f"  ─────────────────────────────────")
    print(f"  TOTAL modificaciones:     {total}")
    if stats['errors']:
        print(f"\n  ⚠️  Errores: {len(stats['errors'])}")
        for e in stats['errors']:
            print(f"    • {e}")
    print()
    print("✅ Mejora completada. Ejecute re-auditoría para validar.")
