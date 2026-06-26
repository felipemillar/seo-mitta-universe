const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const CONTENIDOS = path.join(ROOT, '02_Contenidos_Redactados');
const OUTPUT1 = path.join(ROOT, 'Portal_Contenidos_Offline.html');
const OUTPUT2 = path.join(ROOT, 'Portal_Contenidos_Offline_Con_Metadata.html');

// ── Extract article content from HTML files ──────────────────

function extractArticleData(htmlPath) {
    const raw = fs.readFileSync(htmlPath, 'utf8');

    // Extract title
    const titleMatch = raw.match(/<title>(.*?)<\/title>/);
    const title = titleMatch ? titleMatch[1] : path.basename(htmlPath, '.html');

    // Extract meta description
    const descMatch = raw.match(/<meta\s+name="description"\s+content="(.*?)"/);
    const description = descMatch ? descMatch[1] : '';

    // Extract body content (everything between <body> and </body>)
    const bodyMatch = raw.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
    let bodyContent = bodyMatch ? bodyMatch[1].trim() : '';

    // Remove any <script> tags from body (JSON-LD etc.) — we keep them but sanitized
    const scripts = [];
    bodyContent = bodyContent.replace(/<script[\s\S]*?<\/script>/gi, (match) => {
        scripts.push(match);
        return '';
    });

    // Extract Pilar from the tech sheet 
    const pilarMatch = raw.match(/<strong>(?:Pilar|Categoria):<\/strong>\s*(.*?)<\/div>/i);
    const pilar = pilarMatch ? pilarMatch[1].trim() : 'General';

    return { title, description, pilar, body: bodyContent, scripts: scripts.join('\n') };
}

const brandPillars = {
    'mittago': [
        "Pilar 1: Presupuestos (Finanzas Inteligentes)",
        "Pilar 2: Suscripciones (Claridad Operativa)",
        "Pilar 3: Smart Uses (Estilos de Vida Modernos)",
        "Pilar 4: Educación (Cultura de Movilidad)"
    ],
    'rentacar': [
        "Pilar 1: Rent a Car (Foco B2C y Turismo)",
        "Pilar 2: Leasing Operativo (Foco B2B y Flotas)",
        "Pilar 3: Renting Flexible (Puente B2C/Pymes)",
        "Pilar 4: Notas de Utilidad (Evergreen & Tips)"
    ],
    'nuevos2026': [
        "Finanzas y presupuesto",
        "Rent a Car"
    ]
};

const pillarDescriptions = {
    'mittago': {
        "Pilar 1: Presupuestos (Finanzas Inteligentes)": {
            objetivo: "Derribar las barreras de compra demostrando los costos reales de propiedad y la ventaja de la suscripción mensual.",
            temas: [
                "Comparativa de costos de \"Suscripción vs. Crédito Automotriz\".",
                "Costos ocultos del auto propio (mantenciones, seguros, patentes, revisión técnica).",
                "Análisis de la depreciación rápida del vehículo nuevo.",
                "Optimización de flujo de caja libre para independientes y Pymes."
            ]
        },
        "Pilar 2: Suscripciones (Claridad Operativa)": {
            objetivo: "Explicar detalladamente el funcionamiento de la plataforma y el alcance del servicio, reduciendo dudas del embudo de conversión.",
            temas: [
                "Cómo funciona el arriendo mensual en MittaGO (flujo digital de reserva).",
                "El concepto de \"Todo Incluido\" (seguros, mantenciones oficiales, auto de reemplazo).",
                "Diferencias de valor entre Rent a Car por días y Renting mensual.",
                "Prueba y transición hacia la electromovilidad con autos híbridos por meses."
            ]
        },
        "Pilar 3: Smart Uses (Estilos de Vida Modernos)": {
            objetivo: "Inspirar a través de casos prácticos donde la flexibilidad mensual de MittaGO encaja con el estilo de vida actual.",
            temas: [
                "Arriendo estacional (ej: suscribir un auto grande solo para el verano).",
                "Adaptación al teletrabajo y esquemas laborales híbridos.",
                "Facilidad de arriendo para expatriados y extranjeros sin RUT definitivo.",
                "Auto temporal durante esperas prolongadas en talleres mecánicos."
            ]
        },
        "Pilar 4: Educación (Cultura de Movilidad)": {
            objetivo: "Aportar conocimiento técnico y de seguridad sobre tecnología automotriz y el impacto ambiental.",
            temas: [
                "Glosario del mercado de movilidad (Renting vs. Leasing vs. Compra).",
                "Ventajas de la \"mantención delegada\" (cero preocupaciones mecánicas).",
                "Guía de acción simplificada en siniestros y uso de deducibles.",
                "Uso de sistemas avanzados de asistencia a la conducción (ADAS)."
            ]
        }
    },
    'rentacar': {
        "Pilar 1: Rent a Car (Foco B2C y Turismo)": {
            objetivo: "Capturar búsquedas de planificación de viajes y dudas operativas de corto plazo.",
            temas: [
                "Guías definitivas de arriendo en aeropuertos de Chile.",
                "Requisitos legales y financieros para arriendo de extranjeros.",
                "Recomendaciones de categoría de vehículo según el destino (camioneta, SUV, sedán).",
                "Gestiones de pasos fronterizos (ej: viajar a Argentina en auto arrendado)."
            ]
        },
        "Pilar 2: Leasing Operativo (Foco B2B y Flotas)": {
            objetivo: "Convencer a tomadores de decisión (CFOs, Gerentes de Operaciones y RRHH) con argumentos de rentabilidad y continuidad del negocio.",
            temas: [
                "Ventajas tributarias y contables de externalizar flotas (gasto directo).",
                "Análisis comparativo de \"Leasing Operativo vs. Compra de Flotas\".",
                "Gestión de continuidad operacional y auto de reemplazo rápido.",
                "Equipamiento técnico para flotas mineras e industriales.",
                "Electromovilidad corporativa y cumplimiento de metas sustentables (ESG)."
            ]
        },
        "Pilar 3: Renting Flexible (Puente B2C/Pymes)": {
            objetivo: "Educar sobre la flexibilidad del arriendo mensual en comparación con créditos automotrices de largo plazo o compra directa.",
            temas: [
                "Renting de autos para Pymes para preservar liquidez y capital de trabajo.",
                "Renting mensual para profesionales independientes sin comprometer ratios de deuda.",
                "Renting Flexible vs. Crédito Automotriz tradicional.",
                "Movilidad temporal por meses escalable según la demanda de proyectos.",
                "Renting flexible de camionetas y utilitarios para microempresas."
            ]
        },
        "Pilar 4: Notas de Utilidad (Evergreen & Tips)": {
            objetivo: "Capturar tráfico de la parte alta del embudo (Top of Funnel) y generar confianza utilitaria.",
            temas: [
                "Protocolo ante pannes mecánicas o accidentes en ruta.",
                "Normativas de seguridad vial en Chile (ej: sistemas de retención infantil).",
                "Tips prácticos de conducción eficiente y ahorro de combustible.",
                "Políticas y consejos para viajes con mascotas (Pet-Friendly)."
            ]
        }
    },
    'nuevos2026': {
        "Finanzas y presupuesto": {
            objetivo: "Analizar presupuestos, costos y comparativas financieras entre compra de auto y suscripción mensual.",
            temas: []
        },
        "Rent a Car": {
            objetivo: "Guías, recomendaciones y consejos prácticos para arriendo de corto plazo y flotas.",
            temas: []
        }
    }
};

function mapPilar(brandKey, originalPilar, articleNum) {
    if (brandKey === 'nuevos2026') {
        return originalPilar;
    }
    if (brandKey === 'mittago') {
        const p = originalPilar.toLowerCase();
        if (p.includes('presupuesto')) return "Pilar 1: Presupuestos (Finanzas Inteligentes)";
        if (p.includes('suscripcion')) return "Pilar 2: Suscripciones (Claridad Operativa)";
        if (p.includes('smart') || p.includes('uses')) return "Pilar 3: Smart Uses (Estilos de Vida Modernos)";
        if (p.includes('educacion') || p.includes('educación')) return "Pilar 4: Educación (Cultura de Movilidad)";
        return "Pilar 4: Educación (Cultura de Movilidad)";
    } else if (brandKey === 'rentacar') {
        const num = articleNum;
        if ([21, 22, 23, 24, 25].includes(num)) {
            return "Pilar 2: Leasing Operativo (Foco B2B y Flotas)";
        }
        if ([26, 27, 28, 29, 30].includes(num)) {
            return "Pilar 3: Renting Flexible (Puente B2C/Pymes)";
        }
        if ([16, 17, 18, 19, 20].includes(num)) {
            return "Pilar 4: Notas de Utilidad (Evergreen & Tips)";
        }
        return "Pilar 1: Rent a Car (Foco B2C y Turismo)";
    }
    return originalPilar;
}

function scanBrand(folderPath, brandLabel, brandKey) {
    const finalesPath = path.join(folderPath, 'finales');
    if (!fs.existsSync(finalesPath)) return [];

    return fs.readdirSync(finalesPath)
        .filter(f => f.endsWith('.html'))
        .sort()
        .map(f => {
            const data = extractArticleData(path.join(finalesPath, f));
            const numMatch = f.match(/^(\d+)/);
            const num = numMatch ? parseInt(numMatch[1]) : 0;
            const mappedPilar = mapPilar(brandKey, data.pilar, num);
            return {
                id: f.replace('.html', '').replace(/_v2$/, ''),
                fileName: f,
                number: num,
                brand: brandLabel,
                ...data,
                pilar: mappedPilar
            };
        });
}

// ── Scan all brands ──────────────────────────────────────────

const brands = [
    { key: 'mittago', label: 'MittaGO', path: path.join(CONTENIDOS, 'MittaGO') },
    { key: 'rentacar', label: 'Mitta Rent a Car', path: path.join(CONTENIDOS, 'Mitta_Rent_a_Car') },
    { key: 'nuevos2026', label: 'Contenidos Optimizados', path: path.join(CONTENIDOS, 'Nuevos_Contenidos_2026') }
];

const allArticles = [];
const sections = [];

brands.forEach(b => {
    const articles = scanBrand(b.path, b.label, b.key);
    articles.forEach(a => allArticles.push(a));
    sections.push({ ...b, count: articles.length });
    console.log(`  ${b.label}: ${articles.length} articles`);
});

console.log(`Total: ${allArticles.length} articles scanned`);

// ── Escape for embedding in JS ───────────────────────────────

function escapeForJS(str) {
    return str
        .replace(/\\/g, '\\\\')
        .replace(/`/g, '\\`')
        .replace(/\$/g, '\\$')
        .replace(/<\/script>/gi, '<\\/script>');
}

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function truncate(str, max) {
    if (str.length <= max) return str;
    return str.substring(0, max) + '...';
}

// ── Build article data blob ──────────────────────────────────

const articlesJS = allArticles.map(a => {
    return `  "${a.id}": {
    title: \`${escapeForJS(a.title)}\`,
    desc: \`${escapeForJS(a.description)}\`,
    brand: \`${escapeForJS(a.brand)}\`,
    pilar: \`${escapeForJS(a.pilar)}\`,
    num: ${a.number},
    body: \`${escapeForJS(a.body)}\`,
    scripts: \`${escapeForJS(a.scripts)}\`
  }`;
}).join(',\n');

// ── Build index rows ─────────────────────────────────────────

function buildIndexRow(a) {
    const num = String(a.number).padStart(2, '0');
    const desc = truncate(a.description, 160);
    return `
                <a href="#" class="article-row" data-id="${a.id}" data-title="${escapeHtml(a.title)}" data-desc="${escapeHtml(a.description)}" onclick="showArticle('${a.id}');return false;">
                    <span class="article-num">${num}</span>
                    <div class="article-info">
                        <div class="article-title">${escapeHtml(a.title)}</div>
                        <div class="article-desc">${escapeHtml(desc)}</div>
                    </div>
                    <span class="article-arrow">&rarr;</span>
                </a>`;
}

function buildSection(brand) {
    const articles = allArticles.filter(a => a.brand === brand.label);
    
    if (brand.key === 'nuevos2026') {
        const rows = articles.map(buildIndexRow).join('\n');
        return `
            <section class="brand-section" data-brand="${brand.key}">
                <div class="brand-header" onclick="toggleBrand('${brand.key}')" style="cursor: pointer;">
                    <h2>${escapeHtml(brand.label)}</h2>
                    <div class="brand-metrics">
                        <span class="brand-count">${brand.count} articulos</span>
                        <span class="toggle-icon brand-icon">&#9660;</span>
                    </div>
                </div>
                <div class="brand-pillars" id="brand-${brand.key}" style="display: flex; flex-direction: column;">
                    <div class="articles-list" style="display: flex; flex-direction: column; border-top: none;">
                        ${rows}
                    </div>
                </div>
            </section>`;
    }

    const pillars = brandPillars[brand.key] || [];
    
    let html = `
            <section class="brand-section" data-brand="${brand.key}">
                <div class="brand-header" onclick="toggleBrand('${brand.key}')" style="cursor: pointer;">
                    <h2>${escapeHtml(brand.label)}</h2>
                    <div class="brand-metrics">
                        <span class="brand-count">${brand.count} articulos</span>
                        <span class="toggle-icon brand-icon">&#9660;</span>
                    </div>
                </div>
                <div class="brand-pillars" id="brand-${brand.key}">`;
                
    pillars.forEach((pilar, index) => {
        const pilarArticles = articles.filter(a => a.pilar === pilar);
        const pilarId = brand.key + '-p' + index;
        
        // Fetch description
        const descInfo = pillarDescriptions[brand.key] && pillarDescriptions[brand.key][pilar];
        let descHtml = '';
        if (descInfo) {
            descHtml += `<div class="pillar-info">`;
            if (descInfo.objetivo) {
                descHtml += `<p><strong>Objetivo:</strong> ${escapeHtml(descInfo.objetivo)}</p>`;
            }
            if (descInfo.temas && descInfo.temas.length > 0) {
                descHtml += `<p style="margin-top: 8px;"><strong>Temas Principales:</strong></p><ul style="padding-left: 20px; margin-top: 4px; margin-bottom: 0; list-style-type: disc;">`;
                descInfo.temas.forEach(tema => {
                    descHtml += `<li>${escapeHtml(tema)}</li>`;
                });
                descHtml += `</ul>`;
            }
            descHtml += `</div>`;
        }

        html += `
                    <div class="pillar-section" data-pilar="${escapeHtml(pilar)}">
                        <div class="pillar-header" onclick="togglePillar('${pilarId}')" style="cursor: pointer;">
                            <h3>📁 ${escapeHtml(pilar)}</h3>
                            <div class="pillar-metrics">
                                <span class="pillar-count">${pilarArticles.length}</span>
                                <span class="toggle-icon pillar-icon">&#9660;</span>
                            </div>
                        </div>
                        <div class="articles-list" id="${pilarId}" style="display: none; flex-direction: column;">
                            ${descHtml}
${pilarArticles.length > 0 ? pilarArticles.map(a => buildIndexRow(a)).join('\n') : '                    <div style="padding: 14px 20px; color: var(--text-tertiary); font-size: 0.85rem; font-style: italic; background: white;">No hay artículos en este pilar</div>'}
                        </div>
                    </div>`;
    });
    
    html += `
                </div>
            </section>`;
    return html;
}

const now = new Date();
const dateStr = now.toLocaleDateString('es-CL', { year: 'numeric', month: 'long', day: 'numeric' });

// ── Assemble final HTML ──────────────────────────────────────

const finalHTML = `<!DOCTYPE html>
<html lang="es-CL">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal de Contenidos Offline — Mitta</title>
    <meta name="description" content="Portal offline autocontenido con todos los articulos SEO/GEO/AEO de Mitta y MittaGO.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --text-primary: #111827;
            --text-secondary: #6B7280;
            --text-tertiary: #9CA3AF;
            --bg-page: #FFFFFF;
            --bg-hover: #F9FAFB;
            --border: #E5E7EB;
            --border-light: #F3F4F6;
            --font: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        body {
            font-family: var(--font);
            background-color: var(--bg-page);
            color: var(--text-primary);
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }

        /* ── INDEX VIEW ── */
        .page-header {
            border-bottom: 1px solid var(--border);
            padding: 48px 40px 40px;
        }
        .header-inner { max-width: 960px; margin: 0 auto; }
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 32px;
        }
        .header-brand {
            font-size: 0.75rem; font-weight: 500;
            letter-spacing: 0.12em; text-transform: uppercase;
            color: var(--text-tertiary); margin-bottom: 12px;
        }
        .header-title {
            font-size: 1.75rem; font-weight: 600;
            letter-spacing: -0.025em; margin-bottom: 8px;
        }
        .header-subtitle { font-size: 0.95rem; color: var(--text-secondary); }
        .header-date { font-size: 0.8rem; color: var(--text-tertiary); white-space: nowrap; padding-top: 4px; }
        .metrics-bar { display: flex; gap: 48px; }
        .metric { display: flex; flex-direction: column; }
        .metric-value { font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }
        .metric-label { font-size: 0.75rem; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px; }

        .search-container { max-width: 960px; margin: 0 auto; padding: 24px 40px; border-bottom: 1px solid var(--border-light); }
        .search-input {
            width: 100%; padding: 12px 0; border: none; outline: none;
            font-family: var(--font); font-size: 0.95rem; background: transparent;
        }
        .search-input::placeholder { color: var(--text-tertiary); }

        .content { max-width: 960px; margin: 0 auto; padding: 0 40px 80px; }
        .brand-section { padding-top: 24px; }
        .brand-section + .brand-section { border-top: 1px solid var(--border); margin-top: 24px; }
        .brand-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #F9FAFB; border-radius: 8px; margin-bottom: 16px; transition: background 0.2s ease; border: 1px solid var(--border-light); }
        .brand-header:hover { background: #F3F4F6; }
        .brand-header h2 { font-size: 1.15rem; font-weight: 600; letter-spacing: -0.01em; margin: 0; }
        .brand-metrics { display: flex; align-items: center; gap: 12px; }
        .brand-count { font-size: 0.85rem; color: var(--text-secondary); background: white; padding: 4px 10px; border-radius: 20px; border: 1px solid var(--border); }
        .toggle-icon { font-size: 0.75rem; color: var(--text-tertiary); transition: transform 0.2s ease; display: inline-block; }
        
        .brand-pillars { display: flex; flex-direction: column; gap: 12px; padding-left: 24px; margin-bottom: 24px; }
        .pillar-section { border: 1px solid var(--border-light); border-radius: 6px; overflow: hidden; }
        .pillar-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 20px; background: white; transition: background 0.2s ease; }
        .pillar-header:hover { background: #F9FAFB; }
        .pillar-header h3 { font-size: 0.95rem; font-weight: 500; margin: 0; color: var(--text-primary); display: flex; align-items: center; gap: 8px; }
        .pillar-metrics { display: flex; align-items: center; gap: 12px; }
        .pillar-count { font-size: 0.8rem; color: var(--text-secondary); background: #F3F4F6; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; border-radius: 12px; }
        
        .articles-list { display: flex; flex-direction: column; border-top: 1px solid var(--border-light); }
        .pillar-info {
            padding: 16px 20px;
            background-color: var(--bg-hover);
            border-bottom: 1px solid var(--border-light);
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
        .pillar-info p {
            margin-bottom: 8px;
            line-height: 1.4;
        }
        .pillar-info p:last-child {
            margin-bottom: 0;
        }
        .pillar-info li {
            margin-bottom: 4px;
            line-height: 1.4;
        }
        .pillar-info li:last-child {
            margin-bottom: 0;
        }
        .pillar-info strong {
            color: var(--text-primary);
            font-weight: 600;
        }
        .article-row {
            display: flex; align-items: center; gap: 16px;
            padding: 14px 12px; text-decoration: none; color: inherit;
            border-bottom: 1px solid var(--border-light);
            transition: background-color 0.15s ease;
        }
        .article-row:last-child { border-bottom: none; }
        .article-row:hover { background-color: var(--bg-hover); }
        .article-num { font-size: 0.8rem; font-weight: 500; color: var(--text-tertiary); min-width: 28px; font-variant-numeric: tabular-nums; }
        .article-info { flex: 1; min-width: 0; }
        .article-title { font-size: 0.95rem; font-weight: 500; margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .article-desc { font-size: 0.8rem; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .article-arrow { color: var(--text-tertiary); font-size: 0.9rem; opacity: 0; transition: opacity 0.15s ease, transform 0.15s ease; transform: translateX(-4px); }
        .article-row:hover .article-arrow { opacity: 1; transform: translateX(0); }

        .no-results { display: none; padding: 48px 0; text-align: center; color: var(--text-tertiary); font-size: 0.95rem; }
        .page-footer { border-top: 1px solid var(--border); padding: 24px 40px; text-align: center; }
        .footer-text { font-size: 0.75rem; color: var(--text-tertiary); }

        /* ── ARTICLE VIEW ── */
        #articleView { display: none; }

        .article-nav {
            border-bottom: 1px solid var(--border);
            padding: 16px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            background: var(--bg-page);
            z-index: 100;
        }
        .back-link {
            font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);
            text-decoration: none; cursor: pointer;
            transition: color 0.15s ease;
        }
        .back-link:hover { color: var(--text-primary); }
        .article-nav-title {
            font-size: 0.8rem; color: var(--text-tertiary);
            max-width: 500px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            text-align: right;
        }
        .article-nav-brand {
            font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em;
            color: var(--text-tertiary); margin-bottom: 2px;
        }

        .article-viewport {
            max-width: 800px; margin: 0 auto; padding: 40px;
        }

        /* ── Embedded article styles (from article template) ── */
        .article-viewport .meta-header {
            background-color: var(--bg-page); border: 1px solid var(--border-light);
            border-radius: 8px; padding: 20px; margin-bottom: 40px;
            font-size: 0.85rem; color: var(--text-secondary);
        }
        .article-viewport .meta-header h3 {
            margin-top: 0; font-size: 0.75rem; color: var(--text-secondary);
            text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px;
        }
        .article-viewport .meta-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
        .article-viewport .tag-pill {
            background-color: transparent; border: 1px solid var(--border-light);
            color: var(--text-secondary); padding: 4px 12px; border-radius: 4px;
            font-weight: 400; font-size: 0.8rem;
        }
        .article-viewport .article-content, .article-viewport article {
            background-color: var(--bg-page); border: 1px solid var(--border);
            border-radius: 4px; padding: 60px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }
        .article-viewport h1 { font-size: 2.2rem; line-height: 1.2; margin-top: 0; margin-bottom: 24px; letter-spacing: -0.02em; }
        .article-viewport h2 { font-size: 1.6rem; margin-top: 48px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid var(--border-light); }
        .article-viewport h3 { font-size: 1.2rem; margin-top: 32px; margin-bottom: 12px; }
        .article-viewport p { margin-bottom: 20px; font-size: 1.05rem; line-height: 1.7; }
        .article-viewport ul, .article-viewport ol { padding-left: 24px; margin-bottom: 20px; }
        .article-viewport li { margin-bottom: 8px; font-size: 1.05rem; }
        .article-viewport a { color: var(--text-primary); text-decoration: underline; text-underline-offset: 3px; }
        .article-viewport blockquote, .article-viewport .answer-block, .article-viewport .aeo-summary {
            background-color: #F9FAFB; border-left: 2px solid var(--text-primary);
            padding: 24px 32px; margin: 0 0 40px 0; font-size: 1.1rem; line-height: 1.7;
        }
        .article-viewport .aeo-label {
            font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.15em;
            color: var(--text-secondary); margin-bottom: 12px; font-weight: 600;
        }
        .article-viewport .faq-section { border-top: 1px solid var(--border); padding-top: 48px; margin-top: 60px; }
        .article-viewport .faq-section h2 { margin-top: 0; border-bottom: none; padding-bottom: 24px; font-size: 1.5rem; }
        .article-viewport .faq-item { margin-bottom: 24px; }
        .article-viewport .faq-question { font-weight: 600; font-size: 1.1rem; margin-bottom: 8px; }
        .article-viewport .faq-answer { color: var(--text-secondary); }
        .article-viewport .cta-container { margin-top: 60px; padding: 32px 0; border-top: 1px solid var(--border-light); }
        .article-viewport .cta-button {
            display: inline-block; background: transparent; color: var(--text-primary);
            padding: 14px 28px; border: 1px solid var(--text-primary); border-radius: 2px;
            text-decoration: none; font-weight: 500; font-size: 0.95rem;
            transition: all 0.2s ease;
        }
        .article-viewport .cta-button:hover { background: var(--text-primary); color: #fff; }
        .article-viewport .internal-link {
            background: #F9FAFB; padding: 12px 16px; border-radius: 4px;
            border: 1px dashed var(--border); font-size: 0.9rem;
        }
        .article-viewport hr { border: none; border-top: 1px solid var(--border-light); margin: 40px 0; }
        .article-viewport .container { max-width: 100%; padding: 0; }

        /* ── Tables ── */
        .article-viewport table {
            width: 100%;
            border-collapse: collapse;
            margin: 40px 0;
            font-size: 0.95rem;
        }
        .article-viewport th, .article-viewport td {
            padding: 16px 8px;
            text-align: left;
            border-bottom: 1px solid var(--border-light);
        }
        .article-viewport th {
            font-weight: 500;
            color: var(--text-secondary);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }
        .article-viewport td strong { font-weight: 600; }
        .article-viewport tr:last-child td {
            border-bottom: 1px solid var(--border-light);
        }
        .article-viewport td:nth-child(2), .article-viewport td:nth-child(3),
        .article-viewport th:nth-child(2), .article-viewport th:nth-child(3) {
            text-align: center;
        }
        .article-viewport .table-wrapper {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        .article-viewport .toc {
            background: #F9FAFB;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 24px 32px;
            margin: 24px 0 40px;
        }
        .article-viewport .toc h2 {
            font-size: 1rem;
            margin-top: 0;
            margin-bottom: 12px;
            border-bottom: none;
            padding-bottom: 0;
        }
        .article-viewport .toc ul { margin-bottom: 0; }
        .article-viewport .toc li { font-size: 0.95rem; margin-bottom: 6px; }

        /* ── Responsive ── */
        @media (max-width: 640px) {
            .page-header, .article-nav { padding-left: 20px; padding-right: 20px; }
            .search-container, .content { padding-left: 20px; padding-right: 20px; }
            .article-viewport { padding: 20px; }
            .article-viewport .article-content, .article-viewport article { padding: 30px 20px; }
            .header-top { flex-direction: column; gap: 8px; }
            .header-title { font-size: 1.4rem; }
            .metrics-bar { gap: 32px; }
            .article-title, .article-desc { white-space: normal; }
            .article-arrow { display: none; }
            .article-viewport h1 { font-size: 1.8rem; }
        }
    </style>
</head>
<body>

    <!-- ══════ INDEX VIEW ══════ -->
    <div id="indexView">
        <header class="page-header">
            <div class="header-inner">
                <div class="header-top">
                    <div>
                        <div class="header-brand">INMedios / Mitta</div>
                        <h1 class="header-title">Portal de Contenidos</h1>
                        <p class="header-subtitle">Indice editorial de articulos SEO, GEO y AEO — Version offline</p>
                    </div>
                    <div class="header-date">Actualizado: ${dateStr}</div>
                </div>
                <div class="metrics-bar">
                    <div class="metric">
                        <span class="metric-value">${allArticles.length}</span>
                        <span class="metric-label">Total articulos</span>
                    </div>
${sections.map(s => `                    <div class="metric">
                        <span class="metric-value">${s.count}</span>
                        <span class="metric-label">${escapeHtml(s.label)}</span>
                    </div>`).join('\n')}
                </div>
            </div>
        </header>

        <div class="search-container">
            <input type="text" class="search-input" id="searchInput" placeholder="Buscar articulo por titulo o descripcion..." autocomplete="off">
        </div>

        <main class="content" id="mainContent">
${sections.map(buildSection).join('\n')}
            <div class="no-results" id="noResults">No se encontraron articulos con ese criterio.</div>
        </main>

        <footer class="page-footer">
            <p class="footer-text">Agencia IN Medios — Proyecto Mitta SEO/GEO/AEO — Documento offline autocontenido</p>
        </footer>
    </div>

    <!-- ══════ ARTICLE VIEW ══════ -->
    <div id="articleView">
        <nav class="article-nav">
            <a class="back-link" onclick="showIndex()">Volver al indice</a>
            <div>
                <div class="article-nav-brand" id="navBrand"></div>
                <div class="article-nav-title" id="navTitle"></div>
            </div>
        </nav>
        <div class="article-viewport" id="articleContent"></div>
        <footer class="page-footer">
            <p class="footer-text">Agencia IN Medios — Proyecto Mitta SEO/GEO/AEO — Documento offline autocontenido</p>
        </footer>
    </div>

    <!-- ══════ EMBEDDED ARTICLE DATA ══════ -->
    <script>
    const ARTICLES = {
${articlesJS}
    };

    function showArticle(id) {
        const art = ARTICLES[id];
        if (!art) return;

        document.getElementById('indexView').style.display = 'none';
        document.getElementById('articleView').style.display = 'block';
        document.getElementById('articleContent').innerHTML = art.body;
        document.getElementById('navTitle').textContent = art.title;
        document.getElementById('navBrand').textContent = art.brand;
        window.scrollTo(0, 0);
        history.pushState({ article: id }, '', '#' + id);
    }

    function showIndex() {
        document.getElementById('articleView').style.display = 'none';
        document.getElementById('indexView').style.display = 'block';
        window.scrollTo(0, 0);
        history.pushState({}, '', window.location.pathname);
    }

    // Handle browser back button
    window.addEventListener('popstate', function(e) {
        if (e.state && e.state.article) {
            showArticle(e.state.article);
        } else {
            showIndex();
        }
    });

    // Handle direct link with hash
    if (window.location.hash) {
        const id = window.location.hash.substring(1);
        if (ARTICLES[id]) showArticle(id);
    }

    // Accordion toggles
    function toggleBrand(id) {
        const el = document.getElementById('brand-' + id);
        const icon = el.previousElementSibling.querySelector('.brand-icon');
        if (el.style.display === 'none') {
            el.style.display = 'flex';
            icon.style.transform = 'rotate(180deg)';
        } else {
            el.style.display = 'none';
            icon.style.transform = 'rotate(0deg)';
        }
    }
    
    function togglePillar(id) {
        const el = document.getElementById(id);
        const icon = el.previousElementSibling.querySelector('.pillar-icon');
        if (el.style.display === 'none') {
            el.style.display = 'flex';
            icon.style.transform = 'rotate(180deg)';
        } else {
            el.style.display = 'none';
            icon.style.transform = 'rotate(0deg)';
        }
    }

    // Search
    const searchInput = document.getElementById('searchInput');
    const rows = document.querySelectorAll('.article-row');
    const brandSections = document.querySelectorAll('.brand-section');
    const pillarSections = document.querySelectorAll('.pillar-section');
    const noResults = document.getElementById('noResults');

    searchInput.addEventListener('input', function() {
        const q = this.value.toLowerCase().trim();
        let count = 0;
        
        if (q) {
            rows.forEach(row => {
                const match = row.dataset.title.toLowerCase().includes(q) || row.dataset.desc.toLowerCase().includes(q);
                row.style.display = match ? 'flex' : 'none';
                if (match) count++;
            });
            pillarSections.forEach(sec => {
                const list = sec.querySelector('.articles-list');
                const hasMatch = Array.from(list.children).some(r => r.style.display !== 'none');
                sec.style.display = hasMatch ? 'block' : 'none';
                list.style.display = 'flex'; 
                sec.querySelector('.pillar-icon').style.transform = 'rotate(180deg)';
            });
            brandSections.forEach(sec => {
                const hasMatch = Array.from(sec.querySelectorAll('.article-row')).some(r => r.style.display !== 'none');
                sec.style.display = hasMatch ? 'block' : 'none';
                const el = sec.querySelector('.brand-pillars');
                el.style.display = 'flex'; 
                sec.querySelector('.brand-icon').style.transform = 'rotate(180deg)';
            });
        } else {
            rows.forEach(row => row.style.display = 'flex');
            pillarSections.forEach(sec => {
                sec.style.display = 'block';
                sec.querySelector('.articles-list').style.display = 'none';
                sec.querySelector('.pillar-icon').style.transform = 'rotate(0deg)';
            });
            brandSections.forEach(sec => {
                sec.style.display = 'block';
                sec.querySelector('.brand-pillars').style.display = 'flex'; 
                sec.querySelector('.brand-icon').style.transform = 'rotate(180deg)';
            });
            count = rows.length;
        }
        noResults.style.display = count === 0 ? 'block' : 'none';
    });
    
    // Initial setup
    brandSections.forEach(sec => {
        sec.querySelector('.brand-pillars').style.display = 'flex';
        sec.querySelector('.brand-icon').style.transform = 'rotate(180deg)';
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === '/' && document.activeElement !== searchInput) { e.preventDefault(); searchInput.focus(); }
        if (e.key === 'Escape') {
            if (document.getElementById('articleView').style.display === 'block') { showIndex(); }
            else { searchInput.value = ''; searchInput.dispatchEvent(new Event('input')); searchInput.blur(); }
        }
    });
    </script>

</body>
</html>`;

fs.writeFileSync(OUTPUT1, finalHTML);
fs.writeFileSync(OUTPUT2, finalHTML);
const sizeKB = Math.round(fs.statSync(OUTPUT1).size / 1024);
console.log(`\nPortal offline generated: ${OUTPUT1}`);
console.log(`Portal offline con metadata generated: ${OUTPUT2}`);
console.log(`File size: ${sizeKB} KB`);
console.log(`Articles embedded: ${allArticles.length}`);
