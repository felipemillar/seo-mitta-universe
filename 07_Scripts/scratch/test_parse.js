const fs = require('fs');
const path = require('path');
const vm = require('vm');

const PORTAL_PATH = path.join(__dirname, '../../Portal_Contenidos_Offline.html');
const portalHtml = fs.readFileSync(PORTAL_PATH, 'utf8');

const scriptMatch = portalHtml.match(/const ARTICLES = \{[\s\S]*?\n\s*\};\s*\n\s*function showArticle/);
if (!scriptMatch) {
    console.error("Error: No se encontró con la nueva regex.");
    process.exit(1);
}

let code = scriptMatch[0].replace(/\s*function showArticle\s*$/, '').trim();

// Reemplazar 'const ARTICLES =' con 'globalThis.ARTICLES =' para que se declare en el sandbox global
const codeToRun = code.replace(/^const ARTICLES\s*=/, 'globalThis.ARTICLES =');

const sandbox = {};
vm.createContext(sandbox);
try {
    vm.runInContext(codeToRun, sandbox);
    console.log("ARTICLES in sandbox:", sandbox.ARTICLES ? "Defined" : "Undefined");
    if (sandbox.ARTICLES) {
        console.log("SUCCESS! Keys found:", Object.keys(sandbox.ARTICLES).length);
        console.log("Example article title:", sandbox.ARTICLES["01_Como_Funciona_MittaGO"].title);
    }
} catch (e) {
    console.error("Execution error:", e.message, e.stack);
}
