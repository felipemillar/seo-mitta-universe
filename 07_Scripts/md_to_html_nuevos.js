const fs = require('fs');
const path = require('path');

const WORKSPACE = "/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta";
const DEST_ROOT = path.join(WORKSPACE, "InMedios_Mitta/02_Contenidos_Redactados/Nuevos_Contenidos_2026");
const BORRADORES_DIR = path.join(DEST_ROOT, "borradores");
const FINALES_DIR = path.join(DEST_ROOT, "finales");

// Rutas de templates
const templateMittaGOPath = path.join(WORKSPACE, "InMedios_Mitta/02_Contenidos_Redactados/MittaGO/finales/03_Que_Incluye_Cuota.html");

// Asegurar directorios
if (!fs.existsSync(FINALES_DIR)) fs.mkdirSync(FINALES_DIR, { recursive: true });

// Cargar estructura base de MittaGO (head, style, etc.)
let headAndStyleMittaGO = '';
if (fs.existsSync(templateMittaGOPath)) {
    const templateHTML = fs.readFileSync(templateMittaGOPath, 'utf8');
    headAndStyleMittaGO = templateHTML.substring(0, templateHTML.indexOf('<div class="container">'));
} else {
    console.error(`ERROR: No se encontró la plantilla de MittaGO en ${templateMittaGOPath}`);
}

function parseMarkdownTable(block) {
    const lines = block.trim().split('\n').map(l => l.trim());
    if (lines.length < 2) return block;
    
    let html = '<div class="table-wrapper">\n<table>\n';
    
    // Cabecera
    const headerCols = lines[0].split('|').map(c => c.trim()).filter((c, idx, arr) => idx > 0 && idx < arr.length - 1);
    html += '  <thead>\n    <tr>\n';
    headerCols.forEach(col => {
        // Habilitar negritas o cursivas simples si existieran
        const colClean = col.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html += `      <th>${colClean}</th>\n`;
    });
    html += '    </tr>\n  </thead>\n';
    
    // Cuerpo
    html += '  <tbody>\n';
    const rows = lines.slice(2); // Omitir línea de separadores
    rows.forEach(row => {
        if (!row.trim() || !row.includes('|')) return;
        const cols = row.split('|').map(c => c.trim()).filter((c, idx, arr) => idx > 0 && idx < arr.length - 1);
        html += '    <tr>\n';
        cols.forEach(col => {
            const colClean = col.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            html += `      <td>${colClean}</td>\n`;
        });
        html += '    </tr>\n';
    });
    html += '  </tbody>\n';
    html += '</table>\n</div>';
    
    return html;
}

function parseMarkdown(mdText) {
    let html = mdText;
    
    // Extract frontmatter
    let frontmatter = {};
    if (html.startsWith('---')) {
        const endOfFrontmatter = html.indexOf('---', 3);
        if (endOfFrontmatter !== -1) {
            const fmText = html.substring(3, endOfFrontmatter).trim();
            fmText.split('\n').forEach(line => {
                const colonIdx = line.indexOf(':');
                if (colonIdx !== -1) {
                    const key = line.substring(0, colonIdx).trim();
                    let val = line.substring(colonIdx + 1).trim();
                    val = val.replace(/^\[|]$/g, '').replace(/["']/g, '').trim();
                    if (!frontmatter[key]) {
                        frontmatter[key] = val;
                    }
                }
            });
            html = html.substring(endOfFrontmatter + 3).trim();
        }
    }

    // Extract JSON-LD script if it exists
    let scriptTag = '';
    const scriptStart = html.indexOf('<script type="application/ld+json">');
    if (scriptStart !== -1) {
        scriptTag = html.substring(scriptStart);
        html = html.substring(0, scriptStart).trim();
    }

    // Process AEO summaries
    html = html.replace(/<!-- AEO-SUMMARY-START -->/g, '<div class="aeo-summary">\n<div class="aeo-label">AEO SUMMARY (OPTIMIZED FOR LLMs)</div>');
    html = html.replace(/<!-- AEO-SUMMARY-END -->/g, '</div>');

    // Headers (don't wrap existing HTML headings)
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');

    // Blockquotes
    html = html.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');

    // Unordered Lists
    html = html.replace(/^\- (.*$)/gim, '<ul><li>$1</li></ul>');
    html = html.replace(/<\/ul>\n<ul>/gim, '\n');
    html = html.replace(/^\* (.*$)/gim, '<ul><li>$1</li></ul>');
    html = html.replace(/<\/ul>\n<ul>/gim, '\n');

    // Ordered Lists
    html = html.replace(/^[0-9]+\. (.*$)/gim, '<ol><li>$1</li></ol>');
    html = html.replace(/<\/ol>\n<ol>/gim, '\n');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Links
    html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');

    // Paragraphs
    html = html.split('\n\n').map(p => {
        const trimmed = p.trim();
        if (!trimmed) return '';
        if (trimmed.startsWith('|')) {
            return parseMarkdownTable(trimmed);
        }
        if (!trimmed.startsWith('<') && !trimmed.startsWith('[')) {
            return `<p>${trimmed}</p>`;
        }
        return trimmed;
    }).join('\n\n');

    // Internal links suggest
    html = html.replace(/\[LINK INTERNO SUGERIDO: "(.*?)" \-\> (.*?)\]/g, '<p class="internal-link"><strong>Enlace sugerido:</strong> <a href="$2">$1</a></p>');

    // Horizontal rules
    html = html.replace(/^---$/gim, '<hr>');

    return { frontmatter, body: html, script: scriptTag };
}

function generateMittaHTML(parsed, fileBaseName) {
    const title = parsed.frontmatter.meta_title || parsed.frontmatter.titulo || fileBaseName;
    const description = parsed.frontmatter.meta_description || '';
    const keywords = parsed.frontmatter.keywords || '';
    const categoria = parsed.frontmatter.pilar || 'Rent a Car';

    return `<!DOCTYPE html>
<html lang="es-CL">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <meta name="description" content="${description}">
    <style>
        :root {
            --primary-color: #1A1A1A;
            --text-main: #2D2D2D;
            --text-secondary: #6B7280;
            --bg-body: #FAFAFA;
            --bg-card: #FFFFFF;
            --border-color: #F3F4F6;
            --border-dark: #E5E7EB;
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        body {
            font-family: var(--font-family);
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.6;
            margin: 0;
            padding: 40px 20px;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        .meta-header {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 40px;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .meta-header h3 {
            margin-top: 0;
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 16px;
        }

        .meta-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }

        .tag-pill {
            background-color: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: 400;
            font-size: 0.8rem;
            letter-spacing: 0.02em;
        }

        .article-content {
            background-color: var(--bg-card);
            border: 1px solid var(--border-dark);
            border-radius: 4px;
            padding: 60px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }

        h1 {
            font-size: 2.5rem;
            line-height: 1.2;
            margin-top: 0;
            margin-bottom: 24px;
            letter-spacing: -0.02em;
        }

        h2 {
            font-size: 1.75rem;
            margin-top: 48px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-color);
            letter-spacing: -0.01em;
        }

        h3 {
            font-size: 1.25rem;
            margin-top: 32px;
            margin-bottom: 12px;
        }

        p {
            margin-bottom: 20px;
            font-size: 1.05rem;
        }

        .aeo-summary {
            background-color: #FAFAFA;
            border-left: 2px solid var(--text-main);
            padding: 24px 32px;
            margin: 0 0 40px 0;
            font-size: 1.1rem;
            font-weight: 400;
            color: var(--text-main);
            line-height: 1.7;
        }

        .aeo-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: var(--text-secondary);
            margin-bottom: 12px;
            font-weight: 600;
        }

        .answer-block {
            background-color: #FAFAFA;
            border-left: 2px solid var(--text-main);
            padding: 24px 32px;
            margin: 0 0 40px 0;
            font-size: 1.1rem;
            font-weight: 400;
            color: var(--text-main);
            line-height: 1.7;
        }

        .answer-block strong { font-weight: 600; }

        blockquote {
            background-color: #FAFAFA;
            border-left: 2px solid var(--text-main);
            padding: 24px 32px;
            margin: 0 0 40px 0;
            font-size: 1.1rem;
            color: var(--text-main);
            line-height: 1.7;
        }

        ul, ol {
            padding-left: 24px;
            margin-bottom: 20px;
        }

        li {
            margin-bottom: 8px;
            font-size: 1.05rem;
        }

        a {
            color: var(--text-main);
            text-decoration: underline;
            text-underline-offset: 3px;
        }

        .internal-link {
            background: #F9FAFB;
            padding: 12px 16px;
            border-radius: 4px;
            border: 1px dashed var(--border-dark);
            font-size: 0.9rem;
        }

        hr {
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 40px 0;
        }

        .faq-section {
            border-top: 1px solid var(--border-dark);
            padding-top: 48px;
            margin-top: 60px;
        }

        .faq-section h2 {
            margin-top: 0;
            border-bottom: none;
            padding-bottom: 24px;
            font-size: 1.5rem;
        }

        .faq-item { margin-bottom: 24px; }
        .faq-item:last-child { margin-bottom: 0; }

        .faq-question {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 8px;
            color: var(--text-main);
        }

        .faq-answer {
            color: var(--text-secondary);
            margin-bottom: 0;
        }

        .cta-container {
            margin-top: 60px;
            text-align: left;
            padding: 32px 0;
            border-top: 1px solid var(--border-color);
        }
        
        .cta-button {
            display: inline-block;
            background-color: transparent;
            color: var(--text-main);
            padding: 14px 28px;
            border: 1px solid var(--text-main);
            border-radius: 2px;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            letter-spacing: 0.02em;
            transition: all 0.2s ease;
        }
        
        .cta-button:hover {
            background-color: var(--text-main);
            color: #FFFFFF;
        }

        /* Table styles */
        .table-wrapper {
            overflow-x: auto;
            margin: 30px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid var(--border-color);
            text-align: left;
        }
        th {
            background-color: var(--bg-body);
            font-weight: 600;
        }

        @media (max-width: 600px) {
            .article-content { padding: 30px 20px; }
            h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>

<div class="container">
    <header class="meta-header">
        <h3>Ficha Tecnica del Articulo</h3>
        <div><strong>Titulo:</strong> ${title}</div>
        <div><strong>Categoria:</strong> ${categoria}</div>
        <div><strong>Slug:</strong> ${parsed.frontmatter.slug || ''}</div>
        <div class="meta-tags">
            <span class="tag-pill">Mitta Rent a Car</span>
            ${keywords.split(',').map(k => `<span class="tag-pill">${k.trim()}</span>`).join('\n            ')}
        </div>
    </header>
    
    <article class="article-content">
        <h1>${parsed.frontmatter.titulo || title}</h1>
${parsed.body}
    </article>
</div>
${parsed.script}
</body>
</html>`;
}

function generateMittaGOHTML(parsed, fileBaseName) {
    const title = parsed.frontmatter.meta_title || parsed.frontmatter.titulo || fileBaseName;
    const description = parsed.frontmatter.meta_description || '';
    const keywords = parsed.frontmatter.keywords || '';
    const categoria = parsed.frontmatter.pilar || 'Suscripciones';

    // Generar el cuerpo de MittaGO
    const contentHTML = `${headAndStyleMittaGO}
<div class="container">
    <!-- Meta Data Header -->
    <header class="meta-header">
        <h3>Ficha Técnica del Artículo</h3>
        <div><strong>Título:</strong> ${title}</div>
        <div><strong>Pilar:</strong> ${categoria}</div>
        <div><strong>Marca:</strong> MittaGO</div>
        <div><strong>Ruta/Slug:</strong> <a href="${parsed.frontmatter.slug || ''}" target="_blank">${parsed.frontmatter.slug || ''}</a></div>
        <div><strong>Descripción meta:</strong> ${description}</div>
        <div class="meta-tags">
            ${keywords.split(',').map(k => `<span class="tag-pill">${k.trim()}</span>`).join('\n            ')}
        </div>
    </header>

    <!-- Article Content -->
    <article class="article-content">
        <h1>${parsed.frontmatter.titulo || title}</h1>
${parsed.body}
    </article>
</div>
${parsed.script}
</body>
</html>`;

    // Reemplazar title y description en head
    let finalHTML = contentHTML.replace(/<title>.*<\/title>/, `<title>${title}</title>`);
    finalHTML = finalHTML.replace(/<meta name="description" content=".*">/, `<meta name="description" content="${description}">`);
    return finalHTML;
}

// Escanear y procesar borradores
const files = fs.readdirSync(BORRADORES_DIR).filter(f => f.endsWith('.md'));
console.log(`Encontrados ${files.length} borradores Markdown para convertir.`);

files.forEach(file => {
    const mdPath = path.join(BORRADORES_DIR, file);
    const mdText = fs.readFileSync(mdPath, 'utf8');
    const parsed = parseMarkdown(mdText);
    
    const brand = parsed.frontmatter.marca || 'Mitta';
    let finalHTML = '';

    if (brand.toLowerCase() === 'mittago') {
        finalHTML = generateMittaGOHTML(parsed, file);
    } else {
        finalHTML = generateMittaHTML(parsed, file);
    }
    
    const htmlFile = file.replace('.md', '.html');
    const destPath = path.join(FINALES_DIR, htmlFile);
    fs.writeFileSync(destPath, finalHTML, 'utf8');
    console.log(`  [HTML] Generado: ${htmlFile} (Marca: ${brand})`);
});

console.log(`\nConversión finalizada! ${files.length} archivos HTML creados en finales/.`);
