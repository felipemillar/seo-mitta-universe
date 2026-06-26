#!/usr/bin/env python3
"""
=================================================================
 MITTA BRAND ALIGNMENT AUDIT v1.0
 Verifica que los 71 artículos cumplan las directrices de marca
=================================================================
Directrices extraídas de:
- Marco Teórico Renting MITTA GO.pptx
- Términos y Condiciones Rent a Car.docx  
- Material Leasing Operativo (LOP).pptx
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta/02_Contenidos_Redactados")

ALL_DIRS = {
    "MittaGO": BASE_DIR / "MittaGO" / "finales",
    "Mitta_Rent_a_Car": BASE_DIR / "Mitta_Rent_a_Car" / "finales",
    "Nuevos_Contenidos_2026": BASE_DIR / "Nuevos_Contenidos_2026" / "finales",
    "Cyber_2026": BASE_DIR / "Cyber_2026" / "finales",
}


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


def count_occurrences(text, pattern, flags=re.IGNORECASE):
    return len(re.findall(pattern, text, flags))


# ═══════════════════════════════════════════════════════════════
# BRAND RULES from official documents
# ═══════════════════════════════════════════════════════════════

RULES = {
    # === R1: MittaGO TERMINOLOGÍA ===
    # "Evitar completamente los términos 'arriendo', 'alquiler' o 'traslados'"
    # "Usar siempre 'Renting' o 'Suscripción'"
    "R1_MITTAGO_NO_ARRIENDO": {
        "desc": "MittaGO: NO usar 'arriendo/alquiler' — usar 'suscripción/renting'",
        "severity": "CRITICAL",
        "applies_to": ["MittaGO"],
        "forbidden_patterns": [
            r'\b(?:arrienda|arriendo|arrendando|arrendar|arrendatario)\b',
            r'\b(?:alquiler|alquilar|alquilando)\b',
            r'\b(?:traslados?)\b',
        ],
        "exceptions": [
            r'rent a car',  # OK when comparing
            r'arrendat',     # Legal terms in T&C context
            r'arriendo de autos',  # When comparing with RAC
            r'(?:vs|versus|contra|diferencia|compara)',  # Comparison context
        ]
    },
    
    # === R2: MittaGO NO ES LEASING/FINANCIAMIENTO ===
    # "No es un financiamiento con opción de compra"
    # "No confundir con Leasing"
    "R2_MITTAGO_NO_LEASING": {
        "desc": "MittaGO: NO confundir con leasing/financiamiento",
        "severity": "HIGH",
        "applies_to": ["MittaGO"],
        "check_fn": "check_leasing_confusion"
    },
    
    # === R3: TERMINOLOGÍA CORRECTA ===
    # "Arriendo Flexible" → "Renting Flexible"
    "R3_RENTING_FLEXIBLE": {
        "desc": "Usar 'Renting Flexible' (NO 'Arriendo Flexible')",
        "severity": "HIGH",
        "applies_to": ["MittaGO", "Mitta_Rent_a_Car", "Cyber_2026"],
        "forbidden_patterns": [
            r'\barriendo\s+flexible\b',
        ]
    },
    
    # === R4: DATOS FACTUALES T&C ===
    # Edad: 22 años, Garantías: $450K/$700K/$1.5M, 48hr cancelación
    "R4_EDAD_MINIMA": {
        "desc": "Edad mínima: 22 años (NO 21, NO 23, NO 25)",
        "severity": "CRITICAL",
        "applies_to": ["ALL"],
        "check_fn": "check_age_requirement"
    },
    
    "R5_GARANTIAS": {
        "desc": "Garantías: $450.000 (base), $700.000 (SUV/camioneta), $1.500.000 (zona norte 4x4)",
        "severity": "HIGH",
        "applies_to": ["ALL"],
        "check_fn": "check_guarantee_amounts"
    },
    
    "R6_CANCELACION_48H": {
        "desc": "Cancelación: 48 horas antes = 100% devolución",
        "severity": "MEDIUM",
        "applies_to": ["ALL"],
        "check_fn": "check_cancellation_policy"
    },
    
    # === R7: CATEGORÍAS, NO MODELOS ===
    # "MITTA confirma categorías de vehículos y NO modelos específicos"
    "R7_CATEGORIAS_NO_MODELOS": {
        "desc": "Mitta confirma CATEGORÍAS, no modelos/marcas específicos",
        "severity": "MEDIUM",
        "applies_to": ["Mitta_Rent_a_Car", "Cyber_2026"],
        "check_fn": "check_specific_models"
    },
    
    # === R8: DEDUCIBLE CDW ===
    # Sin deducible en colisión excepto XI y XII región (UF20)
    "R8_CDW_DEDUCIBLE": {
        "desc": "CDW: Sin deducible excepto XI/XII región (UF20)",
        "severity": "MEDIUM",
        "applies_to": ["Mitta_Rent_a_Car"],
        "check_fn": "check_cdw_info"
    },
    
    # === R9: TONO B2C vs B2B ===
    # B2C: "auto" + cercano/positivo/aspiracional
    # B2B: "vehículo/flota" + profesional/racional/técnico
    "R9_TONO_B2C": {
        "desc": "B2C: usar 'auto', tono cercano/aspiracional",
        "severity": "LOW",
        "applies_to": ["MittaGO"],
        "check_fn": "check_b2c_tone"
    },
    
    # === R10: RESPALDO MITSUI ===
    "R10_RESPALDO": {
        "desc": "Mencionar respaldo Mitsui & Co. cuando se habla de confianza",
        "severity": "LOW",
        "applies_to": ["ALL"],
        "check_fn": "check_mitsui_mention"
    },

    # === R11: KM LIBRES ===
    # "Kilometraje libre" excepto Punta Arenas 1 día (300km) y mensuales (4000km)
    "R11_KM_LIBRES": {
        "desc": "Km libres: incluidos (excepción P. Arenas 1 día=300km, mensual=4000km)",
        "severity": "MEDIUM",
        "applies_to": ["Mitta_Rent_a_Car"],
        "check_fn": "check_km_policy"
    },
    
    # === R12: SEGUNDO CONDUCTOR ===
    "R12_SEGUNDO_CONDUCTOR": {
        "desc": "Segundo conductor incluido sin costo",
        "severity": "LOW",
        "applies_to": ["Mitta_Rent_a_Car"],
        "check_fn": "check_second_driver"
    },
}


# ═══════════════════════════════════════════════════════════════
# CHECK FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def check_leasing_confusion(text, category, filename):
    """Check if MittaGO articles confuse renting with leasing."""
    violations = []
    if category != "MittaGO":
        return violations
    
    # Look for "leasing" without context of comparison
    leasing_mentions = list(re.finditer(r'\bleasing\b', text, re.IGNORECASE))
    for m in leasing_mentions:
        context = text[max(0, m.start()-100):m.end()+100].lower()
        # OK if it's in comparison context
        if any(w in context for w in ['vs', 'versus', 'diferencia', 'no es', 'compara', 'distinto']):
            continue
        # Not OK if it says MittaGO IS leasing
        if any(w in context for w in ['mittago es', 'es un leasing', 'tipo de leasing']):
            violations.append(f"Posible confusión MittaGO=leasing: '...{text[max(0,m.start()-30):m.end()+30]}...'")
    
    return violations


def check_age_requirement(text, category, filename):
    """Check that age requirement is stated as 22 years."""
    violations = []
    # Look for age mentions
    age_matches = re.findall(r'(\d{2})\s*años', text)
    for age in age_matches:
        age_int = int(age)
        if age_int in [21, 23, 25, 18] and 'edad' in text[max(0, text.find(f'{age} años')-50):text.find(f'{age} años')+50].lower():
            violations.append(f"Edad incorrecta: {age} años (debe ser 22)")
    return violations


def check_guarantee_amounts(text, category, filename):
    """Check guarantee amounts match T&C."""
    violations = []
    # Look for guarantee amounts
    amounts = re.findall(r'\$[\s]*([\d.,]+)', text)
    for amt in amounts:
        clean = amt.replace('.', '').replace(',', '')
        if clean.isdigit():
            val = int(clean)
            # Flag wrong common amounts
            if val in [500000, 600000, 800000, 900000, 1000000]:
                context_start = max(0, text.find(f'${amt}') - 80)
                context = text[context_start:context_start + 160].lower()
                if 'garantía' in context or 'garantia' in context:
                    violations.append(f"Garantía ${amt}: verificar — T&C dice $450K (base), $700K (SUV), $1.5M (zona norte)")
    return violations


def check_cancellation_policy(text, category, filename):
    """Check cancellation policy is 48 hours."""
    violations = []
    # Look for cancellation time mentions
    cancel_matches = re.findall(r'(\d+)\s*horas?\s*(?:antes|anticipación|previo|previa)', text, re.IGNORECASE)
    for hours in cancel_matches:
        if int(hours) != 48 and int(hours) != 72:  # 72 is for Argentina permit
            violations.append(f"Cancelación: dice {hours} horas (debe ser 48)")
    
    # Check for "24 horas" in cancellation context
    if re.search(r'cancel.*?24\s*horas', text, re.IGNORECASE):
        violations.append("Cancelación: dice 24 horas (debe ser 48)")
    
    return violations


def check_specific_models(text, category, filename):
    """Check if articles promise specific car models."""
    violations = []
    if category not in ["Mitta_Rent_a_Car", "Cyber_2026"]:
        return violations
    
    # Check for "recibirás un Toyota" or similar promises
    promise_patterns = [
        r'(?:recibirás|tendrás|te\s+entregaremos|te\s+asignamos)\s+(?:un|una)\s+(?:Toyota|Hyundai|Suzuki|Kia|Chevrolet|Nissan)',
        r'(?:modelo\s+exacto|marca\s+exacta|auto\s+específico)',
    ]
    for pat in promise_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            violations.append(f"Promete modelo/marca específica: '{m.group()}'")
    
    return violations


def check_cdw_info(text, category, filename):
    """Check CDW deductible information."""
    violations = []
    if category != "Mitta_Rent_a_Car":
        return violations
    
    # Check for wrong deductible amounts
    if re.search(r'deducible.*?UF\s*(\d+)', text, re.IGNORECASE):
        uf_match = re.search(r'deducible.*?UF\s*(\d+)', text, re.IGNORECASE)
        uf_val = int(uf_match.group(1))
        # Valid values: 0 (most), 20 (XI/XII), 80 (robo), 5 (furgones fríos), 3 (J2/K2/C5)
        if uf_val not in [0, 3, 5, 15, 20, 25, 80]:
            violations.append(f"Deducible UF{uf_val}: verificar contra T&C (UF0/UF20/UF80)")
    
    return violations


def check_b2c_tone(text, category, filename):
    """Check B2C tone uses 'auto' not 'vehículo'."""
    violations = []
    if category != "MittaGO":
        return violations
    
    # Check if B2C articles use mostly "vehículo" instead of "auto"
    auto_count = count_occurrences(text, r'\bauto\b')
    vehiculo_count = count_occurrences(text, r'\bvehículo\b')
    
    # B2C articles about pymes/empresas are OK with "vehículo"
    is_b2b_context = any(w in filename.lower() for w in ['pyme', 'empresa', 'corporativ', 'flota', 'leasing'])
    
    if not is_b2b_context and vehiculo_count > auto_count * 3 and vehiculo_count > 5:
        violations.append(f"Tono B2C: usa 'vehículo' ({vehiculo_count}x) más que 'auto' ({auto_count}x) — considerar ajustar")
    
    return violations


def check_mitsui_mention(text, category, filename):
    violations = []  # Not a violation, just informational
    return violations


def check_km_policy(text, category, filename):
    violations = []
    if category != "Mitta_Rent_a_Car":
        return violations
    
    # Check if mentions km limit incorrectly
    if re.search(r'(?:200|250|150)\s*(?:km|kilómetros)\s*(?:libres|incluidos)', text, re.IGNORECASE):
        violations.append("Km libres: monto incorrecto (T&C dice km libre, excepto P.Arenas 1d=300km)")
    
    return violations


def check_second_driver(text, category, filename):
    violations = []
    # Check for wrong info about second driver
    if re.search(r'segundo\s+conductor.*?(?:costo|cargo|recargo|pagar)', text, re.IGNORECASE):
        context = re.search(r'segundo\s+conductor.*?(?:costo|cargo|recargo|pagar).{0,50}', text, re.IGNORECASE)
        if context and 'sin costo' not in context.group().lower() and 'gratis' not in context.group().lower() and 'incluido' not in context.group().lower():
            violations.append("Segundo conductor: T&C dice 'sin costo' — verificar redacción")
    return violations


# ═══════════════════════════════════════════════════════════════
# MAIN AUDIT
# ═══════════════════════════════════════════════════════════════

def audit_article(filepath, category):
    """Audit a single article against all applicable rules."""
    content = filepath.read_text(encoding='utf-8')
    text = strip_tags(content).lower()
    findings = []
    
    for rule_id, rule in RULES.items():
        applies = rule["applies_to"]
        if "ALL" not in applies and category not in applies:
            continue
        
        violations = []
        
        # Pattern-based checks
        if "forbidden_patterns" in rule:
            exceptions = rule.get("exceptions", [])
            for pat in rule["forbidden_patterns"]:
                for m in re.finditer(pat, text, re.IGNORECASE):
                    # Check context for exceptions
                    context = text[max(0, m.start()-80):m.end()+80]
                    is_exception = False
                    for exc in exceptions:
                        if re.search(exc, context, re.IGNORECASE):
                            is_exception = True
                            break
                    if not is_exception:
                        word = m.group()
                        line_start = text.rfind('\n', 0, m.start()) + 1
                        line_end = text.find('\n', m.end())
                        if line_end == -1: line_end = m.end() + 50
                        snippet = text[line_start:min(line_end, line_start+120)].strip()
                        violations.append(f"'{word}' → ...{snippet}...")
        
        # Function-based checks
        if "check_fn" in rule:
            fn = globals().get(rule["check_fn"])
            if fn:
                violations.extend(fn(text, category, filepath.name))
        
        if violations:
            findings.append({
                "rule_id": rule_id,
                "desc": rule["desc"],
                "severity": rule["severity"],
                "violations": violations
            })
    
    return findings


def main():
    print("="*70)
    print("  MITTA BRAND ALIGNMENT AUDIT v1.0")
    print("  Verificación contra directrices oficiales")
    print("="*70)
    
    all_findings = {}
    summary = defaultdict(lambda: {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "articles_clean": 0})
    total_violations = 0
    
    for cat_name, cat_dir in ALL_DIRS.items():
        print(f"\n{'─'*70}")
        print(f"  📂 {cat_name}")
        print(f"{'─'*70}")
        
        for fpath in sorted(cat_dir.glob("*.html")):
            findings = audit_article(fpath, cat_name)
            
            if findings:
                v_count = sum(len(f["violations"]) for f in findings)
                total_violations += v_count
                severity_counts = defaultdict(int)
                for f in findings:
                    severity_counts[f["severity"]] += len(f["violations"])
                    summary[cat_name][f["severity"].lower()] += len(f["violations"])
                
                summary[cat_name]["total"] += v_count
                
                # Print findings
                crit = severity_counts.get("CRITICAL", 0)
                high = severity_counts.get("HIGH", 0)
                severity_str = ""
                if crit > 0: severity_str += f" 🔴{crit}"
                if high > 0: severity_str += f" 🟠{high}"
                
                print(f"  ⚠️  {fpath.name}: {v_count} hallazgos{severity_str}")
                for f in findings:
                    icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "⚪"}.get(f["severity"], "⚪")
                    print(f"      {icon} [{f['rule_id']}] {f['desc']}")
                    for v in f["violations"][:3]:  # Show max 3
                        print(f"         → {v[:100]}")
                    if len(f["violations"]) > 3:
                        print(f"         → ... y {len(f['violations'])-3} más")
                
                all_findings[fpath.name] = findings
            else:
                summary[cat_name]["articles_clean"] += 1
                print(f"  ✅ {fpath.name}: alineado")
    
    # Summary
    print(f"\n{'='*70}")
    print(f"  RESUMEN DE ALINEACIÓN DE MARCA")
    print(f"{'='*70}")
    
    for cat, s in summary.items():
        clean_pct = (s["articles_clean"] / max(s["articles_clean"] + len([k for k,v in all_findings.items()]), 1)) * 100
        print(f"\n  {cat}:")
        print(f"    Total hallazgos: {s['total']} (🔴{s['critical']} 🟠{s['high']} 🟡{s['medium']} ⚪{s['low']})")
    
    print(f"\n  {'─'*50}")
    print(f"  TOTAL VIOLACIONES: {total_violations}")
    print(f"  ARTÍCULOS LIMPIOS: {sum(s['articles_clean'] for s in summary.values())}/71")
    
    # Save JSON results
    output_path = Path("/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta/04_Auditorias_y_Reportes/brand_alignment_audit.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": str(__import__('datetime').datetime.now()),
            "total_violations": total_violations,
            "findings_by_file": {k: [{"rule": fi["rule_id"], "severity": fi["severity"], "count": len(fi["violations"]), "samples": fi["violations"][:3]} for fi in v] for k,v in all_findings.items()},
            "summary": dict(summary)
        }, f, ensure_ascii=False, indent=2)
    print(f"\n  💾 JSON: {output_path}")


if __name__ == "__main__":
    main()
