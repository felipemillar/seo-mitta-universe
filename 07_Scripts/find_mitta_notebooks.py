import json

file_path = '/Users/fmillar/.gemini/antigravity/brain/dd00f0eb-a29f-4cbd-bdad-102481305479/.system_generated/steps/5/output.txt'

with open(file_path, 'r') as f:
    data = json.load(f)

keywords = ['mitta', 'rental', 'leasing', 'vehiculo', 'vehicle', 'chile']
results = []

for nb in data.get('notebooks', []):
    title = nb.get('title', '').lower()
    if any(kw in title for kw in keywords):
        results.append(nb)

print(json.dumps(results, indent=2))
