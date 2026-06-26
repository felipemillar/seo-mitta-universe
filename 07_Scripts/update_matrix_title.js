const fs = require('fs');
const path = require('path');

const baseDir = '../02_Contenidos_Redactados';
const dirs = fs.readdirSync(baseDir).filter(f => fs.statSync(path.join(baseDir, f)).isDirectory());

let updatedCount = 0;

dirs.forEach(d => {
    const finalesDir = path.join(baseDir, d, 'finales');
    if(fs.existsSync(finalesDir)) {
        fs.readdirSync(finalesDir).forEach(f => {
            if(f.endsWith('.html')) {
                const htmlPath = path.join(finalesDir, f);
                let content = fs.readFileSync(htmlPath, 'utf8');
                
                if (content.includes("Matriz de Producción Visual (Digital Predict)")) {
                    content = content.replace(/Matriz de Producción Visual \(Digital Predict\)/g, "INM Digital Predict");
                    fs.writeFileSync(htmlPath, content, 'utf8');
                    updatedCount++;
                }
            }
        });
    }
});

console.log("Título actualizado a 'INM Digital Predict' en " + updatedCount + " archivos HTML.");
