const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.join(__dirname, '..');
const CONTENIDOS = path.join(ROOT, '02_Contenidos_Redactados');
const PORTAL_PATH = path.join(ROOT, 'Portal_Contenidos_Offline.html');

console.log("=== INICIANDO ACTUALIZACIÓN DE METADATOS DE ARTÍCULOS ===");
console.log(`Leyendo portal offline: ${PORTAL_PATH}`);

if (!fs.existsSync(PORTAL_PATH)) {
    console.error("Error: No existe el archivo Portal_Contenidos_Offline.html en la raíz.");
    process.exit(1);
}

const portalHtml = fs.readFileSync(PORTAL_PATH, 'utf8');

// 1. Extraer el objeto ARTICLES de los scripts del portal de forma robusta
const scriptMatch = portalHtml.match(/const ARTICLES = \{[\s\S]*?\n\s*\};\s*\n\s*function showArticle/);
if (!scriptMatch) {
    console.error("Error: No se pudo encontrar el objeto ARTICLES en el portal offline.");
    process.exit(1);
}

let code = scriptMatch[0].replace(/\s*function showArticle\s*$/, '').trim();
// Reemplazar 'const ARTICLES =' con 'globalThis.ARTICLES =' para que se declare en el sandbox
const codeToRun = code.replace(/^const ARTICLES\s*=/, 'globalThis.ARTICLES =');

const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(codeToRun, sandbox);
const articles = sandbox.ARTICLES;

const keys = Object.keys(articles);
console.log(`Cargados ${keys.length} artículos desde el portal offline.`);

// 2. Mapear carpetas de marcas
const folderMap = {
    'MittaGO': path.join(CONTENIDOS, 'MittaGO', 'finales'),
    'Mitta Rent a Car': path.join(CONTENIDOS, 'Mitta_Rent_a_Car', 'finales'),
    'Cyber 2026 (Borradores)': path.join(CONTENIDOS, 'Cyber_2026', 'finales')
};

// Helper para encontrar el archivo HTML real (considerando _v2 y extensiones)
function findHtmlFile(folderPath, id) {
    if (!fs.existsSync(folderPath)) return null;
    const files = fs.readdirSync(folderPath);
    const match = files.find(f => {
        const base = f.replace('.html', '');
        return base === id || base === id + '_v2';
    });
    return match ? path.join(folderPath, match) : null;
}

// Helper para extraer el slug de la cabecera actual, del JSON-LD, o generar fallback
function getSlug(htmlContent, id) {
    // 1. Buscar en el meta-header actual
    const slugMatch = htmlContent.match(/<strong>Ruta\/Slug:<\/strong>\s*(.*?)(?:<\/div>|$)/i) || 
                       htmlContent.match(/<strong>Slug:<\/strong>\s*(.*?)(?:<\/div>|$)/i);
    if (slugMatch && slugMatch[1].trim()) {
        const extracted = slugMatch[1].replace(/<[^>]*>/g, '').trim(); // Limpiar tags <a>
        if (extracted) return extracted;
    }

    // 2. Buscar en JSON-LD (mainEntityOfPage)
    const jsonLdMatch = htmlContent.match(/"mainEntityOfPage"\s*:\s*\{\s*"@type"\s*:\s*"WebPage"\s*,\s*"@id"\s*:\s*"(.*?)"/s);
    if (jsonLdMatch && jsonLdMatch[1]) {
        const url = jsonLdMatch[1].trim();
        const urlPathMatch = url.match(/https?:\/\/[^\/]+(\/.*)/);
        if (urlPathMatch && urlPathMatch[1]) {
            return urlPathMatch[1];
        }
    }

    // 3. Fallback basado en el ID
    const slugified = id.toLowerCase().replace(/_/g, '-').replace(/^\d+-/, '');
    return `/${slugified}/`;
}

// Helper para extraer keywords de los tag-pills existentes
function getKeywords(htmlContent) {
    const pills = [];
    const pillRegex = /<span class="tag-pill">(.*?)<\/span>/gi;
    let match;
    while ((match = pillRegex.exec(htmlContent)) !== null) {
        const tag = match[1].trim();
        if (tag && tag !== 'B2C' && tag !== 'MittaGO' && tag !== 'Mitta Rent a Car') {
            pills.push(tag);
        }
    }
    // Si quedó vacío, reintentar sin filtros o usar valor genérico
    if (pills.length === 0) {
        const fallbackRegex = /<span class="tag-pill">(.*?)<\/span>/gi;
        let fm;
        while ((fm = fallbackRegex.exec(htmlContent)) !== null) {
            const tag = fm[1].trim();
            if (tag) pills.push(tag);
        }
    }
    return pills;
}

let updatedCount = 0;
let errorsCount = 0;

keys.forEach(id => {
    const art = articles[id];
    const folder = folderMap[art.brand];
    if (!folder) {
        console.warn(`[WARN] Marca no reconocida para artículo ${id}: "${art.brand}"`);
        errorsCount++;
        return;
    }

    const filePath = findHtmlFile(folder, id);
    if (!filePath) {
        console.error(`[ERROR] No se encontró el archivo HTML para el ID "${id}" en la carpeta: ${folder}`);
        errorsCount++;
        return;
    }

    let html = fs.readFileSync(filePath, 'utf8');
    const originalHtml = html; // Para corroborar si hay cambios

    // Extraer slug y keywords del contenido original
    const slug = getSlug(html, id);
    const keywords = getKeywords(html);
    const keywordsStr = keywords.join(', ');

    // --- ACTUALIZAR EL <head> ---

    // 1. Título
    html = html.replace(/<title>.*?<\/title>/, `<title>${art.title}</title>`);

    // 2. Meta descripción
    const newDescTag = `<meta name="description" content="${art.desc}">`;
    html = html.replace(/<meta\s+name="description"\s+content=".*?"\s*\/?>/i, newDescTag);

    // 3. Meta keywords (inyectar o actualizar)
    const newKeywordsTag = `<meta name="keywords" content="${keywordsStr}">`;
    if (html.includes('name="keywords"') || html.includes('name="Keywords"')) {
        html = html.replace(/<meta\s+name="keywords"\s+content=".*?"\s*\/?>/i, newKeywordsTag);
    } else {
        // Insertar justo debajo de la meta descripción
        html = html.replace(/(<meta\s+name="description"\s+content=".*?"\s*\/?>)/i, `$1\n    ${newKeywordsTag}`);
    }

    // --- ACTUALIZAR LA FICHA TÉCNICA (.meta-header) ---
    let startIdx = html.indexOf('<header class="meta-header">');
    let isHeaderTag = true;
    if (startIdx === -1) {
        startIdx = html.indexOf('<div class="meta-header">');
        isHeaderTag = false;
    }
    if (startIdx !== -1) {
        // Encontrar el inicio del artículo para delimitar el bloque de cabecera
        let articleIdx = html.indexOf('<article');
        if (articleIdx === -1) {
            articleIdx = html.indexOf('<div class="article-content">');
        }

        if (articleIdx !== -1) {
            const headerContent = html.substring(startIdx, articleIdx);
            const lastCloseTagIdx = isHeaderTag ? headerContent.lastIndexOf('</header>') : headerContent.lastIndexOf('</div>');
            const closeTagLength = isHeaderTag ? 9 : 6;
            
            if (lastCloseTagIdx !== -1) {
                const headerBlockToReplace = html.substring(startIdx, startIdx + lastCloseTagIdx + closeTagLength);
                
                // Construir la nueva cabecera homogénea y limpia incluyendo "Descripción meta"
                const cleanBrandLabel = art.brand === 'Cyber 2026 (Borradores)' ? 'Cyber 2026' : art.brand;
                const newHeaderBlock = `<header class="meta-header">
        <h3>Ficha Técnica del Artículo</h3>
        <div><strong>Título:</strong> ${art.title}</div>
        <div><strong>Pilar:</strong> ${art.pilar}</div>
        <div><strong>Marca:</strong> ${cleanBrandLabel}</div>
        <div><strong>Ruta/Slug:</strong> <a href="${slug}" target="_blank">${slug}</a></div>
        <div><strong>Descripción meta:</strong> ${art.desc}</div>
        <div class="meta-tags">
            ${keywords.map(k => `<span class="tag-pill">${k}</span>`).join('\n            ')}
        </div>
    </header>`;
                
                html = html.replace(headerBlockToReplace, newHeaderBlock);
            }
        }
    }

    // Guardar si hubo modificaciones
    if (html !== originalHtml) {
        fs.writeFileSync(filePath, html, 'utf8');
        console.log(`[OK] Actualizada cabecera de: ${path.basename(filePath)} (Slug: ${slug})`);
        updatedCount++;
    } else {
        console.log(`[SKIP] Sin cambios en: ${path.basename(filePath)}`);
    }
});

console.log("\n=== RESUMEN DE EJECUCIÓN ===");
console.log(`Artículos procesados con éxito: ${updatedCount}`);
console.log(`Errores/Advertencias: ${errorsCount}`);
console.log("=========================================");
