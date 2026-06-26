const fs = require('fs');
const path = require('path');

const cyberPrompts = {
    "02_Reserva_Cyber_2026.html": { prompt: "Point of View (1ra persona): Vista desde el volante. Letrero holográfico cian/naranja brillante en el centro que dice 'RESERVA CONFIRMADA CYBER'. Efecto Bokeh en el fondo.", neuro: "Saliencia Visual y Reducción Cognitiva: El Bokeh elimina el ruido periférico forzando la atención foveal. El POV involucra la corteza motora." },
    "02_Suscripcion_Pre_Cyber_2026.html": { prompt: "Split-screen (30/70): Izquierda (30% desaturado): Contrato tradicional y sello rojo 'DEUDA'. Derecha (70% diurno y luminoso): Hombre sonriendo relajado al volante.", neuro: "Aversión a la Pérdida y Contraste Espacial: Contraste drástico asocia la 'deuda' con castigo, mientras que la suscripción activa heurísticas de escape hacia el alivio." },
    "03_Arriendo_vs_Suscripcion_Cyber.html": { prompt: "Composición Isométrica: Cruce de caminos en 'Y'. Izquierda: calendario semanal. Derecha: infinito. Usuario mirando directo a la cámara señalando ambas rutas.", neuro: "Gaze Cuing y Metáfora Espacial: El contacto visual atrae la atención humana; las manos dirigiendo a las rutas reduce la parálisis por análisis." },
    "04_MittaGO_Pymes_Cyber_2026.html": { prompt: "Fotografía Corporativa: Empresaria sonriendo frente a una caja fuerte iluminada de verde. Fondo: flota impecable de camionetas blancas.", neuro: "Procesamiento de Recompensa: La luz verde ataca el sistema dopaminérgico, enlazando la flota operativa con la protección del OPEX." },
    "04_RentACar_Invierno_Cyber_2026.html": { prompt: "Acción Cinematográfica: Camioneta 4x4 robusta cruzando carretera nevada. A través de la ventana, familia riendo. Sello 'Cyber Oferta Asegurada'.", neuro: "Enmarcado de Seguridad (Safe Haven): Mostrar rostros felices mitiga la amenaza en la amígdala y ancla el 4x4 como sinónimo de supervivencia." },
    "05_MittaGO_Stock_SUV_Cyber_2026.html": { prompt: "Render Publicitario: SUV premium en showroom oscuro con luz cenital. Letrero flotante rojo 'ÚLTIMAS UNIDADES' con reloj digital en cuenta regresiva.", neuro: "Sesgo de Escasez y FOMO: Activa el Sistema 1 (cerebro límbico). La urgencia temporal puentea la deliberación lógica." },
    "05_RentACar_Errores_Cyber_2026.html": { prompt: "Resolución Vertical: Arriba (sombra): Usuario frustrado frente a PC. Abajo (luminoso): Mismo usuario feliz, con llaves de auto y ticket de 'Prepago Exitoso'.", neuro: "Resolución de Conflicto Visual: Escaneo top-down. Mostrar la amenaza y resolverla rápidamente inyecta dopamina." }
};

function getMapping(filename) {
    if (cyberPrompts[filename]) return cyberPrompts[filename];
    
    // Generic logic for MittaGO and Rent a Car based on keywords
    let p = "Plano general luminoso: Persona joven sonriendo mientras interactúa con una app móvil junto a un SUV reluciente. Iluminación natural de media mañana.";
    let n = "Asociación Positiva Límbica: La sonrisa y la luz cálida disparan neuronas espejo, induciendo un estado de confianza hacia el servicio.";

    if (filename.includes("Suscripcion") || filename.includes("Mensual") || filename.includes("Presupuesto") || filename.includes("Costos") || filename.includes("Precios")) {
        p = "Split-screen comparativo: Un lado muestra papeleo y estrés (tonos fríos); el otro lado muestra una llave inteligente brillando en una mano relajada (tonos cálidos y dorados).";
        n = "Contraste Cognitivo y Aversión a la Pérdida: Minimiza la carga cognitiva al mostrar visualmente la transición del dolor (trámites) al alivio (MittaGO/Arriendo).";
    } else if (filename.includes("Aeropuerto") || filename.includes("Viajar") || filename.includes("Extranjeros") || filename.includes("Roadtrips") || filename.includes("Atacama") || filename.includes("Austral")) {
        p = "Fotografía de estilo de vida en movimiento: Vista desde el asiento trasero o drone. Un vehículo Mitta recorriendo un paisaje espectacular. Alto contraste de colores saturados.";
        n = "Procesamiento de Recompensa (Dopaminérgico): El paisaje expansivo evoca libertad y exploración, activando fuertemente el deseo de viajar y materializar la reserva.";
    } else if (filename.includes("Seguros") || filename.includes("Accidente") || filename.includes("Multas") || filename.includes("Siniestros")) {
        p = "Close-up protector: Manos sosteniendo un volante de forma segura, o un ejecutivo de Mitta entregando llaves con un escudo holográfico azul sutil de fondo.";
        n = "Enmarcado de Seguridad (Safe Haven): El color azul y el contacto visual de asistencia reducen la actividad de la amígdala (ansiedad) generando sensación de resguardo.";
    } else if (filename.includes("Pymes") || filename.includes("Trabajo") || filename.includes("Camionetas")) {
        p = "Composición Corporativa: Flota de camionetas alineadas impecablemente frente a un sitio de obra o edificio moderno. Tonos neutros con acentos corporativos.";
        n = "Heurística de Autoridad y Eficiencia: La simetría transmite orden y control (Sistema 2), apelando a la racionalidad del gerente en la optimización de sus recursos.";
    } else if (filename.includes("SUV") || filename.includes("Hibrido") || filename.includes("Ecologia") || filename.includes("Circular")) {
        p = "Render Hi-Tech: Vehículo con detalles verdes luminiscentes o integrado orgánicamente en un entorno urbano sostenible. Texturas limpias y aire puro visual.";
        n = "Efecto Halo Ecológico: Asocia subconscientemente la modernidad del vehículo con el estatus ético y tecnológico, elevando la percepción de valor de la marca.";
    }

    return { prompt: p, neuro: n };
}

function generateTableHtml(promptData) {
    return `
<!-- INICIO MATRIZ VISUAL NEUROCIENCIA -->
<div class="visual-prompt-matrix" style="margin-top: 50px; border-top: 2px solid #E5E7EB; padding-top: 30px;">
    <h3 style="font-size: 1.2rem; color: #1A1A1A; margin-bottom: 15px;">Matriz de Producción Visual (Digital Predict)</h3>
    <table style="width: 100%; border-collapse: collapse; font-size: 0.95rem; background: #FFFFFF; border: 1px solid #E5E7EB;">
        <thead style="background-color: #F8F9FA;">
            <tr>
                <th style="padding: 15px; border: 1px solid #E5E7EB; text-align: left; width: 50%; color: #374151;">Instrucción de Prompt Visual (IA)</th>
                <th style="padding: 15px; border: 1px solid #E5E7EB; text-align: left; width: 50%; color: #374151;">Justificación Algorítmica (Neurociencia)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 15px; border: 1px solid #E5E7EB; color: #1F2937; vertical-align: top;">
                    <strong>Imagen Principal (Hero):</strong><br><br>
                    ${promptData.prompt}
                </td>
                <td style="padding: 15px; border: 1px solid #E5E7EB; color: #4B5563; vertical-align: top; background: #F9FAFB;">
                    <strong>Predict Trigger:</strong><br><br>
                    ${promptData.neuro}
                </td>
            </tr>
        </tbody>
    </table>
</div>
<!-- FIN MATRIZ VISUAL NEUROCIENCIA -->
`;
}

const baseDir = '../02_Contenidos_Redactados';
const dirs = fs.readdirSync(baseDir).filter(f => fs.statSync(path.join(baseDir, f)).isDirectory());

let injectedCount = 0;

dirs.forEach(d => {
    const finalesDir = path.join(baseDir, d, 'finales');
    if(fs.existsSync(finalesDir)) {
        fs.readdirSync(finalesDir).forEach(f => {
            if(f.endsWith('.html')) {
                const htmlPath = path.join(finalesDir, f);
                let content = fs.readFileSync(htmlPath, 'utf8');
                
                // Si ya tiene la matriz, la evitamos para no duplicar
                if (content.includes("visual-prompt-matrix")) return;

                const promptData = getMapping(f);
                const tableHtml = generateTableHtml(promptData);

                // Inyectar justo antes de cerrar el article o antes de las FAQ
                if (content.includes("</article>")) {
                    content = content.replace("</article>", tableHtml + "\n    </article>");
                } else if (content.includes("<h3>Preguntas Frecuentes")) {
                    content = content.replace("<h3>Preguntas Frecuentes", tableHtml + "\n\n<h3>Preguntas Frecuentes");
                } else {
                    content = content + "\n" + tableHtml;
                }

                fs.writeFileSync(htmlPath, content, 'utf8');
                injectedCount++;
            }
        });
    }
});

console.log("Tablas de Producción Visual inyectadas en " + injectedCount + " archivos HTML.");
