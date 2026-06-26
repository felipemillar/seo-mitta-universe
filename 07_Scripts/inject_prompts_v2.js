const fs = require('fs');
const path = require('path');

const cyberPrompts = {
    "02_Reserva_Cyber_2026.html": { 
        prompt1: "Point of View (1ra persona): Vista desde el volante. Letrero holográfico cian/naranja brillante en el centro que dice 'RESERVA CONFIRMADA CYBER'. Efecto Bokeh en el fondo.", 
        neuro1: "Saliencia Visual y Reducción Cognitiva: El Bokeh elimina el ruido periférico forzando la atención foveal. El POV involucra la corteza motora.",
        prompt2: "Mockup de Smartphone: Mano sosteniendo teléfono con un código QR dorado de Mitta flotando. Fondo de aeropuerto minimalista.",
        neuro2: "Heurística de Simplicidad: El código QR y el móvil representan acceso sin fricciones, reduciendo la ansiedad anticipatoria del viaje."
    },
    "02_Suscripcion_Pre_Cyber_2026.html": { 
        prompt1: "Split-screen (30/70): Izquierda (30% desaturado): Contrato tradicional y sello rojo 'DEUDA'. Derecha (70% diurno y luminoso): Hombre sonriendo relajado al volante.", 
        neuro1: "Aversión a la Pérdida y Contraste Espacial: Contraste drástico asocia la 'deuda' con castigo, mientras que la suscripción activa heurísticas de escape hacia el alivio.",
        prompt2: "Gráfico Abstracto Isométrico: Bloques apilándose representando ahorro mensual frente a la depreciación de un auto.",
        neuro2: "Metáfora Visual de Ganancia: Tangibiliza un concepto abstracto (depreciación) en bloques físicos, apelando a la validación lógica del Sistema 2."
    },
    "03_Arriendo_vs_Suscripcion_Cyber.html": { 
        prompt1: "Composición Isométrica: Cruce de caminos en 'Y'. Izquierda: calendario semanal. Derecha: infinito. Usuario mirando directo a la cámara señalando ambas rutas.", 
        neuro1: "Gaze Cuing y Metáfora Espacial: El contacto visual atrae la atención humana; las manos dirigiendo a las rutas reduce la parálisis por análisis.",
        prompt2: "Infografía humana: Dos personas; una con mochila ligera de viaje (Arriendo) y otra con maletín y llaves de una oficina moderna (Suscripción).",
        neuro2: "Anclaje de Identidad: El lector se proyecta en el arquetipo visual correspondiente, facilitando el puente hacia la toma de decisión basada en auto-imagen."
    },
    "04_MittaGO_Pymes_Cyber_2026.html": { 
        prompt1: "Fotografía Corporativa: Empresaria sonriendo frente a una caja fuerte iluminada de verde. Fondo: flota impecable de camionetas blancas.", 
        neuro1: "Procesamiento de Recompensa: La luz verde ataca el sistema dopaminérgico, enlazando la flota operativa con la protección del OPEX.",
        prompt2: "Dashboard holográfico: Interfaz de gestión de flota flotando sobre una tablet, mostrando '100% Operativo'.",
        neuro2: "Sesgo de Control: Mostrar herramientas de gestión visualmente avanzadas transmite sensación de control absoluto y certidumbre al tomador de decisiones B2B."
    },
    "04_RentACar_Invierno_Cyber_2026.html": { 
        prompt1: "Acción Cinematográfica: Camioneta 4x4 robusta cruzando carretera nevada. A través de la ventana, familia riendo. Sello 'Cyber Oferta Asegurada'.", 
        neuro1: "Enmarcado de Seguridad (Safe Haven): Mostrar rostros felices mitiga la amenaza en la amígdala y ancla el 4x4 como sinónimo de supervivencia.",
        prompt2: "Detalle (Macro): Neumático con cadenas para nieve con tracción perfecta sobre hielo iluminado con un rayo de sol cálido.",
        neuro2: "Efecto de Garantía Visual: El detalle técnico específico refuerza la sensación de invulnerabilidad y fiabilidad mecánica."
    },
    "05_MittaGO_Stock_SUV_Cyber_2026.html": { 
        prompt1: "Render Publicitario: SUV premium en showroom oscuro con luz cenital. Letrero flotante rojo 'ÚLTIMAS UNIDADES' con reloj digital en cuenta regresiva.", 
        neuro1: "Sesgo de Escasez y FOMO: Activa el Sistema 1 (cerebro límbico). La urgencia temporal puentea la deliberación lógica.",
        prompt2: "Lifestyle premium: Llaves del SUV sobre una mesa de mármol con un café de especialidad y un pasaporte.",
        neuro2: "Efecto Halo de Estatus: Vincula el vehículo con un estilo de vida aspiracional, elevando la percepción de valor de la oferta de última hora."
    },
    "05_RentACar_Errores_Cyber_2026.html": { 
        prompt1: "Resolución Vertical: Arriba (sombra): Usuario frustrado frente a PC. Abajo (luminoso): Mismo usuario feliz, con llaves de auto y ticket de 'Prepago Exitoso'.", 
        neuro1: "Resolución de Conflicto Visual: Escaneo top-down. Mostrar la amenaza y resolverla rápidamente inyecta dopamina.",
        prompt2: "Iconografía tridimensional: Un candado dorado abierto y brillante junto a una tarjeta de crédito iluminada.",
        neuro2: "Fricción Visual Cero: El candado abierto actúa como un estímulo primario de desbloqueo, indicando una ruta de pago libre de problemas."
    },
    "21_Leasing_Operativo_vs_Compra_Flotas.html": {
        prompt1: "Plano medio: Un CFO en una oficina corporativa luminosa mirando un gráfico digital interactivo que muestra una curva ascendente de flujo de caja. De fondo, a través del ventanal, se aprecia una flota de vehículos corporativos.",
        neuro1: "Procesamiento de Recompensa (Dopamina): La curva ascendente de flujo de caja activa el sistema de recompensa del cerebro ejecutivo. El fondo desenfocado sitúa el negocio en primer plano.",
        prompt2: "Mockup 3D: Una balanza equilibrada. En el platillo izquierdo (CAPEX inmovilizado): un bloque de hierro pesado. En el platillo derecho (OPEX flexible): una pluma flotando junto a un icono de escudo protector de Mitta.",
        neuro2: "Heurística de Simplicidad Visual: Traduce un dilema financiero complejo (CAPEX vs OPEX) en una metáfora de peso y ligereza, facilitando la toma de decisiones rápidas por el Sistema 1."
    },
    "22_Continuidad_Operacional_Mineria.html": {
        prompt1: "Plano americano: Camioneta minera 4x4 equipada con pértiga y barra antivuelco, posicionada en una faena cordillera a gran altitud. Iluminación dorada de atardecer, cielo despejado.",
        neuro1: "Saliencia Visual e Inducción de Seguridad: El equipamiento técnico de alta visibilidad (pértiga, barras) actúa como un estímulo primario de seguridad frente al riesgo geográfico en la amígdala.",
        prompt2: "Primer plano (Macro): Un módem de telemetría e interfaz de usuario de GPS vehicular instalados en el tablero de una camioneta comercial, mostrando el estado 'Conexión Segura y GPS Activo'.",
        neuro2: "Sesgo de Control: Mostrar la tecnología de telemetría y diagnóstico activo reduce la ansiedad operacional transmitiendo certidumbre técnica."
    },
    "23_Beneficios_Tributarios_Leasing_Operativo.html": {
        prompt1: "Plano medio: Una tablet sobre un escritorio de madera ejecutiva mostrando un balance contable limpio y un sello digital verde que dice '100% GASTO ACEPTADO'.",
        neuro1: "Refuerzo Positivo Contable: El sello verde y el balance impecable estimulan la certidumbre contable y reducen la carga cognitiva asociada a auditorías.",
        prompt2: "Render conceptual: Un escudo de cristal transparente protegiendo una pila de monedas y billetes chilenos de una tormenta de impuestos representados por nubes de tormenta.",
        neuro2: "Aversión a la Pérdida (Loss Aversion): El escudo de cristal tangibiliza la idea de un 'escudo fiscal', activando el impulso biológico de proteger el capital."
    },
    "24_Flotas_Corporativas_Sustentables.html": {
        prompt1: "Plano general: Furgón de reparto eléctrico comercial cargándose en un Wallbox inteligente en un centro de distribución sustentable. De fondo, paneles solares iluminados por el sol.",
        neuro1: "Efecto Halo Ecológico y Novedad: La luz verde del cargador y los paneles solares asocian subconscientemente la marca con modernidad y responsabilidad ética.",
        prompt2: "Infografía 3D: Un brote verde creciendo del conector de una batería eléctrica con un medidor digital que muestra '-90% Emisiones CO2'.",
        neuro2: "Procesamiento Semántico Rápido: Vincula de manera instantánea el concepto técnico de electromovilidad con el beneficio ecológico medible."
    },
    "25_Gestion_Flotas_Inteligente.html": {
        prompt1: "Vista en perspectiva: Una consola de control logístico o tablet mostrando un mapa de Santiago de Chile con rutas optimizadas en verde y la posición de 10 vehículos comerciales.",
        neuro1: "Heurística de Control y Reducción del Caos: La visualización estructurada de un mapa con rutas limpias y marcadas activa la sensación de orden y dominio espacial.",
        prompt2: "Close-up: Manos de un mecánico oficial realizando el chequeo preventivo del motor de una camioneta en un taller de Mitta limpio e iluminado.",
        neuro2: "Señal de Confianza y Delegación: Mostrar el mantenimiento preventivo profesional delega la carga mental del cuidado técnico, reduciendo el estrés de gestión."
    },
    "26_Renting_Autos_Pymes.html": {
        prompt1: "Plano medio: Dos emprendedores jóvenes sonriendo y chocando las manos frente a un furgón comercial cargado de cajas de entrega listas para despacho. Entorno urbano diurno.",
        neuro1: "Activación de Neuronas Espejo: Las sonrisas y el gesto de triunfo disparan empatía y proyectan el éxito de la Pyme al contratar el renting.",
        prompt2: "Iconografía 3D: Un candado dorado abierto suspendido junto a una tarjeta de crédito, simbolizando el fin del endeudamiento bancario tradicional.",
        neuro2: "Heurística de Liberación: El candado abierto simboliza la liberación de flujo de caja y la ausencia de deudas en Dicom."
    },
    "27_Arriendo_Mensual_Independientes.html": {
        prompt1: "Plano medio: Un profesional independiente (arquitecta o consultor) con café en mano y maletín, subiéndose relajado a un SUV mediano frente a su oficina de cristal.",
        neuro1: "Estatus y Proyección Social: El entorno premium y el comportamiento relajado apelan al deseo de estatus y éxito profesional del independiente.",
        prompt2: "Infografía 3D: Un calendario mensual con el día 30 marcado con un icono de actualización circular verde y el mensaje 'Renovación Flexible sin Multas'.",
        neuro2: "Mitigación del Compromiso (FOMO y Flexibilidad): Visualizar la renovación mensual mitiga el miedo al compromiso financiero de largo plazo."
    },
    "28_Renting_Flexible_vs_Credito_Automotriz.html": {
        prompt1: "Split-screen vertical (50/50): Izquierda (tonos opacos): Hombre estresado firmando un contrato bancario con un sello de 'Deuda a 48 meses'. Derecha (tonos cálidos y luminosos): Misma persona conduciendo feliz con llaves en mano.",
        neuro1: "Contraste Cognitivo Inmediato: El cerebro procesa el contraste espacial de forma subconsciente, asociando la deuda con castigo y el renting con alivio.",
        prompt2: "Render 3D: Un auto Mitta saliendo de una caja de regalo abierta, representando el modelo de movilidad como servicio libre de trámites iniciales.",
        neuro2: "Sesgo de Gratificación Inmediata: La caja de regalo activa estímulos asociados a la recompensa sin el esfuerzo ni la burocracia de la compra."
    },
    "29_Movilidad_Temporal_Proyectos.html": {
        prompt1: "Plano general: Un capataz o ingeniero con casco blanco en una obra de construcción supervisando la llegada de 3 camionetas de trabajo Mitta.",
        neuro1: "Anclaje de Contexto de Utilidad: Sitúa al vehículo en su rol de herramienta de producción, activando la heurística de utilidad laboral B2B.",
        prompt2: "Infografía conceptual: Gráfico de barras que sube y baja coincidiendo con la cantidad de camionetas activas, con la leyenda 'Escalabilidad mes a mes'.",
        neuro2: "Validación Lógica del Sistema 2: Muestra visualmente la correlación directa entre el costo y la duración del proyecto, justificando la eficiencia."
    },
    "30_Renting_Flexible_Camionetas.html": {
        prompt1: "Plano medio: Conductor de microempresa acomodando herramientas y escaleras en el portamaletas de una camioneta cabina doble. Fondo: taller de carpintería o servicios.",
        neuro1: "Heurística de Preparación para la Acción: El dinamismo de cargar herramientas activa la corteza motora del lector y lo prepara para visualizar su propio trabajo.",
        prompt2: "Checklist tridimensional: Un formulario digital flotante con checks verdes en 'Seguro Incluido', 'Mantenimiento Oficial' y 'Patente al Día'.",
        neuro2: "Facilidad Cognitiva: Reducir las inclusiones a un checklist de tres ítems simples elimina la parálisis por análisis y transmite certidumbre total."
    }
};

function getMapping(filename) {
    if (cyberPrompts[filename]) return cyberPrompts[filename];
    
    // Generic logic for MittaGO and Rent a Car based on keywords
    let p1 = "Plano general luminoso: Persona joven sonriendo mientras interactúa con una app móvil junto a un SUV reluciente. Iluminación natural de media mañana.";
    let n1 = "Asociación Positiva Límbica: La sonrisa y la luz cálida disparan neuronas espejo, induciendo un estado de confianza hacia el servicio.";
    let p2 = "Mockup Integrado: Teléfono mostrando el proceso rápido de checkout digital con un checkmark verde brillante.";
    let n2 = "Refuerzo Positivo: El checkmark verde comunica éxito y fluidez, reduciendo el riesgo percibido en el momento de conversión.";

    if (filename.includes("Suscripcion") || filename.includes("Mensual") || filename.includes("Presupuesto") || filename.includes("Costos") || filename.includes("Precios")) {
        p1 = "Split-screen comparativo: Lado izquierdo con papeleo y estrés (tonos fríos); lado derecho con una llave inteligente en mano relajada (tonos cálidos).";
        n1 = "Contraste Cognitivo y Aversión a la Pérdida: Minimiza la carga cognitiva mostrando visualmente la transición del dolor al alivio.";
        p2 = "Infografía Minimalista 3D: Una billetera de cuero de la cual escudos protectores salen hacia un auto.";
        n2 = "Protección Patrimonial: Materializa visualmente el blindaje del presupuesto, apelando al cerebro racional que busca certidumbre financiera.";
    } else if (filename.includes("Aeropuerto") || filename.includes("Viajar") || filename.includes("Extranjeros") || filename.includes("Roadtrips") || filename.includes("Atacama") || filename.includes("Austral")) {
        p1 = "Fotografía de estilo de vida en movimiento: Vista desde el asiento trasero o drone. Un vehículo Mitta recorriendo un paisaje espectacular con alto contraste.";
        n1 = "Procesamiento de Recompensa (Dopaminérgico): El paisaje expansivo evoca libertad y exploración, activando el deseo de viajar.";
        p2 = "Close-up Viajero: Manos guardando un pasaporte y maleta pequeña en el portamaletas amplio de un SUV.";
        n2 = "Anclaje de Continuidad: Visualiza el paso previo inmediato a comenzar la aventura, preparando el cerebro para la acción motora del viaje.";
    } else if (filename.includes("Seguros") || filename.includes("Accidente") || filename.includes("Multas") || filename.includes("Siniestros")) {
        p1 = "Close-up protector: Manos sosteniendo un volante de forma segura, o un ejecutivo entregando llaves con un escudo holográfico azul sutil de fondo.";
        n1 = "Enmarcado de Seguridad (Safe Haven): El color azul y el contacto visual reducen la actividad de la amígdala (ansiedad).";
        p2 = "Escena de Respaldo: Un vehículo de asistencia en ruta amarillo reflectante llegando rápidamente bajo la lluvia.";
        n2 = "Mitigación del Miedo: Validar que existe un 'plan B' tangible (asistencia) desactiva el bloqueo emocional frente a accidentes.";
    } else if (filename.includes("Pymes") || filename.includes("Trabajo") || filename.includes("Camionetas")) {
        p1 = "Composición Corporativa: Flota de camionetas alineadas impecablemente frente a un sitio de obra o edificio moderno. Tonos neutros.";
        n1 = "Heurística de Autoridad y Eficiencia: La simetría transmite orden y control, apelando a la racionalidad del gerente.";
        p2 = "Acción B2B: Dos profesionales estrechando manos frente a una furgoneta de reparto con cajas organizadas.";
        n2 = "Señalización de Confiabilidad: El apretón de manos activa áreas del cerebro social ligadas a la confianza comercial (oxitocina).";
    } else if (filename.includes("SUV") || filename.includes("Hibrido") || filename.includes("Ecologia") || filename.includes("Circular")) {
        p1 = "Render Hi-Tech: Vehículo con detalles verdes luminiscentes o integrado orgánicamente en un entorno urbano sostenible. Aire puro visual.";
        n1 = "Efecto Halo Ecológico: Asocia subconscientemente la modernidad con estatus ético y tecnológico.";
        p2 = "Detalle Textura: Acercamiento al botón de encendido con una hoja verde sutil o medidor de consumo en cero.";
        n2 = "Saliencia de Novedad: El cerebro presta atención extra a pequeños detalles que validan la etiqueta 'eco-friendly'.";
    }

    return { prompt1: p1, neuro1: n1, prompt2: p2, neuro2: n2 };
}

function generateTableHtml(promptData) {
    return `
<!-- INICIO MATRIZ VISUAL NEUROCIENCIA -->
<div class="visual-prompt-matrix" style="margin-top: 50px; border-top: 2px solid #E5E7EB; padding-top: 30px;">
    <h3 style="font-size: 1.2rem; color: #1A1A1A; margin-bottom: 15px;">Matriz de Producción Visual (Digital Predict)</h3>
    <table style="width: 100%; border-collapse: collapse; font-size: 0.95rem; background: #FFFFFF; border: 1px solid #E5E7EB;">
        <thead style="background-color: #F8F9FA;">
            <tr>
                <th style="padding: 15px; border: 1px solid #E5E7EB; text-align: left; width: 20%; color: #374151;">Tipo de Imagen</th>
                <th style="padding: 15px; border: 1px solid #E5E7EB; text-align: left; width: 40%; color: #374151;">Instrucción de Prompt Visual (IA)</th>
                <th style="padding: 15px; border: 1px solid #E5E7EB; text-align: left; width: 40%; color: #374151;">Justificación Algorítmica (Neurociencia)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 15px; border: 1px solid #E5E7EB; color: #1F2937; vertical-align: top;">
                    <strong>1. Principal (Hero)</strong><br><span style="font-size: 0.8rem; color: #6B7280;">Cabecera del artículo</span>
                </td>
                <td style="padding: 15px; border: 1px solid #E5E7EB; color: #1F2937; vertical-align: top;">
                    ${promptData.prompt1}
                </td>
                <td style="padding: 15px; border: 1px solid #E5E7EB; color: #4B5563; vertical-align: top; background: #F9FAFB;">
                    ${promptData.neuro1}
                </td>
            </tr>
            <tr>
                <td style="padding: 15px; border: 1px solid #E5E7EB; color: #1F2937; vertical-align: top;">
                    <strong>2. Secundaria (In-text)</strong><br><span style="font-size: 0.8rem; color: #6B7280;">Apoyo de lectura media</span>
                </td>
                <td style="padding: 15px; border: 1px solid #E5E7EB; color: #1F2937; vertical-align: top;">
                    ${promptData.prompt2}
                </td>
                <td style="padding: 15px; border: 1px solid #E5E7EB; color: #4B5563; vertical-align: top; background: #F9FAFB;">
                    ${promptData.neuro2}
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
                
                const promptData = getMapping(f);
                const tableHtml = generateTableHtml(promptData);

                // Si ya existe la matriz anterior, reemplazarla
                if (content.includes("<!-- INICIO MATRIZ VISUAL NEUROCIENCIA -->")) {
                    const regex = /<!-- INICIO MATRIZ VISUAL NEUROCIENCIA -->[\s\S]*?<!-- FIN MATRIZ VISUAL NEUROCIENCIA -->/g;
                    content = content.replace(regex, tableHtml);
                } else {
                    // Inyectar por primera vez
                    if (content.includes("</article>")) {
                        content = content.replace("</article>", tableHtml + "\n    </article>");
                    } else if (content.includes("<h3>Preguntas Frecuentes")) {
                        content = content.replace("<h3>Preguntas Frecuentes", tableHtml + "\n\n<h3>Preguntas Frecuentes");
                    } else {
                        content = content + "\n" + tableHtml;
                    }
                }

                fs.writeFileSync(htmlPath, content, 'utf8');
                injectedCount++;
            }
        });
    }
});

console.log("Tablas de Producción Visual (2 imágenes) inyectadas en " + injectedCount + " archivos HTML.");
