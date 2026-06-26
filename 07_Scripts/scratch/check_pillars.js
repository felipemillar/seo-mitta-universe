const fs = require('fs');
const path = require('path');

const CONTENIDOS = "/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta/02_Contenidos_Redactados";

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
    ]
};

function extractArticlePilar(htmlPath) {
    const raw = fs.readFileSync(htmlPath, 'utf8');
    const pilarMatch = raw.match(/<strong>(?:Pilar|Categoria|Pilar:):<\/strong>\s*(.*?)<\/div>/i);
    return pilarMatch ? pilarMatch[1].trim() : 'General';
}

function mapPilar(brandKey, originalPilar, articleNum) {
    if (brandKey === 'mittago') {
        const p = originalPilar.toLowerCase();
        if (p.includes('presupuesto')) return "Pilar 1: Presupuestos (Finanzas Inteligentes)";
        if (p.includes('suscripcion')) return "Pilar 2: Suscripciones (Claridad Operativa)";
        if (p.includes('smart') || p.includes('uses')) return "Pilar 3: Smart Uses (Estilos de Vida Modernos)";
        if (p.includes('educacion') || p.includes('educación')) return "Pilar 4: Educación (Cultura de Movilidad)";
        return "Pilar 4: Educación (Cultura de Movilidad)";
    } else if (brandKey === 'rentacar') {
        const num = articleNum;
        if ([16, 17, 18, 19, 20].includes(num)) {
            return "Pilar 4: Notas de Utilidad (Evergreen & Tips)";
        }
        return "Pilar 1: Rent a Car (Foco B2C y Turismo)";
    }
    return originalPilar;
}

const report = {};

// Scan MittaGO
const goFinales = path.join(CONTENIDOS, 'MittaGO/finales');
if (fs.existsSync(goFinales)) {
    report['MittaGO'] = {};
    brandPillars['mittago'].forEach(p => report['MittaGO'][p] = 0);
    fs.readdirSync(goFinales).filter(f => f.endsWith('.html')).forEach(f => {
        const num = parseInt(f.match(/^(\d+)/)[1]);
        const pilar = extractArticlePilar(path.join(goFinales, f));
        const mapped = mapPilar('mittago', pilar, num);
        report['MittaGO'][mapped] = (report['MittaGO'][mapped] || 0) + 1;
    });
}

// Scan Rent a Car
const racFinales = path.join(CONTENIDOS, 'Mitta_Rent_a_Car/finales');
if (fs.existsSync(racFinales)) {
    report['Mitta Rent a Car'] = {};
    brandPillars['rentacar'].forEach(p => report['Mitta Rent a Car'][p] = 0);
    fs.readdirSync(racFinales).filter(f => f.endsWith('.html')).forEach(f => {
        const num = parseInt(f.match(/^(\d+)/)[1]);
        const pilar = extractArticlePilar(path.join(racFinales, f));
        const mapped = mapPilar('rentacar', pilar, num);
        report['Mitta Rent a Car'][mapped] = (report['Mitta Rent a Car'][mapped] || 0) + 1;
    });
}

console.log(JSON.stringify(report, null, 2));
