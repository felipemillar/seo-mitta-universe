/**
 * build_portal_v2.js
 * Construye el Portal de Contenidos v2 basándose exactamente en el HTML original.
 * Conserva la estructura de nodos exacta para no romper el CSS ni el JS original.
 */

const fs = require('fs');
const path = require('path');

const MITTA_DIR = path.join(__dirname, '../02_Contenidos_Redactados/Mitta/finales');
const MITTAGO_DIR = path.join(__dirname, '../02_Contenidos_Redactados/MittaGO/finales');
const TEMPLATE_FILE = path.join(__dirname, '../Portal_Contenidos_Offline_Con_Metadata.html');
const OUTPUT_FILE = path.join(__dirname, '../Portal_Contenidos_Offline_v2.html');

// Read the original template
let template = fs.readFileSync(TEMPLATE_FILE, 'utf-8');

// ─── PILAR MAPPINGS ──────────────────────────────────────────
const MITTA_PILARS = {
  p1: { name: 'Pilar 1: Rent a Car (Foco B2C y Turismo)', desc: 'Capturar búsquedas de planificación de viajes, guías de arriendo en aeropuertos y consejos turísticos.' },
  p2: { name: 'Pilar 2: Leasing Operativo (Foco B2B y Flotas)', desc: 'Optimización de flotas corporativas, ventajas tributarias (OPEX vs CAPEX), TCO y estándares mineros.' },
  p3: { name: 'Pilar 3: Renting Flexible (Puente B2C / Pymes)', desc: 'Soluciones mensuales sin pie ni deuda CMF, flexibilidad operacional y renovación de unidades.' },
  p4: { name: 'Pilar 4: Notas de Utilidad (Evergreen & Tips)', desc: 'Contenido práctico sobre asistencia en ruta, sillas ISOFIX, conducción eficiente y mascotas.' }
};

const MITTAGO_PILARS = {
  p1: { name: 'Pilar 1: Presupuestos (Finanzas Inteligentes)', desc: 'Análisis financiero, comparación vs crédito automotriz, costos ocultos y curva de depreciación.' },
  p2: { name: 'Pilar 2: Suscripciones (Claridad Operativa)', desc: 'Funcionamiento del servicio todo incluido, mantenimiento delegado y transición a híbridos.' },
  p3: { name: 'Pilar 3: Smart Uses (Estilos de Vida Modernos)', desc: 'Soluciones para expatriados, trabajo híbrido, uso estacional y auto de reemplazo.' },
  p4: { name: 'Pilar 4: Educación (Cultura de Movilidad)', desc: 'Diccionario de movilidad, economía circular, seguridad ADAS y protocolos ante siniestros.' }
};

function getMittaPilarKey(fileNum) {
  if (fileNum >= 1 && fileNum <= 5) return 'p1';
  if (fileNum >= 6 && fileNum <= 10) return 'p2';
  if (fileNum >= 11 && fileNum <= 15) return 'p3';
  return 'p4';
}

function getMittaGoPilarKey(fileNum) {
  if ([2, 4, 7, 10, 13].includes(fileNum)) return 'p1';
  if ([1, 3, 5, 9, 15].includes(fileNum)) return 'p2';
  if ([6, 8, 11, 14, 18].includes(fileNum)) return 'p3';
  return 'p4'; // 12, 16, 17, 19, 20
}

function escapeForJsTemplate(str) {
  return str.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\${/g, '\\${').replace(/<\/script>/gi, '<\\/script>');
}

// ─── PARSER ──────────────────────────────────────────────────
function parseArticleFile(filePath, brand, fileNum) {
  const html = fs.readFileSync(filePath, 'utf-8');
  const filename = path.basename(filePath);
  const id = filename.replace(/\.html$/, '');

  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const rawTitle = titleMatch ? titleMatch[1].trim() : id;

  const descMatch = html.match(/<meta\s+name="description"\s+content="([^"]*)"/i);
  const desc = descMatch ? descMatch[1].trim() : '';

  const kwMatch = html.match(/<meta\s+name="keywords"\s+content="([^"]*)"/i);
  const keywordsStr = kwMatch ? kwMatch[1].trim() : '';
  const keywordsList = keywordsStr ? keywordsStr.split(',').map(k => k.trim()).filter(Boolean) : [];

  const schemaMatch = html.match(/<script\s+type="application\/ld\+json">([\s\S]*?)<\/script>/i);
  const schemaJson = schemaMatch ? schemaMatch[1].trim() : '';

  let bodyContent = '';
  const articleMatch = html.match(/<article[\s\S]*?<\/article>/i);
  const mainMatch = html.match(/<main[\s\S]*?<\/main>/i);
  const containerMatch = html.match(/<div\s+class="container">([\s\S]*?)<\/div>\s*<\/body>/i);

  if (articleMatch) {
    bodyContent = articleMatch[0];
  } else if (mainMatch) {
    bodyContent = mainMatch[0];
  } else if (containerMatch) {
    bodyContent = containerMatch[1];
  } else {
    const bMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
    bodyContent = bMatch ? bMatch[1] : html;
  }

  const pilarKey = brand === 'MITTA' ? getMittaPilarKey(fileNum) : getMittaGoPilarKey(fileNum);
  const pilarObj = brand === 'MITTA' ? MITTA_PILARS[pilarKey] : MITTAGO_PILARS[pilarKey];
  const slug = '/' + id.replace(/^\d+_/, '').toLowerCase().replace(/_/g, '-') + '/';

  let formattedSchema = '';
  if (schemaJson) {
    try {
      formattedSchema = JSON.stringify(JSON.parse(schemaJson), null, 2);
    } catch (e) {
      formattedSchema = schemaJson;
    }
  }

  const metaHeaderHtml = `
<header class="meta-header">
    <h3>Ficha Técnica del Artículo</h3>
    <div><strong>Título:</strong> ${rawTitle}</div>
    <div><strong>Pilar:</strong> ${pilarObj.name}</div>
    <div><strong>Marca:</strong> ${brand}</div>
    <div><strong>Ruta/Slug:</strong> <a href="${slug}" target="_blank">${slug}</a></div>
    <div><strong>Descripción meta:</strong> ${desc}</div>
    <div class="meta-tags">
        ${keywordsList.map(k => `<span class="tag-pill">${k}</span>`).join('\n        ')}
    </div>
    ${formattedSchema ? `
    <div style="margin-top: 15px; border-top: 1px solid var(--border-light); padding-top: 15px;">
        <details>
            <summary style="cursor: pointer; font-weight: 500; font-size: 0.8rem; color: var(--text-primary);">
                🔍 Ver Schema.org JSON-LD (${formattedSchema.length} caracteres)
            </summary>
            <pre style="background: #111827; color: #E5E7EB; padding: 15px; border-radius: 4px; font-size: 0.75rem; overflow-x: auto; margin-top: 10px; max-height: 400px; font-family: monospace;"><code>${formattedSchema.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code></pre>
        </details>
    </div>` : ''}
</header>`;

  const fullArticleHtml = `<div class="container">\n${metaHeaderHtml}\n${bodyContent}\n</div>`;

  return {
    id, num: fileNum, title: rawTitle, desc, brand, pilarKey, pilarName: pilarObj.name, keywords: keywordsList, html: fullArticleHtml
  };
}

const mittaFiles = fs.readdirSync(MITTA_DIR).filter(f => f.endsWith('.html')).sort().slice(0, 20);
const mittaArticles = mittaFiles.map((file, idx) => parseArticleFile(path.join(MITTA_DIR, file), 'MITTA', idx + 1));

const mittaGoFiles = fs.readdirSync(MITTAGO_DIR).filter(f => f.endsWith('.html')).sort().slice(0, 20);
const mittaGoArticles = mittaGoFiles.map((file, idx) => parseArticleFile(path.join(MITTAGO_DIR, file), 'MittaGO', idx + 1));

const allArticles = [...mittaArticles, ...mittaGoArticles];

// ─── BUILD INDEX HTML EXACT FORMAT ───────────────────────────
function buildBrandSectionHtml(brandName, brandId, pilarDefs, articles) {
  let pillarsHtml = '';

  Object.keys(pilarDefs).forEach((pKey, pIdx) => {
    const pObj = pilarDefs[pKey];
    const pArticles = articles.filter(a => a.pilarKey === pKey);

    const rowsHtml = pArticles.map(art => `
                <a href="#" class="article-row" data-id="${art.id}" data-title="${art.title.replace(/"/g, '&quot;')}" data-desc="${art.desc.replace(/"/g, '&quot;')}" onclick="showArticle('${art.id}');return false;">
                    <span class="article-num">${String(art.num).padStart(2, '0')}</span>
                    <div class="article-info">
                        <div class="article-title">${art.title}</div>
                        <div class="article-desc">${art.desc}</div>
                    </div>
                    <span class="article-arrow">&rarr;</span>
                </a>`).join('');

    pillarsHtml += `
            <div class="pillar-section" data-pilar="${pObj.name}">
                <div class="pillar-header" onclick="togglePillar('${brandId}-p${pIdx}')" style="cursor: pointer;">
                    <h3>📁 ${pObj.name}</h3>
                    <div class="pillar-metrics">
                        <span class="pillar-count">${pArticles.length}</span>
                        <span class="toggle-icon pillar-icon">&#9660;</span>
                    </div>
                </div>
                <div class="articles-list" id="${brandId}-p${pIdx}" style="display: none; flex-direction: column;">
                    <div class="pillar-info">
                        <p><strong>Descripción del Pilar:</strong> ${pObj.desc}</p>
                    </div>
${rowsHtml}
                </div>
            </div>`;
  });

  return `
        <section class="brand-section" data-brand="${brandId}">
            <div class="brand-header" onclick="toggleBrand('${brandId}')" style="cursor: pointer;">
                <h2>${brandName}</h2>
                <div class="brand-metrics">
                    <span class="brand-count">${articles.length} artículos</span>
                    <span class="toggle-icon brand-icon">&#9660;</span>
                </div>
            </div>
            <div class="brand-pillars" id="brand-${brandId}">
${pillarsHtml}
            </div>
        </section>`;
}

const mittagoSectionHtml = buildBrandSectionHtml('MittaGO (Suscripción Vehicular)', 'mittago', MITTAGO_PILARS, mittaGoArticles);
const mittaSectionHtml = buildBrandSectionHtml('MITTA (Rent a Car & Leasing Operativo)', 'mitta', MITTA_PILARS, mittaArticles);

// ─── BUILD ARTICLES JS OBJECT ────────────────────────────────
let articlesJsDict = 'const ARTICLES = {\n';
allArticles.forEach((art, idx) => {
  articlesJsDict += `  "${art.id}": {\n`;
  articlesJsDict += `    title: \`${escapeForJsTemplate(art.title)}\`,\n`;
  articlesJsDict += `    desc: \`${escapeForJsTemplate(art.desc)}\`,\n`;
  articlesJsDict += `    brand: \`${art.brand}\`,\n`;
  articlesJsDict += `    pilar: \`${art.pilarName}\`,\n`;
  articlesJsDict += `    num: ${art.num},\n`;
  articlesJsDict += `    body: \`${escapeForJsTemplate(art.html)}\`\n`;
  articlesJsDict += `  }${idx < allArticles.length - 1 ? ',' : ''}\n`;
});
articlesJsDict += '};';

// ─── REPLACE IN TEMPLATE ──────────────────────────────────────
// 1. Update Metrics
template = template.replace(/<span class="metric-value">71<\/span>/, '<span class="metric-value">40</span>');
template = template.replace(/<span class="metric-value">50<\/span>\s*<span class="metric-label">MittaGO<\/span>/, '<span class="metric-value">20</span>\n                        <span class="metric-label">MittaGO</span>');
template = template.replace(/<span class="metric-value">30<\/span>\s*<span class="metric-label">Mitta Rent a Car<\/span>/, '<span class="metric-value">20</span>\n                        <span class="metric-label">Mitta Rent a Car</span>');
template = template.replace(/<span class="metric-value">14<\/span>\s*<span class="metric-label">Contenidos Optimizados<\/span>/, '<span class="metric-value">40</span>\n                        <span class="metric-label">Contenidos Optimizados</span>');

// 1.5 Update Date and Subtitle
const today = new Date();
const months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
const dateString = `Actualizado: ${today.getDate()} de ${months[today.getMonth()]} de ${today.getFullYear()}`;
template = template.replace(/<div class="header-date">[^<]*<\/div>/, `<div class="header-date">${dateString}</div>`);
// Remove " — Version offline"
template = template.replace(/<p class="header-subtitle">Indice editorial de articulos SEO, GEO y AEO — Version offline<\/p>/, '<p class="header-subtitle">Índice editorial de artículos SEO, GEO y AEO</p>');


// 2. Hide view-tabs (Gallery tab) without deleting the div completely to avoid structural changes
template = template.replace(/<div class="view-tabs"([^>]*)>[\s\S]*?<\/div>/, '<div class="view-tabs" style="display: none;" $1></div>');

// 3. Inject new articles sections precisely inside <div id="articlesSection">
const articlesSectionStart = template.indexOf('<div id="articlesSection">');
const gallerySectionStart = template.indexOf('<div id="gallerySection"');
if (articlesSectionStart !== -1 && gallerySectionStart !== -1) {
  const originalArticlesSectionContentRegex = /<div id="articlesSection">([\s\S]*?)\s*<div id="gallerySection"/;
  template = template.replace(originalArticlesSectionContentRegex, 
    '<div id="articlesSection">\n' + mittagoSectionHtml + '\n' + mittaSectionHtml + '\n            </div>\n\n            <div id="gallerySection"'
  );
}

// 4. Hide gallerySection without deleting it
template = template.replace(/<div id="gallerySection" style="display: none;">/, '<div id="gallerySection" style="display: none !important;">');

// 5. Replace Javascript
const articlesJsStart = template.indexOf('const ARTICLES = {');
const showArticleStart = template.indexOf('function showArticle(id) {');
if (articlesJsStart !== -1 && showArticleStart !== -1) {
  const headPart = template.substring(0, articlesJsStart);
  const tailPart = template.substring(showArticleStart);
  template = headPart + articlesJsDict + '\n\n    ' + tailPart;
}

fs.writeFileSync(OUTPUT_FILE, template, 'utf-8');
console.log(`\n✅ Portal de Contenidos Offline v2.0 generado con exactitud en:\n${OUTPUT_FILE}`);
