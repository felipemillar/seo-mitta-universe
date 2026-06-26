#!/usr/bin/env python3
"""
Auditoría automatizada de terminología y datos factuales
en todos los contenidos de blog Mitta/MittaGO.

Reglas verificadas:
  R1: Terminología prohibida en MittaGO ("arriendo","alquiler","traslados" en cuerpo)
  R2: "Renting Financiero" / "Leasing Financiero" como producto Mitta
  R3: "Arriendo Flexible" en comparaciones con créditos
  R4: Confusión entre unidades de negocio (Leasing vs RAC vs Renting)
  R5: Datos factuales incorrectos vs T&C
"""

import os, re, json
from collections import defaultdict

BASE = "/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta/02_Contenidos_Redactados"

# ── Carpetas a escanear ───────────────────────────────────────────────
SCAN_DIRS = {
    "MittaGO": os.path.join(BASE, "MittaGO"),
    "Rent_a_Car": os.path.join(BASE, "Mitta_Rent_a_Car"),
    "Nuevos_2026": os.path.join(BASE, "Nuevos_Contenidos_2026"),
    "Cyber_2026": os.path.join(BASE, "Cyber_2026"),
}

# ── Reglas ────────────────────────────────────────────────────────────

def is_metadata_line(line):
    """Check if a line is YAML frontmatter, meta tag, or comment."""
    stripped = line.strip().lower()
    return any([
        stripped.startswith("meta_"),
        stripped.startswith("keywords:"),
        stripped.startswith("slug:"),
        stripped.startswith("titulo:"),
        stripped.startswith("<meta"),
        stripped.startswith("<title"),
        stripped.startswith("<!-- "),
        stripped.startswith("description:"),
    ])


def check_R1_mittago_terminology(filepath, lines, marca):
    """R1: Terminología prohibida en MittaGO."""
    if marca != "MittaGO":
        return []
    
    violations = []
    prohibited = [
        (r'\barriendo\b', "arriendo"),
        (r'\barriendos\b', "arriendos"),
        (r'\balquiler\b', "alquiler"),
        (r'\balquilar\b', "alquilar"),
        (r'\btraslados?\b', "traslado(s)"),
    ]
    
    for i, line in enumerate(lines, 1):
        if is_metadata_line(line):
            continue
        for pattern, term in prohibited:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for m in matches:
                # Exception: when used in explicit comparison with Rent a Car
                context = line[max(0, m.start()-40):m.end()+40].strip()
                if "rent a car" in context.lower() and ("diferencia" in context.lower() or "vs" in context.lower() or "comparad" in context.lower()):
                    continue
                violations.append({
                    "rule": "R1",
                    "line": i,
                    "term": term,
                    "context": context,
                    "severity": "HIGH",
                    "fix": f'Reemplazar "{term}" por "suscripción" o "renting"'
                })
    return violations


def check_R2_renting_financiero(filepath, lines, marca):
    """R2: 'Renting Financiero' / 'Leasing Financiero' como producto Mitta."""
    violations = []
    patterns = [
        (r'renting\s+financiero', "Renting Financiero"),
        (r'leasing\s+financiero', "Leasing Financiero"),
        (r'arriendo\s+financiero', "Arriendo Financiero"),
    ]
    
    for i, line in enumerate(lines, 1):
        for pattern, term in patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for m in matches:
                context = line[max(0, m.start()-40):m.end()+40].strip()
                violations.append({
                    "rule": "R2",
                    "line": i,
                    "term": term,
                    "context": context,
                    "severity": "CRITICAL",
                    "fix": f'Eliminar referencia a "{term}" — NO es un producto de Mitta'
                })
    return violations


def check_R3_arriendo_flexible(filepath, lines, marca):
    """R3: 'Arriendo Flexible' en comparaciones con créditos."""
    violations = []
    
    for i, line in enumerate(lines, 1):
        matches = re.finditer(r'arriendo\s+flexible', line, re.IGNORECASE)
        for m in matches:
            context = line[max(0, m.start()-40):m.end()+40].strip()
            violations.append({
                "rule": "R3",
                "line": i,
                "term": "Arriendo Flexible",
                "context": context,
                "severity": "HIGH",
                "fix": 'Reemplazar por "Renting Flexible" o "Suscripción Flexible"'
            })
    return violations


def check_R4_unit_confusion(filepath, lines, marca):
    """R4: Confusión entre unidades de negocio en artículos nuevos de RAC."""
    if marca != "Rent_a_Car":
        return []
    
    fname = os.path.basename(filepath)
    # Only check articles 21-30
    num_match = re.match(r'^(\d+)_', fname)
    if not num_match:
        return []
    num = int(num_match.group(1))
    if num < 21 or num > 30:
        return []
    
    violations = []
    is_leasing = num <= 25  # 21-25 are Leasing Operativo
    is_renting = num >= 26  # 26-30 are Renting Flexible
    
    for i, line in enumerate(lines, 1):
        # In Leasing articles, check if they mention "Rent a Car" features as their own
        if is_leasing and re.search(r'arriendo\s+diario|corto\s+plazo|turismo', line, re.IGNORECASE):
            context = line.strip()[:120]
            violations.append({
                "rule": "R4",
                "line": i,
                "term": "Feature de RAC en artículo de LOP",
                "context": context,
                "severity": "MEDIUM",
                "fix": "Verificar que no se mezclen features de Rent a Car con Leasing Operativo"
            })
        
        # In Renting Flexible articles, check for Leasing language
        if is_renting and re.search(r'leasing\s+operativo|flota\s+corporativ|largo\s+plazo', line, re.IGNORECASE):
            context = line.strip()[:120]
            violations.append({
                "rule": "R4",
                "line": i,
                "term": "Feature de LOP en artículo de Renting",
                "context": context,
                "severity": "MEDIUM",
                "fix": "Verificar que no se mezclen features de Leasing Operativo con Renting Flexible"
            })
    
    return violations


def check_R5_factual_data(filepath, lines, marca):
    """R5: Datos factuales incorrectos vs T&C Rent a Car."""
    if marca not in ("Rent_a_Car", "Cyber_2026"):
        return []
    
    violations = []
    
    for i, line in enumerate(lines, 1):
        lower = line.lower()
        
        # Wrong minimum age
        if re.search(r'mayor\s+de\s+(18|21|25|23)\s+años', lower):
            if "22" not in lower:
                context = line.strip()[:120]
                violations.append({
                    "rule": "R5",
                    "line": i,
                    "term": "Edad mínima incorrecta",
                    "context": context,
                    "severity": "HIGH",
                    "fix": "Edad mínima correcta: 22 años (según T&C oficial)"
                })
        
        # Wrong guarantee amounts
        if re.search(r'garant[ií]a.*\$\s*[0-9]', lower):
            if re.search(r'\$\s*(300|350|400|500)\.000', lower) and not re.search(r'\$\s*450\.000', lower):
                context = line.strip()[:120]
                violations.append({
                    "rule": "R5",
                    "line": i,
                    "term": "Monto garantía posiblemente incorrecto",
                    "context": context,
                    "severity": "MEDIUM",
                    "fix": "Garantía mínima: $450.000 (autos), $700.000 (SUV/camionetas), $1.500.000 (4x4 zona norte)"
                })
        
        # Wrong cancellation policy
        if re.search(r'(24|72)\s+horas.*cancel|cancel.*\b(24|72)\b\s+horas', lower):
            if "48" not in lower:
                context = line.strip()[:120]
                violations.append({
                    "rule": "R5",
                    "line": i,
                    "term": "Plazo de cancelación posiblemente incorrecto",
                    "context": context,
                    "severity": "MEDIUM",
                    "fix": "Cancelación: 48 horas antes = 100% reembolso (según T&C)"
                })
    
    return violations


# ── Motor de escaneo ──────────────────────────────────────────────────

def scan_file(filepath, marca):
    """Run all rules against a single file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return [{"rule": "ERROR", "line": 0, "term": str(e), "context": "", "severity": "ERROR", "fix": ""}]
    
    violations = []
    violations.extend(check_R1_mittago_terminology(filepath, lines, marca))
    violations.extend(check_R2_renting_financiero(filepath, lines, marca))
    violations.extend(check_R3_arriendo_flexible(filepath, lines, marca))
    violations.extend(check_R4_unit_confusion(filepath, lines, marca))
    violations.extend(check_R5_factual_data(filepath, lines, marca))
    
    return violations


def main():
    print("🔍 Auditoría de Terminología y Datos Factuales — Mitta Blog\n")
    
    all_results = {}
    stats = defaultdict(int)
    severity_counts = defaultdict(int)
    rule_counts = defaultdict(int)
    
    for marca, base_dir in SCAN_DIRS.items():
        for root, dirs, files in os.walk(base_dir):
            for fname in sorted(files):
                if not fname.endswith(('.md', '.html')):
                    continue
                filepath = os.path.join(root, fname)
                violations = scan_file(filepath, marca)
                
                if violations:
                    rel_path = os.path.relpath(filepath, os.path.dirname(BASE))
                    all_results[rel_path] = violations
                    stats[marca] += len(violations)
                    for v in violations:
                        severity_counts[v["severity"]] += 1
                        rule_counts[v["rule"]] += 1
    
    # ── Print Summary ─────────────────────────────────────────────────
    total = sum(stats.values())
    print(f"📊 Total infracciones encontradas: {total}")
    print(f"   Archivos afectados: {len(all_results)}")
    print()
    
    print("📁 Por marca:")
    for marca, count in sorted(stats.items()):
        print(f"   {marca}: {count}")
    print()
    
    print("🚨 Por severidad:")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if sev in severity_counts:
            print(f"   {sev}: {severity_counts[sev]}")
    print()
    
    print("📋 Por regla:")
    rule_names = {
        "R1": "Terminología prohibida MittaGO",
        "R2": "Renting/Leasing Financiero",
        "R3": "Arriendo Flexible",
        "R4": "Confusión unidades de negocio",
        "R5": "Datos factuales vs T&C",
    }
    for rule in sorted(rule_counts.keys()):
        name = rule_names.get(rule, rule)
        print(f"   {rule} ({name}): {rule_counts[rule]}")
    print()
    
    # ── Top 15 most affected files ────────────────────────────────────
    print("📄 Top 15 archivos más afectados:")
    sorted_files = sorted(all_results.items(), key=lambda x: len(x[1]), reverse=True)
    for fpath, violations in sorted_files[:15]:
        crits = sum(1 for v in violations if v["severity"] == "CRITICAL")
        highs = sum(1 for v in violations if v["severity"] == "HIGH")
        meds = sum(1 for v in violations if v["severity"] == "MEDIUM")
        print(f"   {os.path.basename(fpath)}: {len(violations)} total ({crits}C/{highs}H/{meds}M)")
    print()
    
    # ── Save JSON report ──────────────────────────────────────────────
    report = {
        "generated_at": "2026-06-26",
        "total_violations": total,
        "files_affected": len(all_results),
        "stats_by_marca": dict(stats),
        "stats_by_severity": dict(severity_counts),
        "stats_by_rule": dict(rule_counts),
        "violations": all_results,
    }
    
    out_path = os.path.join(os.path.dirname(BASE), "04_Auditorias_y_Reportes", "audit_terminology_junio_2026.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Reporte guardado en: {out_path}")


if __name__ == "__main__":
    main()
