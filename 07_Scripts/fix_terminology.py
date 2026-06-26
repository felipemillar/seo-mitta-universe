#!/usr/bin/env python3
"""
Corrección automatizada de terminología en borradores MittaGO.
Aplica reglas R1 (terminología prohibida) y R3 (Arriendo Flexible).

NOTA: No modifica metadatos YAML/meta tags (preserva keywords SEO).
Solo corrige el cuerpo visible del texto.
"""

import os, re, sys
from datetime import datetime

BASE = "/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta/02_Contenidos_Redactados"

# ── Definición de zonas protegidas ────────────────────────────────────

def is_protected_line(line):
    """Lines that should NOT be modified (SEO metadata, schema, etc.)."""
    stripped = line.strip().lower()
    return any([
        stripped.startswith("meta_"),
        stripped.startswith("keywords"),
        stripped.startswith("keyword_principal"),
        stripped.startswith("slug:"),
        stripped.startswith("titulo:"),
        stripped.startswith("<meta"),
        stripped.startswith("<title"),
        stripped.startswith("<!-- aeo-"),
        stripped.startswith('"description"'),
        stripped.startswith('"headline"'),
        stripped.startswith('"name"'),
        stripped.startswith('"text"'),
        stripped.startswith('"url"'),
        stripped.startswith('"@'),
        # YAML frontmatter boundary
        stripped == "---",
    ])


def is_in_frontmatter(lines, line_idx):
    """Check if line_idx is inside YAML frontmatter (between first and second ---)."""
    fm_count = 0
    for i in range(line_idx):
        if lines[i].strip() == "---":
            fm_count += 1
    return fm_count == 1  # Inside first pair of ---


def is_in_schema(lines, line_idx):
    """Check if line_idx is inside a JSON-LD schema block."""
    in_schema = False
    for i in range(line_idx):
        if '<script type="application/ld+json">' in lines[i]:
            in_schema = True
        if '</script>' in lines[i] and in_schema:
            in_schema = False
    return in_schema


# ── Reglas de reemplazo ───────────────────────────────────────────────

REPLACEMENTS_MITTAGO = [
    # R3: Arriendo Flexible → Renting Flexible / Suscripción Flexible
    (r'\barriendo\s+flexible\b', 'Renting Flexible', re.IGNORECASE),
    (r'\barriendos\s+flexibles\b', 'Renting Flexibles', re.IGNORECASE),
    
    # R1: specific compound phrases first (order matters!)
    (r'\barriendo\s+mensual\b', 'suscripción mensual', re.IGNORECASE),
    (r'\barriendo\s+de\s+autos?\b', 'suscripción de autos', re.IGNORECASE),
    (r'\barriendo\s+vehicular\b', 'suscripción vehicular', re.IGNORECASE),
    (r'\barriendo\s+por\s+suscripción\b', 'suscripción', re.IGNORECASE),
    (r'\bel\s+arriendo\b', 'la suscripción', re.IGNORECASE),
    (r'\bdel\s+arriendo\b', 'de la suscripción', re.IGNORECASE),
    (r'\bun\s+arriendo\b', 'una suscripción', re.IGNORECASE),
    (r'\btipo\s+arriendo\b', 'tipo suscripción', re.IGNORECASE),
    (r'\bmodelo\s+de\s+arriendo\b', 'modelo de suscripción', re.IGNORECASE),
    (r'\bcontrato\s+de\s+arriendo\b', 'contrato de suscripción', re.IGNORECASE),
    
    # R1: generic "arriendo" as standalone (only if not followed by context clues for RAC)
    # We use a negative lookahead for RAC-specific terms
    (r'\barriendos?\b(?!\s+(diario|corto|rent|de vehículos en))', 'suscripción', re.IGNORECASE),
    
    # R1: alquiler variants
    (r'\balquilar\b', 'suscribir', re.IGNORECASE),
    (r'\balquiler\b', 'suscripción', re.IGNORECASE),
]


def apply_corrections(filepath, marca):
    """Apply terminology corrections to a single file."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    changes = []
    new_lines = []
    
    for i, line in enumerate(lines):
        original = line
        
        # Skip protected zones
        if is_protected_line(line) or is_in_frontmatter(lines, i) or is_in_schema(lines, i):
            new_lines.append(line)
            continue
        
        # Apply MittaGO-specific replacements
        if marca == "MittaGO":
            for pattern, replacement, flags in REPLACEMENTS_MITTAGO:
                new_line = re.sub(pattern, replacement, line, flags=flags)
                if new_line != line:
                    line = new_line
        
        # Apply universal replacements (R3: Arriendo Flexible → across all brands)
        if marca != "MittaGO":
            line = re.sub(r'\barriendo\s+flexible\b', 'Renting Flexible', line, flags=re.IGNORECASE)
            line = re.sub(r'\barriendos\s+flexibles\b', 'Renting Flexibles', line, flags=re.IGNORECASE)
        
        if line != original:
            changes.append({
                "line": i + 1,
                "before": original.strip(),
                "after": line.strip(),
            })
        
        new_lines.append(line)
    
    if changes:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    
    return changes


# ── Main ──────────────────────────────────────────────────────────────

def main():
    print("🔧 Corrección automatizada de terminología\n")
    
    targets = [
        ("MittaGO", os.path.join(BASE, "MittaGO", "borradores")),
        ("Nuevos_2026", os.path.join(BASE, "Nuevos_Contenidos_2026", "borradores")),
        ("Rent_a_Car", os.path.join(BASE, "Mitta_Rent_a_Car", "borradores")),
        ("Cyber_2026", os.path.join(BASE, "Cyber_2026", "borradores")),
    ]
    
    total_files = 0
    total_changes = 0
    log_lines = []
    
    for marca, borradores_dir in targets:
        if not os.path.exists(borradores_dir):
            continue
        
        md_files = sorted([f for f in os.listdir(borradores_dir) if f.endswith('.md')])
        
        for fname in md_files:
            filepath = os.path.join(borradores_dir, fname)
            changes = apply_corrections(filepath, marca)
            
            if changes:
                total_files += 1
                total_changes += len(changes)
                print(f"  ✏️  {marca}/{fname}: {len(changes)} correcciones")
                for c in changes[:3]:  # Show first 3
                    print(f"      L{c['line']}: \"{c['before'][:60]}...\"")
                    print(f"          → \"{c['after'][:60]}...\"")
                if len(changes) > 3:
                    print(f"      ... y {len(changes)-3} más")
                
                log_lines.append(f"- **{marca}/{fname}**: {len(changes)} correcciones")
    
    print(f"\n📊 Resumen: {total_changes} correcciones en {total_files} archivos")
    
    # Save correction log
    log_path = os.path.join(BASE, "..", "04_Auditorias_y_Reportes", "correction_log_junio_2026.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# Log de Correcciones Automatizadas — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Total**: {total_changes} correcciones en {total_files} archivos\n\n")
        f.write("## Archivos corregidos\n\n")
        for line in log_lines:
            f.write(f"{line}\n")
    
    print(f"📝 Log guardado en: {log_path}")


if __name__ == "__main__":
    main()
