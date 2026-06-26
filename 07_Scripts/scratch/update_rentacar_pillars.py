import os
import re

ROOT_DIR = "/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta"
BORRADORES_DIR = os.path.join(ROOT_DIR, "02_Contenidos_Redactados/Mitta_Rent_a_Car/borradores")
FINALES_DIR = os.path.join(ROOT_DIR, "02_Contenidos_Redactados/Mitta_Rent_a_Car/finales")

def get_new_pilar(num):
    if num in [16, 17, 18, 19, 20]:
        return "Pilar 4: Notas de Utilidad (Evergreen & Tips)"
    else:
        return "Pilar 1: Rent a Car (Foco B2C y Turismo)"

def update_markdown_files():
    if not os.path.exists(BORRADORES_DIR):
        print(f"Directory {BORRADORES_DIR} does not exist.")
        return
    
    files = [f for f in os.listdir(BORRADORES_DIR) if f.endswith('.md')]
    for file in files:
        # Extract number from filename (e.g. "01_Guia_Arriendo_Aeropuertos_v2.md" -> 1)
        match = re.match(r"^(\d+)", file)
        if not match:
            continue
        
        num = int(match.group(1))
        new_pilar = get_new_pilar(num)
        
        filepath = os.path.join(BORRADORES_DIR, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update frontmatter pilar: "..."
        # Match lines like: pilar: "..." or pilar: '...' or pilar: ...
        pattern = r"pilar:\s*[\"']?(.*?)[\"']?\s*$"
        
        # We need to find if there is a pilar line
        lines = content.split('\n')
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith('pilar:'):
                lines[i] = f'pilar: "{new_pilar}"'
                updated = True
                break
                
        if updated:
            new_content = '\n'.join(lines)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated md pilar for {file} to: {new_pilar}")
        else:
            print(f"Could not find pilar line in md file: {file}")

def update_html_files():
    if not os.path.exists(FINALES_DIR):
        print(f"Directory {FINALES_DIR} does not exist.")
        return
    
    files = [f for f in os.listdir(FINALES_DIR) if f.endswith('.html')]
    for file in files:
        match = re.match(r"^(\d+)", file)
        if not match:
            continue
        
        num = int(match.group(1))
        new_pilar = get_new_pilar(num)
        
        filepath = os.path.join(FINALES_DIR, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # We want to replace either:
        # <div><strong>Pilar:</strong> ...</div> or <div><strong>Categoria:</strong> ...</div>
        # with <div><strong>Pilar:</strong> [new_pilar]</div>
        
        # Let's use regex for robust replacement
        pilar_pattern = r"<div><strong>Pilar:</strong>\s*(.*?)</div>"
        categoria_pattern = r"<div><strong>Categoria:</strong>\s*(.*?)</div>"
        
        new_content = content
        replaced = False
        
        if re.search(pilar_pattern, new_content):
            new_content = re.sub(pilar_pattern, f"<div><strong>Pilar:</strong> {new_pilar}</div>", new_content)
            replaced = True
        elif re.search(categoria_pattern, new_content):
            new_content = re.sub(categoria_pattern, f"<div><strong>Pilar:</strong> {new_pilar}</div>", new_content)
            replaced = True
            
        if replaced:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated html pilar for {file} to: {new_pilar}")
        else:
            print(f"Could not find Pilar/Categoria block in html file: {file}")

if __name__ == "__main__":
    print("Updating Rent a Car draft files (Markdown)...")
    update_markdown_files()
    print("\nUpdating Rent a Car final files (HTML)...")
    update_html_files()
    print("\nUpdate completed!")
