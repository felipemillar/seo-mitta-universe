#!/usr/bin/env python3
"""
=================================================================
 MITTA SEO / GEO / AEO AUDIT ENGINE v2.0
 Agente Auditor — Diagnóstico Completo de 71 Artículos
=================================================================
 Evalúa 18 criterios ponderados en 3 dimensiones:
   • SEO (40%): Title, Meta Desc, H1, Heading Hierarchy, Schema,
                 Internal Links, Word Count, URL/Slug
   • GEO (30%): Tables, Lists, Blockquotes, Data Density,
                 Structured Formatting, Cross-linking
   • AEO (30%): AEO Summary Block, FAQ Section, FAQ Schema,
                 Question-based H2s, Citability Score
=================================================================
"""

import os
import re
import json
import html
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ─── CONFIG ───────────────────────────────────────────────────────
BASE_DIR = Path("/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta/02_Contenidos_Redactados")
OUTPUT_DIR = Path("/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta/04_Auditorias_y_Reportes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CATEGORIES = {
    "MittaGO": BASE_DIR / "MittaGO" / "finales",
    "Mitta_Rent_a_Car": BASE_DIR / "Mitta_Rent_a_Car" / "finales",
    "Nuevos_Contenidos_2026": BASE_DIR / "Nuevos_Contenidos_2026" / "finales",
    "Cyber_2026": BASE_DIR / "Cyber_2026" / "finales",
}

# Weights per dimension
WEIGHTS = {"SEO": 0.40, "GEO": 0.30, "AEO": 0.30}


# ─── HELPER: Strip HTML tags for text analysis ───────────────────
def strip_tags(html_str):
    """Remove HTML tags but preserve text content."""
    clean = re.sub(r'<style[^>]*>.*?</style>', '', html_str, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<script[^>]*>.*?</script>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = html.unescape(clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


def count_words(text):
    """Count words in plain text."""
    return len(text.split())


def extract_text_content(html_str):
    """Get visible text for word count / analysis."""
    # Remove visual-prompt-matrix (non-content)
    clean = re.sub(r'<!-- INICIO MATRIZ VISUAL.*?<!-- FIN MATRIZ VISUAL[^>]*-->', '', html_str, flags=re.DOTALL)
    # Remove style/script
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<script[^>]*>.*?</script>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    # Remove meta-header
    clean = re.sub(r'<header class="meta-header">.*?</header>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = html.unescape(clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


# ─── AUDIT FUNCTIONS ─────────────────────────────────────────────

def audit_seo(html_str, filepath):
    """Score SEO metrics: 8 criteria, each 0-100."""
    results = {}
    issues = []
    
    # 1. TITLE TAG
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html_str, re.IGNORECASE | re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
        title_len = len(title)
        if 30 <= title_len <= 60:
            results["title_tag"] = 100
        elif 20 <= title_len <= 70:
            results["title_tag"] = 70
            issues.append(f"Title length {title_len} chars (ideal: 30-60)")
        else:
            results["title_tag"] = 30
            issues.append(f"Title length {title_len} chars (fuera de rango)")
    else:
        results["title_tag"] = 0
        issues.append("❌ FALTA tag <title>")
    
    # 2. META DESCRIPTION
    meta_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html_str, re.IGNORECASE)
    if meta_match:
        desc = meta_match.group(1).strip()
        desc_len = len(desc)
        if 120 <= desc_len <= 155:
            results["meta_description"] = 100
        elif 100 <= desc_len <= 170:
            results["meta_description"] = 75
            issues.append(f"Meta description {desc_len} chars (ideal: 120-155)")
        else:
            results["meta_description"] = 40
            issues.append(f"Meta description {desc_len} chars (fuera de rango)")
    else:
        results["meta_description"] = 0
        issues.append("❌ FALTA meta description")
    
    # 3. H1 TAG (single, unique)
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html_str, re.IGNORECASE | re.DOTALL)
    if len(h1_matches) == 1:
        results["h1_tag"] = 100
    elif len(h1_matches) > 1:
        results["h1_tag"] = 50
        issues.append(f"Múltiples H1 ({len(h1_matches)}). Debe haber solo 1")
    else:
        results["h1_tag"] = 0
        issues.append("❌ FALTA H1")
    
    # 4. HEADING HIERARCHY (H2 with IDs)
    h2_matches = re.findall(r'<h2[^>]*id=["\']([^"\']*)["\'][^>]*>(.*?)</h2>', html_str, re.IGNORECASE | re.DOTALL)
    h2_all = re.findall(r'<h2[^>]*>(.*?)</h2>', html_str, re.IGNORECASE | re.DOTALL)
    h3_all = re.findall(r'<h3[^>]*>(.*?)</h3>', html_str, re.IGNORECASE | re.DOTALL)
    
    if len(h2_all) >= 3:
        id_ratio = len(h2_matches) / max(len(h2_all), 1)
        results["heading_hierarchy"] = int(min(100, 50 + (id_ratio * 50)))
        if id_ratio < 0.8:
            missing = len(h2_all) - len(h2_matches)
            issues.append(f"{missing} H2s sin atributo id= (necesario para TOC/sitelinks)")
    elif len(h2_all) >= 1:
        results["heading_hierarchy"] = 60
        issues.append(f"Solo {len(h2_all)} H2s (mínimo recomendado: 3+)")
    else:
        results["heading_hierarchy"] = 0
        issues.append("❌ Sin encabezados H2")

    # 5. SCHEMA JSON-LD
    schemas = re.findall(r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html_str, re.IGNORECASE | re.DOTALL)
    if schemas:
        has_article = any('"Article"' in s or '"BlogPosting"' in s for s in schemas)
        has_faq = any('"FAQPage"' in s for s in schemas)
        has_breadcrumb = any('"BreadcrumbList"' in s for s in schemas)
        has_graph = any('"@graph"' in s for s in schemas)
        
        score = 25  # Base for having any schema
        if has_article: score += 25
        if has_faq: score += 25
        if has_breadcrumb: score += 15
        if has_graph: score += 10
        results["schema_jsonld"] = min(100, score)
        
        missing_schemas = []
        if not has_article: missing_schemas.append("Article/BlogPosting")
        if not has_faq: missing_schemas.append("FAQPage")
        if not has_breadcrumb: missing_schemas.append("BreadcrumbList")
        if not has_graph: missing_schemas.append("@graph wrapper")
        if missing_schemas:
            issues.append(f"Schema faltante: {', '.join(missing_schemas)}")
    else:
        results["schema_jsonld"] = 0
        issues.append("❌ SIN Schema JSON-LD (crítico)")
    
    # 6. INTERNAL LINKS (cross-linking)
    internal_links = re.findall(r'href=["\'](?!#)(/[^"\']*|https?://mitta\.cl[^"\']*)["\']', html_str, re.IGNORECASE)
    suggested_links = re.findall(r'\[LINK\s+INTERNO\s+SUGERIDO', html_str, re.IGNORECASE)
    total_links = len(internal_links) + len(suggested_links)
    if total_links >= 3:
        results["internal_links"] = 100
    elif total_links >= 1:
        results["internal_links"] = 60
        issues.append(f"Solo {total_links} internal links (recomendado: 3+)")
    else:
        results["internal_links"] = 20
        issues.append("⚠️ Sin internal links (posible página huérfana)")
    
    # 7. WORD COUNT
    text = extract_text_content(html_str)
    wc = count_words(text)
    if 1200 <= wc <= 3000:
        results["word_count"] = 100
    elif 800 <= wc <= 4000:
        results["word_count"] = 75
        issues.append(f"Word count: {wc} (ideal: 1200-3000)")
    elif wc >= 500:
        results["word_count"] = 50
        issues.append(f"Word count bajo: {wc}")
    else:
        results["word_count"] = 25
        issues.append(f"Word count muy bajo: {wc}")
    
    # 8. URL/SLUG quality
    slug_match = re.search(r'href=["\'](/[a-z0-9\-]+/)["\']', html_str)
    if not slug_match:
        # Check meta-header for slug
        slug_match = re.search(r'Ruta/Slug.*?href=["\']([^"\']+)["\']', html_str, re.DOTALL)
    if slug_match:
        slug = slug_match.group(1)
        if len(slug) <= 60 and re.match(r'^/[a-z0-9\-/]+$', slug):
            results["url_slug"] = 100
        else:
            results["url_slug"] = 60
            issues.append(f"Slug podría mejorar: {slug}")
    else:
        results["url_slug"] = 50
        issues.append("No se detectó slug definido")
    
    avg = sum(results.values()) / len(results) if results else 0
    return {"scores": results, "average": round(avg, 1), "issues": issues, "word_count": wc, "h2_count": len(h2_all), "h3_count": len(h3_all)}


def audit_geo(html_str, filepath):
    """Score GEO metrics: 6 criteria, each 0-100."""
    results = {}
    issues = []
    
    # 1. TABLES (structured data for AI extraction)
    tables = re.findall(r'<table', html_str, re.IGNORECASE)
    # Exclude the visual-prompt-matrix table
    matrix_tables = len(re.findall(r'visual-prompt-matrix', html_str))
    content_tables = len(tables) - matrix_tables
    if content_tables >= 2:
        results["tables"] = 100
    elif content_tables == 1:
        results["tables"] = 70
    else:
        results["tables"] = 0
        issues.append("❌ Sin tablas de datos (crítico para GEO)")
    
    # 2. LISTS (ordered + unordered)
    ol_count = len(re.findall(r'<ol', html_str, re.IGNORECASE))
    ul_count = len(re.findall(r'<ul', html_str, re.IGNORECASE))
    # Exclude TOC ul
    toc_uls = len(re.findall(r'class=["\']toc["\']', html_str, re.IGNORECASE))
    content_lists = ol_count + max(0, ul_count - toc_uls)
    if content_lists >= 3:
        results["lists"] = 100
    elif content_lists >= 1:
        results["lists"] = 60
        issues.append(f"Solo {content_lists} listas en contenido (recomendado: 3+)")
    else:
        results["lists"] = 20
        issues.append("⚠️ Sin listas en contenido")
    
    # 3. DATA DENSITY (numbers, percentages, currencies in text)
    text = extract_text_content(html_str)
    data_points = re.findall(r'\$[\d.,]+|\d+%|\d{2,}[\s]*(CLP|USD|UF|km|hrs?|días?|meses?|años?|cuotas?)', text, re.IGNORECASE)
    hard_numbers = re.findall(r'\b\d{2,}\b', text)
    density = len(data_points) + len(hard_numbers) * 0.3
    if density >= 15:
        results["data_density"] = 100
    elif density >= 8:
        results["data_density"] = 70
    elif density >= 3:
        results["data_density"] = 45
        issues.append(f"Baja densidad de datos ({int(density)} puntos)")
    else:
        results["data_density"] = 15
        issues.append(f"⚠️ Muy baja densidad de datos ({int(density)} puntos)")
    
    # 4. BLOCKQUOTES / CALLOUTS (citability)
    blockquotes = len(re.findall(r'<blockquote|class=["\'].*?callout|class=["\'].*?highlight-box', html_str, re.IGNORECASE))
    answer_blocks = len(re.findall(r'class=["\']answer-block["\']', html_str, re.IGNORECASE))
    total_quotes = blockquotes + answer_blocks
    if total_quotes >= 2:
        results["blockquotes"] = 100
    elif total_quotes == 1:
        results["blockquotes"] = 60
    else:
        results["blockquotes"] = 20
        issues.append("Sin blockquotes/callouts de citación")
    
    # 5. CROSS-LINKING DENSITY (links per 500 words)
    text = extract_text_content(html_str)
    wc = count_words(text)
    all_links = re.findall(r'<a\s+[^>]*href', html_str, re.IGNORECASE)
    suggested = re.findall(r'\[LINK\s+INTERNO', html_str, re.IGNORECASE)
    link_density = (len(all_links) + len(suggested)) / max(wc / 500, 1)
    if link_density >= 2:
        results["cross_linking"] = 100
    elif link_density >= 1:
        results["cross_linking"] = 65
    else:
        results["cross_linking"] = 30
        issues.append("Baja densidad de cross-linking")
    
    # 6. STRUCTURED FORMATTING (bold, strong, em usage)
    strong_count = len(re.findall(r'<strong', html_str, re.IGNORECASE))
    em_count = len(re.findall(r'<em', html_str, re.IGNORECASE))
    formatting = strong_count + em_count
    if formatting >= 10:
        results["formatting"] = 100
    elif formatting >= 5:
        results["formatting"] = 70
    elif formatting >= 2:
        results["formatting"] = 40
    else:
        results["formatting"] = 10
        issues.append("Insuficiente formateo (bold/italic)")
    
    avg = sum(results.values()) / len(results) if results else 0
    return {"scores": results, "average": round(avg, 1), "issues": issues, "tables": content_tables, "lists": content_lists}


def audit_aeo(html_str, filepath):
    """Score AEO metrics: 5 criteria, each 0-100."""
    results = {}
    issues = []
    
    # 1. AEO SUMMARY BLOCK — recognize both patterns:
    #    Pattern A: <!-- AEO-SUMMARY-START --> ... <!-- AEO-SUMMARY-END -->
    #    Pattern B: <div class="aeo-summary"> with blockquote
    #    Pattern C: <div class="answer-block"> (MittaGO)
    aeo_start = re.search(r'AEO-SUMMARY-START', html_str, re.IGNORECASE)
    aeo_end = re.search(r'AEO-SUMMARY-END', html_str, re.IGNORECASE)
    aeo_div = re.search(r'class=["\']aeo-summary["\']', html_str, re.IGNORECASE)
    answer_block = re.search(r'class=["\']answer-block["\']', html_str, re.IGNORECASE)
    
    if aeo_start and aeo_end:
        # Best case: has explicit markers
        aeo_content = html_str[aeo_start.end():aeo_end.start()]
        aeo_text = strip_tags(aeo_content)
        aeo_wc = count_words(aeo_text)
        if 40 <= aeo_wc <= 180:
            results["aeo_summary"] = 100
        elif 20 <= aeo_wc <= 250:
            results["aeo_summary"] = 70
            issues.append(f"AEO summary: {aeo_wc} words (ideal: 40-180)")
        else:
            results["aeo_summary"] = 40
            issues.append(f"AEO summary muy {'corto' if aeo_wc < 20 else 'largo'}: {aeo_wc} words")
    elif aeo_div or answer_block:
        # Has visual AEO block but without markers — still counts as present
        results["aeo_summary"] = 60
        issues.append("Tiene bloque AEO visual pero sin marcadores START/END")
    else:
        results["aeo_summary"] = 0
        issues.append("❌ FALTA bloque AEO Summary (crítico)")
    
    # 2. FAQ SECTION (HTML) — recognize both patterns:
    #    Pattern A: .faq-section wrapper with .faq-item children
    #    Pattern B: .faq-question elements without wrapper (RAC/NC26/Cyber)
    faq_section = re.search(r'class=["\']faq-section["\']', html_str, re.IGNORECASE)
    faq_items = re.findall(r'class=["\']faq-item["\']', html_str, re.IGNORECASE)
    faq_questions = re.findall(r'class=["\']faq-question["\']', html_str, re.IGNORECASE)
    total_faq = max(len(faq_items), len(faq_questions))
    
    if total_faq >= 3:
        results["faq_section"] = 100
    elif total_faq >= 1:
        results["faq_section"] = 70
        issues.append(f"Solo {total_faq} FAQ items (recomendado: 3+)")
    else:
        results["faq_section"] = 0
        issues.append("❌ FALTA sección FAQ (crítico para AEO)")
    
    # 3. FAQ SCHEMA (JSON-LD)
    schemas = re.findall(r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html_str, re.IGNORECASE | re.DOTALL)
    has_faq_schema = any('"FAQPage"' in s for s in schemas)
    
    if has_faq_schema:
        # Count FAQ items in schema
        faq_schema_questions = 0
        for s in schemas:
            faq_schema_questions += len(re.findall(r'"@type"\s*:\s*"Question"', s))
        
        if faq_schema_questions >= 3:
            results["faq_schema"] = 100
        elif faq_schema_questions >= 1:
            results["faq_schema"] = 70
            issues.append(f"Schema FAQPage con solo {faq_schema_questions} questions")
        else:
            results["faq_schema"] = 40
    else:
        results["faq_schema"] = 0
        issues.append("❌ FALTA Schema FAQPage JSON-LD")
    
    # 4. QUESTION-BASED HEADINGS
    h2_texts = re.findall(r'<h2[^>]*>(.*?)</h2>', html_str, re.IGNORECASE | re.DOTALL)
    h2_questions = [h for h in h2_texts if '?' in strip_tags(h) or 
                    any(strip_tags(h).lower().startswith(q) for q in ['¿', 'cómo', 'qué', 'cuál', 'por qué', 'cuánto', 'cuándo', 'dónde'])]
    
    if len(h2_texts) > 0:
        q_ratio = len(h2_questions) / len(h2_texts)
        if q_ratio >= 0.4:
            results["question_headings"] = 100
        elif q_ratio >= 0.2:
            results["question_headings"] = 65
        elif len(h2_questions) >= 1:
            results["question_headings"] = 45
        else:
            results["question_headings"] = 20
            issues.append("Ningún H2 es una pregunta (reduce citabilidad AI)")
    else:
        results["question_headings"] = 0
    
    # 5. CITABILITY (self-contained factual paragraphs)
    # Count paragraphs with hard data that could be cited
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_str, re.IGNORECASE | re.DOTALL)
    citable = 0
    for p in paragraphs:
        pt = strip_tags(p)
        pw = count_words(pt)
        has_data = bool(re.search(r'\d+', pt))
        has_entity = bool(re.search(r'(Mitta|MittaGO|Chile|Santiago|ANAC|Mitsui)', pt, re.IGNORECASE))
        if 30 <= pw <= 180 and (has_data or has_entity):
            citable += 1
    
    if citable >= 5:
        results["citability"] = 100
    elif citable >= 3:
        results["citability"] = 70
    elif citable >= 1:
        results["citability"] = 45
    else:
        results["citability"] = 15
        issues.append("Baja citabilidad: pocos párrafos auto-contenidos con datos")
    
    avg = sum(results.values()) / len(results) if results else 0
    return {"scores": results, "average": round(avg, 1), "issues": issues, "faq_count": len(faq_items)}


# ─── MAIN AUDIT ENGINE ───────────────────────────────────────────

def audit_all_articles():
    """Run full audit across all categories and articles."""
    all_results = []
    category_stats = {}
    
    for cat_name, cat_path in CATEGORIES.items():
        if not cat_path.exists():
            print(f"⚠️  Skipping {cat_name}: path not found")
            continue
        
        html_files = sorted(cat_path.glob("*.html"))
        cat_results = []
        
        for fpath in html_files:
            print(f"  🔍 Auditing: {fpath.name}")
            content = fpath.read_text(encoding='utf-8', errors='replace')
            
            seo = audit_seo(content, fpath)
            geo = audit_geo(content, fpath)
            aeo = audit_aeo(content, fpath)
            
            # Weighted composite score
            composite = (
                seo["average"] * WEIGHTS["SEO"] +
                geo["average"] * WEIGHTS["GEO"] +
                aeo["average"] * WEIGHTS["AEO"]
            )
            
            # Extract title for display
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
            title = strip_tags(title_match.group(1)) if title_match else fpath.stem
            
            result = {
                "file": fpath.name,
                "category": cat_name,
                "title": title,
                "seo": seo,
                "geo": geo,
                "aeo": aeo,
                "composite_score": round(composite, 1),
                "all_issues": seo["issues"] + geo["issues"] + aeo["issues"],
                "grade": get_grade(composite),
            }
            cat_results.append(result)
            all_results.append(result)
        
        if cat_results:
            avg_composite = sum(r["composite_score"] for r in cat_results) / len(cat_results)
            category_stats[cat_name] = {
                "count": len(cat_results),
                "avg_score": round(avg_composite, 1),
                "avg_seo": round(sum(r["seo"]["average"] for r in cat_results) / len(cat_results), 1),
                "avg_geo": round(sum(r["geo"]["average"] for r in cat_results) / len(cat_results), 1),
                "avg_aeo": round(sum(r["aeo"]["average"] for r in cat_results) / len(cat_results), 1),
                "grade": get_grade(avg_composite),
            }
            print(f"  ✅ {cat_name}: {len(cat_results)} articles, avg score: {avg_composite:.1f}")
    
    return all_results, category_stats


def get_grade(score):
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B+"
    if score >= 60: return "B"
    if score >= 50: return "C+"
    if score >= 40: return "C"
    if score >= 30: return "D"
    return "F"


def get_grade_color(grade):
    colors = {
        "A+": "#10b981", "A": "#34d399",
        "B+": "#3b82f6", "B": "#60a5fa",
        "C+": "#f59e0b", "C": "#fbbf24",
        "D": "#f97316", "F": "#ef4444"
    }
    return colors.get(grade, "#6b7280")


# ─── HTML REPORT GENERATOR ───────────────────────────────────────

def generate_html_report(results, category_stats):
    """Generate comprehensive HTML diagnostic report."""
    
    total_articles = len(results)
    global_avg = sum(r["composite_score"] for r in results) / max(total_articles, 1)
    global_seo = sum(r["seo"]["average"] for r in results) / max(total_articles, 1)
    global_geo = sum(r["geo"]["average"] for r in results) / max(total_articles, 1)
    global_aeo = sum(r["aeo"]["average"] for r in results) / max(total_articles, 1)
    
    # Count critical issues
    total_issues = sum(len(r["all_issues"]) for r in results)
    critical_issues = sum(1 for r in results for i in r["all_issues"] if "❌" in i)
    warning_issues = sum(1 for r in results for i in r["all_issues"] if "⚠️" in i)
    
    # Top/Bottom performers
    sorted_results = sorted(results, key=lambda x: x["composite_score"], reverse=True)
    top5 = sorted_results[:5]
    bottom5 = sorted_results[-5:]
    
    # Issue frequency analysis
    issue_freq = defaultdict(int)
    for r in results:
        for issue in r["all_issues"]:
            # Normalize issue text
            normalized = re.sub(r'\d+', 'N', issue)
            issue_freq[normalized] += 1
    top_issues = sorted(issue_freq.items(), key=lambda x: x[1], reverse=True)[:15]
    
    # Articles missing schema (critical gap)
    no_schema = [r for r in results if r["seo"]["scores"].get("schema_jsonld", 0) == 0]
    no_aeo = [r for r in results if r["aeo"]["scores"].get("aeo_summary", 0) <= 20]
    no_faq_schema = [r for r in results if r["aeo"]["scores"].get("faq_schema", 0) == 0]
    
    html = f"""<!DOCTYPE html>
<html lang="es-CL">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auditoría SEO/GEO/AEO — Mitta Blog Content</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0a0b0f;
            --bg-card: rgba(17, 24, 39, 0.7);
            --bg-card-hover: rgba(17, 24, 39, 0.9);
            --border: rgba(255,255,255,0.06);
            --border-hover: rgba(255,255,255,0.15);
            --text: #e2e8f0;
            --text-dim: #94a3b8;
            --text-muted: #64748b;
            --green: #10b981;
            --green-glow: rgba(16, 185, 129, 0.15);
            --blue: #3b82f6;
            --blue-glow: rgba(59, 130, 246, 0.15);
            --purple: #8b5cf6;
            --purple-glow: rgba(139, 92, 246, 0.15);
            --amber: #f59e0b;
            --red: #ef4444;
            --gradient-main: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            min-height: 100vh;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 2rem; }}
        
        /* Header */
        .report-header {{
            text-align: center;
            padding: 4rem 2rem;
            margin-bottom: 3rem;
            border-bottom: 1px solid var(--border);
            position: relative;
        }}
        .report-header::before {{
            content: '';
            position: absolute;
            top: 0; left: 50%; transform: translateX(-50%);
            width: 600px; height: 300px;
            background: radial-gradient(ellipse, rgba(59,130,246,0.08) 0%, transparent 70%);
            pointer-events: none;
        }}
        .report-header h1 {{
            font-size: 2.8rem;
            font-weight: 800;
            background: var(--gradient-main);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        .report-header .subtitle {{
            font-size: 1.1rem;
            color: var(--text-dim);
        }}
        .report-header .timestamp {{
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 0.5rem;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        /* Score Cards Row */
        .score-cards {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 3rem;
        }}
        .score-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s;
            backdrop-filter: blur(10px);
        }}
        .score-card:hover {{
            border-color: var(--border-hover);
            transform: translateY(-2px);
        }}
        .score-card .label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }}
        .score-card .big-score {{
            font-size: 3rem;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 0.25rem;
        }}
        .score-card .grade-badge {{
            display: inline-block;
            padding: 2px 12px;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }}
        
        /* Category Breakdown */
        .section-title {{
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .section-title::before {{
            content: '';
            width: 4px;
            height: 28px;
            background: var(--gradient-main);
            border-radius: 2px;
        }}
        
        .cat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }}
        .cat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s;
        }}
        .cat-card:hover {{
            border-color: var(--border-hover);
        }}
        .cat-card h3 {{
            font-size: 1.1rem;
            margin-bottom: 1rem;
            color: #fff;
        }}
        .cat-bar {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.6rem;
            font-size: 0.85rem;
        }}
        .cat-bar .bar-label {{
            width: 40px;
            color: var(--text-muted);
            font-weight: 500;
        }}
        .cat-bar .bar-track {{
            flex: 1;
            height: 8px;
            background: rgba(255,255,255,0.05);
            border-radius: 4px;
            overflow: hidden;
        }}
        .cat-bar .bar-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s ease;
        }}
        .cat-bar .bar-val {{
            width: 40px;
            text-align: right;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        }}
        
        /* Issues Summary */
        .issues-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 3rem;
        }}
        .issue-stat {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }}
        .issue-stat .num {{
            font-size: 2.5rem;
            font-weight: 800;
        }}
        .issue-stat .desc {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        
        /* Top Issues Table */
        .issues-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 3rem;
        }}
        .issues-table th {{
            text-align: left;
            padding: 12px 16px;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border);
        }}
        .issues-table td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
            font-size: 0.9rem;
        }}
        .issues-table tr:hover {{
            background: rgba(255,255,255,0.02);
        }}
        .freq-bar {{
            display: inline-block;
            height: 6px;
            border-radius: 3px;
            background: var(--blue);
            margin-right: 8px;
            vertical-align: middle;
        }}
        
        /* Article Table */
        .article-table-wrapper {{
            overflow-x: auto;
            margin-bottom: 3rem;
        }}
        .article-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }}
        .article-table th {{
            position: sticky;
            top: 0;
            background: #111827;
            text-align: left;
            padding: 12px 10px;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            border-bottom: 2px solid var(--border);
            white-space: nowrap;
        }}
        .article-table td {{
            padding: 10px;
            border-bottom: 1px solid var(--border);
            vertical-align: middle;
        }}
        .article-table tr:hover {{
            background: rgba(59,130,246,0.04);
        }}
        .mini-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
        }}
        .cat-label {{
            font-size: 0.7rem;
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: 500;
            background: rgba(255,255,255,0.06);
            color: var(--text-dim);
            white-space: nowrap;
        }}
        
        /* Critical Gaps */
        .gap-section {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
        }}
        .gap-section h3 {{
            color: var(--red);
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }}
        .gap-list {{
            columns: 2;
            column-gap: 2rem;
            list-style: none;
        }}
        .gap-list li {{
            padding: 4px 0;
            font-size: 0.85rem;
            color: var(--text-dim);
            break-inside: avoid;
        }}
        .gap-list li::before {{
            content: '×';
            color: var(--red);
            font-weight: 700;
            margin-right: 8px;
        }}
        
        /* Dimension Deep Dive */
        .detail-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        }}
        .detail-card h3 {{
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
        }}
        .detail-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}
        .detail-metric {{
            text-align: center;
            padding: 1rem;
            background: rgba(255,255,255,0.02);
            border-radius: 8px;
        }}
        .detail-metric .metric-val {{
            font-size: 2rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }}
        .detail-metric .metric-label {{
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.25rem;
        }}

        /* Filter */
        .filter-bar {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }}
        .filter-btn {{
            padding: 6px 16px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: transparent;
            color: var(--text-dim);
            cursor: pointer;
            font-size: 0.85rem;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            border-color: var(--blue);
            color: var(--blue);
            background: var(--blue-glow);
        }}
        
        @media (max-width: 768px) {{
            .score-cards {{ grid-template-columns: repeat(2, 1fr); }}
            .issues-grid {{ grid-template-columns: 1fr; }}
            .gap-list {{ columns: 1; }}
        }}
    </style>
</head>
<body>
<div class="container">

    <!-- HEADER -->
    <header class="report-header">
        <h1>Auditoría SEO / GEO / AEO</h1>
        <p class="subtitle">Diagnóstico completo de {total_articles} artículos de blog — Proyecto Mitta × INMedios</p>
        <p class="timestamp">Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · Motor: Audit Engine v2.0</p>
    </header>

    <!-- GLOBAL SCORES -->
    <div class="score-cards">
        <div class="score-card" style="border-color: {get_grade_color(get_grade(global_avg))}20;">
            <div class="label">Score Global</div>
            <div class="big-score" style="color: {get_grade_color(get_grade(global_avg))};">{global_avg:.0f}</div>
            <span class="grade-badge" style="background: {get_grade_color(get_grade(global_avg))}20; color: {get_grade_color(get_grade(global_avg))};">{get_grade(global_avg)}</span>
        </div>
        <div class="score-card">
            <div class="label">SEO (40%)</div>
            <div class="big-score" style="color: {get_grade_color(get_grade(global_seo))};">{global_seo:.0f}</div>
            <span class="grade-badge" style="background: {get_grade_color(get_grade(global_seo))}20; color: {get_grade_color(get_grade(global_seo))};">{get_grade(global_seo)}</span>
        </div>
        <div class="score-card">
            <div class="label">GEO (30%)</div>
            <div class="big-score" style="color: {get_grade_color(get_grade(global_geo))};">{global_geo:.0f}</div>
            <span class="grade-badge" style="background: {get_grade_color(get_grade(global_geo))}20; color: {get_grade_color(get_grade(global_geo))};">{get_grade(global_geo)}</span>
        </div>
        <div class="score-card">
            <div class="label">AEO (30%)</div>
            <div class="big-score" style="color: {get_grade_color(get_grade(global_aeo))};">{global_aeo:.0f}</div>
            <span class="grade-badge" style="background: {get_grade_color(get_grade(global_aeo))}20; color: {get_grade_color(get_grade(global_aeo))};">{get_grade(global_aeo)}</span>
        </div>
    </div>

    <!-- ISSUE SUMMARY -->
    <div class="issues-grid">
        <div class="issue-stat">
            <div class="num" style="color: var(--red);">{critical_issues}</div>
            <div class="desc">Issues Críticos (❌)</div>
        </div>
        <div class="issue-stat">
            <div class="num" style="color: var(--amber);">{warning_issues}</div>
            <div class="desc">Warnings (⚠️)</div>
        </div>
        <div class="issue-stat">
            <div class="num" style="color: var(--text-dim);">{total_issues}</div>
            <div class="desc">Total Issues</div>
        </div>
    </div>

    <!-- CATEGORY BREAKDOWN -->
    <h2 class="section-title">Score por Categoría</h2>
    <div class="cat-grid">
"""
    
    # Category cards
    for cat_name, stats in category_stats.items():
        grade_color = get_grade_color(stats["grade"])
        html += f"""
        <div class="cat-card">
            <h3>{cat_name.replace('_', ' ')} <span style="float:right; color:{grade_color}; font-family:'JetBrains Mono';">{stats['avg_score']}</span></h3>
            <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:1rem;">{stats['count']} artículos · Nota: {stats['grade']}</div>
            <div class="cat-bar">
                <span class="bar-label">SEO</span>
                <div class="bar-track"><div class="bar-fill" style="width:{stats['avg_seo']}%; background:var(--blue);"></div></div>
                <span class="bar-val">{stats['avg_seo']}</span>
            </div>
            <div class="cat-bar">
                <span class="bar-label">GEO</span>
                <div class="bar-track"><div class="bar-fill" style="width:{stats['avg_geo']}%; background:var(--green);"></div></div>
                <span class="bar-val">{stats['avg_geo']}</span>
            </div>
            <div class="cat-bar">
                <span class="bar-label">AEO</span>
                <div class="bar-track"><div class="bar-fill" style="width:{stats['avg_aeo']}%; background:var(--purple);"></div></div>
                <span class="bar-val">{stats['avg_aeo']}</span>
            </div>
        </div>
"""
    
    html += """
    </div>

    <!-- CRITICAL GAPS -->
    <h2 class="section-title">Brechas Críticas</h2>
"""
    
    # No Schema
    if no_schema:
        html += f"""
    <div class="gap-section">
        <h3>🔴 {len(no_schema)} artículos SIN Schema JSON-LD</h3>
        <p style="font-size:0.9rem; color:var(--text-dim); margin-bottom:1rem;">Google no puede interpretar datos estructurados. Impacto directo en Rich Results y Featured Snippets.</p>
        <ul class="gap-list">
"""
        for r in no_schema:
            html += f'            <li>{r["category"]}: {r["file"]}</li>\n'
        html += """        </ul>
    </div>
"""
    
    # No AEO
    if no_aeo:
        html += f"""
    <div class="gap-section">
        <h3>🔴 {len(no_aeo)} artículos SIN bloque AEO Summary</h3>
        <p style="font-size:0.9rem; color:var(--text-dim); margin-bottom:1rem;">Sin AEO Summary, las IAs (ChatGPT, Perplexity, AI Overviews) no extraerán respuestas directas de estos contenidos.</p>
        <ul class="gap-list">
"""
        for r in no_aeo:
            html += f'            <li>{r["category"]}: {r["file"]}</li>\n'
        html += """        </ul>
    </div>
"""
    
    # No FAQ Schema
    if no_faq_schema:
        html += f"""
    <div class="gap-section">
        <h3>🟡 {len(no_faq_schema)} artículos SIN Schema FAQPage</h3>
        <p style="font-size:0.9rem; color:var(--text-dim); margin-bottom:1rem;">Tienen FAQ visual pero no el markup JSON-LD. Google no generará Rich FAQ Snippets.</p>
        <ul class="gap-list">
"""
        for r in no_faq_schema:
            html += f'            <li>{r["category"]}: {r["file"]}</li>\n'
        html += """        </ul>
    </div>
"""
    
    # TOP ISSUES
    html += """
    <h2 class="section-title">Top 15 Issues más Frecuentes</h2>
    <table class="issues-table">
        <thead>
            <tr><th>#</th><th>Issue</th><th>Frecuencia</th></tr>
        </thead>
        <tbody>
"""
    for i, (issue, freq) in enumerate(top_issues, 1):
        bar_w = min(100, int(freq / max(total_articles, 1) * 100))
        html += f"""            <tr>
                <td style="color:var(--text-muted); width:30px;">{i}</td>
                <td>{issue}</td>
                <td style="width:200px;"><span class="freq-bar" style="width:{bar_w}px;"></span> {freq}/{total_articles}</td>
            </tr>
"""
    html += """        </tbody>
    </table>
"""
    
    # FULL ARTICLE TABLE
    html += """
    <h2 class="section-title">Detalle por Artículo</h2>
    <div class="filter-bar">
        <button class="filter-btn active" onclick="filterCat('all')">Todos</button>
"""
    for cat in CATEGORIES:
        html += f'        <button class="filter-btn" onclick="filterCat(\'{cat}\')">{cat.replace("_"," ")}</button>\n'
    
    html += """    </div>
    <div class="article-table-wrapper">
    <table class="article-table" id="articleTable">
        <thead>
            <tr>
                <th>Categoría</th>
                <th>Artículo</th>
                <th>SEO</th>
                <th>GEO</th>
                <th>AEO</th>
                <th>Score</th>
                <th>Nota</th>
                <th>Words</th>
                <th>Schema</th>
                <th>AEO Block</th>
                <th>FAQ</th>
                <th>Issues</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for r in sorted_results:
        gc = get_grade_color(r["grade"])
        schema_icon = "✅" if r["seo"]["scores"].get("schema_jsonld", 0) > 50 else "❌"
        aeo_icon = "✅" if r["aeo"]["scores"].get("aeo_summary", 0) > 50 else "❌"
        faq_icon = "✅" if r["aeo"]["scores"].get("faq_schema", 0) > 50 else ("🟡" if r["aeo"]["scores"].get("faq_section", 0) > 50 else "❌")
        
        html += f"""            <tr data-cat="{r['category']}">
                <td><span class="cat-label">{r['category'].replace('_',' ')}</span></td>
                <td style="max-width:280px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="{r['title']}">{r['file']}</td>
                <td><span class="mini-badge" style="background:{get_grade_color(get_grade(r['seo']['average']))}20; color:{get_grade_color(get_grade(r['seo']['average']))};">{r['seo']['average']:.0f}</span></td>
                <td><span class="mini-badge" style="background:{get_grade_color(get_grade(r['geo']['average']))}20; color:{get_grade_color(get_grade(r['geo']['average']))};">{r['geo']['average']:.0f}</span></td>
                <td><span class="mini-badge" style="background:{get_grade_color(get_grade(r['aeo']['average']))}20; color:{get_grade_color(get_grade(r['aeo']['average']))};">{r['aeo']['average']:.0f}</span></td>
                <td><span class="mini-badge" style="background:{gc}20; color:{gc}; font-weight:700;">{r['composite_score']:.0f}</span></td>
                <td style="color:{gc}; font-weight:700;">{r['grade']}</td>
                <td style="font-family:'JetBrains Mono'; font-size:0.75rem; color:var(--text-muted);">{r['seo'].get('word_count', '—')}</td>
                <td style="text-align:center;">{schema_icon}</td>
                <td style="text-align:center;">{aeo_icon}</td>
                <td style="text-align:center;">{faq_icon}</td>
                <td style="font-family:'JetBrains Mono'; font-size:0.75rem; color:var(--text-muted);">{len(r['all_issues'])}</td>
            </tr>
"""
    
    html += """        </tbody>
    </table>
    </div>

    <!-- DIMENSION DEEP DIVE -->
    <h2 class="section-title">Análisis Dimensional</h2>
"""
    
    # SEO Deep Dive
    seo_metrics = defaultdict(list)
    geo_metrics = defaultdict(list)
    aeo_metrics = defaultdict(list)
    for r in results:
        for k, v in r["seo"]["scores"].items():
            seo_metrics[k].append(v)
        for k, v in r["geo"]["scores"].items():
            geo_metrics[k].append(v)
        for k, v in r["aeo"]["scores"].items():
            aeo_metrics[k].append(v)
    
    def metric_card(title, metrics, color):
        h = f"""
    <div class="detail-card">
        <h3 style="color:{color};">{title}</h3>
        <div class="detail-grid">
"""
        labels = {
            "title_tag": "Title Tag", "meta_description": "Meta Desc",
            "h1_tag": "H1 Tag", "heading_hierarchy": "H2 Hierarchy",
            "schema_jsonld": "Schema JSON-LD", "internal_links": "Internal Links",
            "word_count": "Word Count", "url_slug": "URL/Slug",
            "tables": "Tablas", "lists": "Listas", "data_density": "Densidad Datos",
            "blockquotes": "Blockquotes", "cross_linking": "Cross-Link", "formatting": "Formateo",
            "aeo_summary": "AEO Summary", "faq_section": "FAQ HTML", "faq_schema": "FAQ Schema",
            "question_headings": "Q-Headings", "citability": "Citabilidad"
        }
        for k, vals in metrics.items():
            avg = sum(vals) / len(vals) if vals else 0
            gc = get_grade_color(get_grade(avg))
            label = labels.get(k, k)
            h += f"""            <div class="detail-metric">
                <div class="metric-val" style="color:{gc};">{avg:.0f}</div>
                <div class="metric-label">{label}</div>
            </div>
"""
        h += """        </div>
    </div>
"""
        return h
    
    html += metric_card("SEO — Desglose por Métrica", seo_metrics, "var(--blue)")
    html += metric_card("GEO — Desglose por Métrica", geo_metrics, "var(--green)")
    html += metric_card("AEO — Desglose por Métrica", aeo_metrics, "var(--purple)")
    
    # Top / Bottom performers
    html += """
    <h2 class="section-title">Top 5 y Bottom 5</h2>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 3rem;">
        <div class="detail-card">
            <h3 style="color:var(--green);">🏆 Top 5 Performers</h3>
"""
    for i, r in enumerate(top5, 1):
        gc = get_grade_color(r["grade"])
        html += f'            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border);font-size:0.85rem;"><span>{i}. {r["file"]}</span><span style="color:{gc};font-weight:700;font-family:\'JetBrains Mono\';">{r["composite_score"]:.0f} ({r["grade"]})</span></div>\n'
    html += """        </div>
        <div class="detail-card">
            <h3 style="color:var(--red);">⚠️ Bottom 5 — Requieren Atención</h3>
"""
    for i, r in enumerate(bottom5, 1):
        gc = get_grade_color(r["grade"])
        html += f'            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border);font-size:0.85rem;"><span>{i}. {r["file"]}</span><span style="color:{gc};font-weight:700;font-family:\'JetBrains Mono\';">{r["composite_score"]:.0f} ({r["grade"]})</span></div>\n'
    html += """        </div>
    </div>
"""
    
    # FOOTER
    html += f"""
    <footer style="text-align:center; padding:2rem; border-top:1px solid var(--border); margin-top:3rem; color:var(--text-muted); font-size:0.8rem;">
        Auditoría SEO/GEO/AEO v2.0 · {total_articles} artículos analizados · {total_issues} issues detectados<br>
        Proyecto Mitta × INMedios · {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </footer>

</div>

<script>
function filterCat(cat) {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    document.querySelectorAll('#articleTable tbody tr').forEach(row => {{
        if (cat === 'all' || row.dataset.cat === cat) {{
            row.style.display = '';
        }} else {{
            row.style.display = 'none';
        }}
    }});
}}
</script>

</body>
</html>
"""
    
    return html


# ─── MAIN ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  MITTA SEO/GEO/AEO AUDIT ENGINE v2.0")
    print("=" * 60)
    print()
    
    results, cat_stats = audit_all_articles()
    
    print()
    print(f"📊 Total artículos auditados: {len(results)}")
    print()
    
    # Save JSON
    json_path = OUTPUT_DIR / "audit_seo_geo_aeo_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({"results": results, "category_stats": cat_stats, "timestamp": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
    print(f"💾 JSON guardado: {json_path}")
    
    # Generate HTML report
    html_report = generate_html_report(results, cat_stats)
    html_path = OUTPUT_DIR / "Mitta_SEO_GEO_AEO_Audit.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    print(f"📄 Reporte HTML: {html_path}")
    
    # Print summary
    print()
    print("─" * 40)
    global_avg = sum(r["composite_score"] for r in results) / max(len(results), 1)
    print(f"  SCORE GLOBAL: {global_avg:.1f}/100 ({get_grade(global_avg)})")
    print("─" * 40)
    for cat, stats in cat_stats.items():
        print(f"  {cat:30s} → {stats['avg_score']:5.1f} ({stats['grade']})")
    print("─" * 40)
    print()
    print("✅ Auditoría completada exitosamente.")
