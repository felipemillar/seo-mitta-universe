const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const CONTENIDOS = path.join(ROOT, '02_Contenidos_Redactados');
const OUTPUT = path.join(ROOT, 'Portal_Contenidos_Mitta.html');

// ── Scan articles ──────────────────────────────────────────────

function extractMeta(htmlPath) {
    const html = fs.readFileSync(htmlPath, 'utf8');
    const titleMatch = html.match(/<title>(.*?)<\/title>/);
    const descMatch = html.match(/<meta\s+name="description"\s+content="(.*?)"/);
    return {
        title: titleMatch ? titleMatch[1] : path.basename(htmlPath, '.html'),
        description: descMatch ? descMatch[1] : '',
        file: htmlPath
    };
}

function scanFolder(folderPath, label) {
    const finalesPath = path.join(folderPath, 'finales');
    if (!fs.existsSync(finalesPath)) return [];
    
    return fs.readdirSync(finalesPath)
        .filter(f => f.endsWith('.html'))
        .sort()
        .map(f => {
            const meta = extractMeta(path.join(finalesPath, f));
            const relPath = path.relative(ROOT, path.join(finalesPath, f));
            const numMatch = f.match(/^(\d+)/);
            return {
                ...meta,
                fileName: f,
                relPath,
                number: numMatch ? parseInt(numMatch[1]) : 0,
                brand: label
            };
        });
}

const brands = [
    { key: 'MittaGO', label: 'MittaGO', path: path.join(CONTENIDOS, 'MittaGO'), accent: '#1A1A1A' },
    { key: 'RentACar', label: 'Mitta Rent a Car', path: path.join(CONTENIDOS, 'Mitta_Rent_a_Car'), accent: '#374151' },
    { key: 'NuevosContenidos2026', label: 'Contenidos Optimizados', path: path.join(CONTENIDOS, 'Nuevos_Contenidos_2026'), accent: '#00529B' }
];

const sections = brands.map(b => ({
    ...b,
    articles: scanFolder(b.path, b.label)
}));

const totalArticles = sections.reduce((sum, s) => sum + s.articles.length, 0);

console.log(`Scanned ${totalArticles} articles across ${sections.length} brands`);
sections.forEach(s => console.log(`  ${s.label}: ${s.articles.length} articles`));

// ── Generate HTML ──────────────────────────────────────────────

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function truncate(str, max) {
    if (str.length <= max) return str;
    return str.substring(0, max) + '...';
}

function renderArticleRow(article) {
    const num = String(article.number).padStart(2, '0');
    const desc = truncate(article.description, 160);
    return `
                <a href="${article.relPath}" class="article-row" target="_blank">
                    <span class="article-num">${num}</span>
                    <div class="article-info">
                        <div class="article-title">${escapeHtml(article.title)}</div>
                        <div class="article-desc">${escapeHtml(desc)}</div>
                    </div>
                    <span class="article-arrow">&rarr;</span>
                </a>`;
}

function renderSection(section) {
    if (section.articles.length === 0) return '';
    const rows = section.articles.map(renderArticleRow).join('\n');
    return `
            <section class="brand-section">
                <div class="brand-header">
                    <h2>${escapeHtml(section.label)}</h2>
                    <span class="brand-count">${section.articles.length} articulos</span>
                </div>
                <div class="articles-list">
${rows}
                </div>
            </section>`;
}

const now = new Date();
const dateStr = now.toLocaleDateString('es-CL', { year: 'numeric', month: 'long', day: 'numeric' });

const portalHTML = `<!DOCTYPE html>
<html lang="es-CL">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal de Contenidos — Mitta</title>
    <meta name="description" content="Indice editorial de contenidos SEO/GEO/AEO para Mitta y MittaGO.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

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
            -moz-osx-font-smoothing: grayscale;
        }

        /* ── Header ── */
        .page-header {
            border-bottom: 1px solid var(--border);
            padding: 48px 40px 40px;
        }

        .header-inner {
            max-width: 960px;
            margin: 0 auto;
        }

        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 32px;
        }

        .header-brand {
            font-size: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-tertiary);
            margin-bottom: 12px;
        }

        .header-title {
            font-size: 1.75rem;
            font-weight: 600;
            letter-spacing: -0.025em;
            color: var(--text-primary);
            margin-bottom: 8px;
        }

        .header-subtitle {
            font-size: 0.95rem;
            color: var(--text-secondary);
            font-weight: 400;
        }

        .header-date {
            font-size: 0.8rem;
            color: var(--text-tertiary);
            white-space: nowrap;
            padding-top: 4px;
        }

        /* ── Metrics ── */
        .metrics-bar {
            display: flex;
            gap: 48px;
        }

        .metric {
            display: flex;
            flex-direction: column;
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }

        .metric-label {
            font-size: 0.75rem;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 2px;
        }

        /* ── Search ── */
        .search-container {
            max-width: 960px;
            margin: 0 auto;
            padding: 24px 40px;
            border-bottom: 1px solid var(--border-light);
        }

        .search-input {
            width: 100%;
            padding: 12px 0;
            border: none;
            outline: none;
            font-family: var(--font);
            font-size: 0.95rem;
            color: var(--text-primary);
            background: transparent;
        }

        .search-input::placeholder {
            color: var(--text-tertiary);
        }

        /* ── Content ── */
        .content {
            max-width: 960px;
            margin: 0 auto;
            padding: 0 40px 80px;
        }

        /* ── Brand Sections ── */
        .brand-section {
            padding-top: 40px;
        }

        .brand-section + .brand-section {
            border-top: 1px solid var(--border);
            margin-top: 16px;
        }

        .brand-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 16px;
            padding-bottom: 12px;
        }

        .brand-header h2 {
            font-size: 1.1rem;
            font-weight: 600;
            letter-spacing: -0.01em;
            color: var(--text-primary);
        }

        .brand-count {
            font-size: 0.8rem;
            color: var(--text-tertiary);
            font-weight: 400;
        }

        /* ── Article Rows ── */
        .articles-list {
            display: flex;
            flex-direction: column;
        }

        .article-row {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 14px 12px;
            text-decoration: none;
            color: inherit;
            border-bottom: 1px solid var(--border-light);
            transition: background-color 0.15s ease;
        }

        .article-row:last-child {
            border-bottom: none;
        }

        .article-row:hover {
            background-color: var(--bg-hover);
        }

        .article-num {
            font-size: 0.8rem;
            font-weight: 500;
            color: var(--text-tertiary);
            min-width: 28px;
            font-variant-numeric: tabular-nums;
        }

        .article-info {
            flex: 1;
            min-width: 0;
        }

        .article-title {
            font-size: 0.95rem;
            font-weight: 500;
            color: var(--text-primary);
            margin-bottom: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .article-desc {
            font-size: 0.8rem;
            color: var(--text-secondary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .article-arrow {
            color: var(--text-tertiary);
            font-size: 0.9rem;
            opacity: 0;
            transition: opacity 0.15s ease, transform 0.15s ease;
            transform: translateX(-4px);
        }

        .article-row:hover .article-arrow {
            opacity: 1;
            transform: translateX(0);
        }

        /* ── Footer ── */
        .page-footer {
            border-top: 1px solid var(--border);
            padding: 24px 40px;
            text-align: center;
        }

        .footer-text {
            font-size: 0.75rem;
            color: var(--text-tertiary);
        }

        /* ── No results ── */
        .no-results {
            display: none;
            padding: 48px 0;
            text-align: center;
            color: var(--text-tertiary);
            font-size: 0.95rem;
        }

        /* ── Responsive ── */
        @media (max-width: 640px) {
            .page-header { padding: 32px 20px; }
            .search-container { padding: 16px 20px; }
            .content { padding: 0 20px 60px; }
            .header-top { flex-direction: column; gap: 8px; }
            .header-title { font-size: 1.4rem; }
            .metrics-bar { gap: 32px; }
            .metric-value { font-size: 1.25rem; }
            .article-title { white-space: normal; }
            .article-desc { white-space: normal; }
            .article-arrow { display: none; }
            .page-footer { padding: 24px 20px; }
        }
    </style>
</head>
<body>

    <header class="page-header">
        <div class="header-inner">
            <div class="header-top">
                <div>
                    <div class="header-brand">INMedios / Mitta</div>
                    <h1 class="header-title">Portal de Contenidos</h1>
                    <p class="header-subtitle">Indice editorial de articulos SEO, GEO y AEO</p>
                </div>
                <div class="header-date">Actualizado: ${dateStr}</div>
            </div>
            <div class="metrics-bar">
                <div class="metric">
                    <span class="metric-value">${totalArticles}</span>
                    <span class="metric-label">Total articulos</span>
                </div>
${sections.map(s => `                <div class="metric">
                    <span class="metric-value">${s.articles.length}</span>
                    <span class="metric-label">${escapeHtml(s.label)}</span>
                </div>`).join('\n')}
            </div>
        </div>
    </header>

    <div class="search-container">
        <input type="text" class="search-input" id="searchInput" placeholder="Buscar articulo por titulo o descripcion..." autocomplete="off">
    </div>

    <main class="content" id="mainContent">
${sections.map(renderSection).join('\n')}
        <div class="no-results" id="noResults">No se encontraron articulos con ese criterio.</div>
    </main>

    <footer class="page-footer">
        <p class="footer-text">INMedios Digital — Proyecto Mitta SEO/GEO/AEO — Generado automaticamente</p>
    </footer>

    <script>
        const searchInput = document.getElementById('searchInput');
        const rows = document.querySelectorAll('.article-row');
        const sections = document.querySelectorAll('.brand-section');
        const noResults = document.getElementById('noResults');

        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            let visibleCount = 0;

            rows.forEach(row => {
                const title = row.querySelector('.article-title').textContent.toLowerCase();
                const desc = row.querySelector('.article-desc').textContent.toLowerCase();
                const match = !query || title.includes(query) || desc.includes(query);
                row.style.display = match ? 'flex' : 'none';
                if (match) visibleCount++;
            });

            // Hide sections with no visible articles
            sections.forEach(section => {
                const visibleRows = section.querySelectorAll('.article-row[style="display: flex"], .article-row:not([style])');
                const hasVisible = Array.from(section.querySelectorAll('.article-row')).some(r => r.style.display !== 'none');
                section.style.display = hasVisible ? 'block' : 'none';
            });

            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        });

        // Keyboard shortcut: / to focus search
        document.addEventListener('keydown', function(e) {
            if (e.key === '/' && document.activeElement !== searchInput) {
                e.preventDefault();
                searchInput.focus();
            }
            if (e.key === 'Escape') {
                searchInput.value = '';
                searchInput.dispatchEvent(new Event('input'));
                searchInput.blur();
            }
        });
    </script>

</body>
</html>`;

fs.writeFileSync(OUTPUT, portalHTML);
console.log(`\nPortal generated: ${OUTPUT}`);
console.log(`Total articles indexed: ${totalArticles}`);
