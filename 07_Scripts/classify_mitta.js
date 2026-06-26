const fs = require('fs');
const path = require('path');

const classifications = {
    "01_Guia_Arriendo_Aeropuertos.html": "Guías Prácticas",
    "02_Requisitos_Extranjeros.html": "Guías Prácticas",
    "03_Arriendo_Primera_Vez.html": "Guías Prácticas",
    "04_Seguros_Coberturas.html": "Coberturas y Condiciones",
    "05_Devolver_Otra_Ciudad.html": "Guías Prácticas",
    "06_Cruzar_Argentina.html": "Destinos y Rutas",
    "07_Carretera_Austral.html": "Destinos y Rutas",
    "08_San_Pedro_Atacama.html": "Destinos y Rutas",
    "09_Top_Roadtrips_Chile.html": "Destinos y Rutas",
    "10_Temporada_Nieve.html": "Destinos y Rutas",
    "11_SUV_vs_Sedan.html": "Flota y Vehículos",
    "12_Camionetas_4x4.html": "Flota y Vehículos",
    "13_Precios_Arriendo_2026.html": "Coberturas y Condiciones",
    "14_Matrimonios_Eventos.html": "Viajes Específicos",
    "15_Fin_Semana_Largo.html": "Viajes Específicos",
    "16_Pana_Accidente.html": "Coberturas y Condiciones",
    "17_Ninos_Sillas_Infantiles.html": "Viajes Específicos",
    "18_Viajar_Mascotas.html": "Viajes Específicos",
    "19_Multas_TAG.html": "Coberturas y Condiciones",
    "20_Checklist_Retiro.html": "Guías Prácticas"
};

const baseDirHtml = '../02_Contenidos_Redactados/Mitta_Rent_a_Car/finales';
const baseDirMd = '../02_Contenidos_Redactados/Mitta_Rent_a_Car/finales';

Object.entries(classifications).forEach(([filename, pilar]) => {
    // HTML File
    const htmlPath = path.join(baseDirHtml, filename);
    if(fs.existsSync(htmlPath)) {
        let content = fs.readFileSync(htmlPath, 'utf8');
        content = content.replace(/<strong>Categoria:<\/strong>\s*Rent a Car/i, `<strong>Pilar:</strong> ${pilar}`);
        fs.writeFileSync(htmlPath, content, 'utf8');
    }
    
    // Markdown file (if we want to replace in markdown too, though not strictly required for the offline portal generation)
    const mdFilename = filename.replace('.html', '.md');
    const mdPath = path.join(baseDirHtml, mdFilename);
    if(fs.existsSync(mdPath)) {
        let mdContent = fs.readFileSync(mdPath, 'utf8');
        mdContent = mdContent.replace(/\*\*Categoria:\*\* Rent a Car/i, `**Pilar:** ${pilar}`);
        mdContent = mdContent.replace(/\*\*Categoría:\*\* Rent a Car/i, `**Pilar:** ${pilar}`);
        fs.writeFileSync(mdPath, mdContent, 'utf8');
    }
});

console.log("Clasificación completada.");
