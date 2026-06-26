const fs = require('fs');
const path = require('path');

const cyberPath = path.join(__dirname, '../02_Contenidos_Redactados/Cyber_2026');
const templatePath = path.join(__dirname, '../02_Contenidos_Redactados/MittaGO/03_Que_Incluye_Cuota.html');

// Leer template para extraer <head>, <style> y estructura base
const templateHTML = fs.readFileSync(templatePath, 'utf8');
const headAndStyle = templateHTML.substring(0, templateHTML.indexOf('<div class="container">'));

function parseMarkdown(mdText) {
    // Basic Markdown to HTML
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
                    const val = line.substring(colonIdx + 1).replace(/["']/g, '').trim();
                    if (!frontmatter[key]) {
                        frontmatter[key] = val;
                    }
                }
            });
            html = html.substring(endOfFrontmatter + 3).trim();
        }
    }

    // Extract Script (JSON-LD)
    let scriptTag = '';
    const scriptStart = html.indexOf('<script type="application/ld+json">');
    if (scriptStart !== -1) {
        scriptTag = html.substring(scriptStart);
        html = html.substring(0, scriptStart).trim();
    }

    // Process AEO
    html = html.replace(/<!-- AEO-SUMMARY-START -->/g, '<div class="aeo-summary">\n<div class="aeo-label">AEO SUMMARY (OPTIMIZED FOR LLMs)</div>');
    html = html.replace(/<!-- AEO-SUMMARY-END -->/g, '</div>');

    // Headers
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');

    // Blockquotes
    html = html.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');

    // Lists
    html = html.replace(/^\- (.*$)/gim, '<ul><li>$1</li></ul>');
    html = html.replace(/<\/ul>\n<ul>/gim, '\n');

    // Ordered Lists
    html = html.replace(/^[0-9]\. (.*$)/gim, '<ol><li>$1</li></ol>');
    html = html.replace(/<\/ol>\n<ol>/gim, '\n');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Links
    html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');

    // Paragraphs
    html = html.split('\n\n').map(p => {
        if (!p.trim().startsWith('<') && !p.trim().startsWith('[')) {
            return `<p>${p.trim()}</p>`;
        }
        return p;
    }).join('\n\n');

    // Internal links suggest
    html = html.replace(/\[LINK INTERNO SUGERIDO: "(.*?)" \-> (.*?)\]/g, '<p><strong>Enlace sugerido:</strong> <a href="$2">$1</a></p>');

    return { frontmatter, body: html, script: scriptTag };
}

fs.readdirSync(cyberPath).forEach(file => {
    if (file.endsWith('.md')) {
        const mdPath = path.join(cyberPath, file);
        const mdText = fs.readFileSync(mdPath, 'utf8');
        const parsed = parseMarkdown(mdText);
        
        let finalHTML = `${headAndStyle}
<div class="container">
    <header class="meta-header">
        <h3>Meta Datos del Documento</h3>
        <div><strong>Título:</strong> ${parsed.frontmatter.titulo || ''}</div>
        <div><strong>Pilar:</strong> ${parsed.frontmatter.pilar || ''}</div>
        <div><strong>Marca:</strong> ${parsed.frontmatter.marca || ''}</div>
        <div><strong>Formato:</strong> ${parsed.frontmatter.formato_signature || ''}</div>
        <div><strong>Segmento:</strong> ${parsed.frontmatter.segmento || ''}</div>
        <div><strong>Keywords:</strong> ${parsed.frontmatter.keyword_principal || ''}</div>
    </header>
    
    <div class="article-content">
${parsed.body}
    </div>
</div>
${parsed.script}
</body>
</html>`;

        // Update Title in head
        finalHTML = finalHTML.replace(/<title>.*<\/title>/, `<title>${parsed.frontmatter.meta_title || parsed.frontmatter.titulo || 'Mitta'}</title>`);
        finalHTML = finalHTML.replace(/<meta name="description" content=".*">/, `<meta name="description" content="${parsed.frontmatter.meta_description || ''}">`);

        const htmlFile = file.replace('.md', '.html');
        fs.writeFileSync(path.join(cyberPath, htmlFile), finalHTML);
        console.log(`Generated ${htmlFile}`);
    }
});
