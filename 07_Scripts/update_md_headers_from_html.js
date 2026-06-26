const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const CONTENIDOS = path.join(ROOT, '02_Contenidos_Redactados');

console.log("=== INICIANDO ACTUALIZACIÓN DE HEADERS DE ARCHIVOS MD ===");

const brands = [
    { key: 'mittago', label: 'MittaGO', path: path.join(CONTENIDOS, 'MittaGO') },
    { key: 'rentacar', label: 'Mitta Rent a Car', path: path.join(CONTENIDOS, 'Mitta_Rent_a_Car') },
    { key: 'cyber', label: 'Cyber 2026', path: path.join(CONTENIDOS, 'Cyber_2026') }
];

let updatedCount = 0;
let errorsCount = 0;

brands.forEach(b => {
    const finalesPath = path.join(b.path, 'finales');
    const borradoresPath = path.join(b.path, 'borradores');
    
    if (!fs.existsSync(finalesPath) || !fs.existsSync(borradoresPath)) {
        console.warn(`[WARN] No existe la carpeta de finales o borradores para ${b.label}`);
        return;
    }

    const htmlFiles = fs.readdirSync(finalesPath).filter(f => f.endsWith('.html'));
    
    htmlFiles.forEach(f => {
        const htmlContent = fs.readFileSync(path.join(finalesPath, f), 'utf8');

        // Extraer metadatos desde el HTML final optimizado
        const titleMatch = htmlContent.match(/<title>(.*?)<\/title>/);
        const metaTitle = titleMatch ? titleMatch[1].trim() : '';

        const descMatch = htmlContent.match(/<meta\s+name="description"\s+content="(.*?)"/i);
        const metaDescription = descMatch ? descMatch[1].trim() : '';

        const keywordsMatch = htmlContent.match(/<meta\s+name="keywords"\s+content="(.*?)"/i);
        const keywords = keywordsMatch ? keywordsMatch[1].trim() : '';

        const pilarMatch = htmlContent.match(/<strong>Pilar:<\/strong>\s*(.*?)(?:<\/div>|$)/i);
        const pilar = pilarMatch ? pilarMatch[1].replace(/<[^>]*>/g, '').trim() : 'General';

        const brandMatch = htmlContent.match(/<strong>Marca:<\/strong>\s*(.*?)(?:<\/div>|$)/i);
        const marca = brandMatch ? brandMatch[1].replace(/<[^>]*>/g, '').trim() : b.label;

        const slugMatch = htmlContent.match(/<strong>Ruta\/Slug:<\/strong>\s*(.*?)(?:<\/div>|$)/i) || 
                          htmlContent.match(/<strong>Slug:<\/strong>\s*(.*?)(?:<\/div>|$)/i);
        const slug = slugMatch ? slugMatch[1].replace(/<[^>]*>/g, '').trim() : '';

        const h1Match = htmlContent.match(/<h1>(.*?)<\/h1>/i);
        const titulo = h1Match ? h1Match[1].replace(/<[^>]*>/g, '').trim() : '';

        // Buscar el archivo MD correspondiente en borradores/
        const id = f.replace('.html', '').replace(/_v2$/, '');
        const mdFiles = fs.readdirSync(borradoresPath);
        const mdFileName = mdFiles.find(m => {
            const base = m.replace('.md', '');
            return base === id || base === id + '_v2' || m === f.replace('.html', '.md');
        });

        if (!mdFileName) {
            console.error(`[ERROR] No se encontró archivo markdown borrador para el HTML: ${f}`);
            errorsCount++;
            return;
        }

        const mdPath = path.join(borradoresPath, mdFileName);
        const mdContent = fs.readFileSync(mdPath, 'utf8');

        // Extraer formato y segmento del frontmatter viejo
        let oldFm = {};
        if (mdContent.startsWith('---')) {
            const endIdx = mdContent.indexOf('---', 3);
            if (endIdx !== -1) {
                const fmText = mdContent.substring(3, endIdx);
                fmText.split('\n').forEach(line => {
                    const colonIdx = line.indexOf(':');
                    if (colonIdx !== -1) {
                        const k = line.substring(0, colonIdx).trim();
                        let v = line.substring(colonIdx + 1).trim();
                        v = v.replace(/^\[|]$/g, '').replace(/["']/g, '').trim();
                        oldFm[k] = v;
                    }
                });
            }
        }

        const formatoSignature = oldFm.formato_signature || oldFm.formato || 'General';
        const segmento = oldFm.segmento || 'B2C';

        // Extraer el cuerpo original del MD (después del segundo ---)
        const endOfFmIdx = mdContent.indexOf('---', 3);
        let body = mdContent;
        if (mdContent.startsWith('---') && endOfFmIdx !== -1) {
            body = mdContent.substring(endOfFmIdx + 3).trim();
        }

        // Construir el nuevo header YAML estandarizado exactamente en el formato solicitado
        const newFm = `---
titulo: "${titulo}"
slug: "${slug}"
meta_title: "${metaTitle}"
meta_description: "${metaDescription}"
keywords: "${keywords}"
marca: "${marca}"
pilar: "${pilar}"
formato_signature: "${formatoSignature}"
segmento: "${segmento}"
---

`;

        const finalContent = newFm + body;
        if (finalContent !== mdContent) {
            fs.writeFileSync(mdPath, finalContent, 'utf8');
            console.log(`[OK] Actualizados metadatos de borrador MD: ${mdFileName}`);
            updatedCount++;
        } else {
            console.log(`[SKIP] Sin cambios de formato en: ${mdFileName}`);
        }
    });
});

console.log("\n=== RESUMEN DE PROCESO ===");
console.log(`Borradores MD actualizados con éxito: ${updatedCount}`);
console.log(`Errores: ${errorsCount}`);
console.log("===========================");
