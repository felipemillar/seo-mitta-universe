const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const CONTENIDOS = path.join(ROOT, '02_Contenidos_Redactados');

console.log("=== ACTUALIZANDO LAS 5 KEYWORDS EN CADA ARTÍCULO ===");

// Mapeo detallado de 5 keywords para los 47 artículos (SEO/GEO/AEO homologados)
const keywordsMap = {
  // MittaGO (20 artículos)
  "01_Como_Funciona_MittaGO": [
    "arriendo mensual auto chile", "suscripción auto santiago", "renting autos mittago", "como funciona mittago", "suscripcion mensual vehiculos"
  ],
  "02_Suscripcion_vs_Credito": [
    "credito automotriz vs suscripcion", "conviene comprar auto credito", "arriendo mensual autos chile", "renting personas chile", "suscripcion vehiculos mittago"
  ],
  "03_Que_Incluye_Cuota": [
    "que incluye mittago", "suscripcion auto seguro incluido", "mantencion auto arriendo mensual", "patente auto suscripcion", "renting automotriz chile coberturas"
  ],
  "04_Costos_Ocultos": [
    "costo mantener auto chile", "gastos ocultos patente seguro", "depreciacion autos nuevos chile", "suscripcion vs compra auto", "cuanto cuesta mantener auto"
  ],
  "05_MittaGO_vs_Rent_a_Car": [
    "rent a car vs renting mensual", "arriendo auto por meses chile", "diferencia renting y rent a car", "suscripcion autos mittago", "arrendar auto chile largo plazo"
  ],
  "06_Expatriados_Extranjeros": [
    "arriendo auto extranjeros chile", "suscripcion auto rut extranjero", "renting expatriados santiago", "arriendo auto por meses rut", "requisitos arrendar auto extranjeros"
  ],
  "07_Pymes_Emprendedores": [
    "renting autos pymes chile", "arriendo mensual autos empresas", "beneficio tributario renting pyme", "suscripcion vehiculos comerciales", "leasing vs renting pymes"
  ],
  "08_Suscripcion_Temporada": [
    "arriendo auto temporada verano", "suscripcion auto meses verano", "renting mensual vacaciones chile", "arriendo suv verano santiago", "suscripcion vehiculos flexible"
  ],
  "09_Cambiar_de_Auto": [
    "cambiar de auto sin vender", "suscripcion auto flexible chile", "renting cambiar auto meses", "renovar auto sin credito", "mittago cambiar modelo auto"
  ],
  "10_Costo_Depreciacion": [
    "depreciacion autos nuevos chile", "cuanto valor pierde auto nuevo", "renting depreciacion vehiculos", "perdida valor auto por año", "conviene comprar auto nuevo chile"
  ],
  "11_Trabajo_Hibrido": [
    "auto para trabajo hybrido", "movilidad flexible home office", "arriendo mensual auto oficina", "suscripcion auto dias oficina", "renting flexible santiago"
  ],
  "12_Diccionario_Movilidad": [
    "renting vs leasing chile", "diferencia renting leasing compra", "que es leasing operativo", "arriendo financiero auto chile", "compra inteligente vs renting"
  ],
  "13_Guia_Presupuesto": [
    "presupuesto compra auto chile", "costo total propiedad auto", "gastos mensuales auto santiago", "suscripcion auto presupuesto mensual", "calculadora gastos auto nuevo"
  ],
  "14_Smart_Mobility": [
    "smart mobility santiago chile", "movilidad inteligente pago por uso", "suscripcion auto electromovilidad", "futuro transporte urbano chile", "suscripcion vehiculos compartidos"
  ],
  "15_Autos_Hibridos": [
    "renting autos hibridos chile", "arriendo mensual auto hibrido", "suscripcion auto ecologico", "ventajas auto hibrido chile", "mittago autos hibridos"
  ],
  "16_Mantenimiento_Cero": [
    "mantenimiento preventivo auto incluido", "taller mecanico gratis renting", "mantenciones incluidas mittago", "suscripcion auto sin mecanico", "donde hacer mantencion auto"
  ],
  "17_Siniestros_Sin_Estres": [
    "que hacer caso choque auto", "seguro auto deducible renting", "siniestro auto arriendo mensual", "suscripcion auto choque seguro", "mittago cobertura de siniestros"
  ],
  "18_Auto_Reemplazo": [
    "auto de reemplazo santiago", "vehiculo de reemplazo taller", "suscripcion auto reemplazo gratis", "mittago auto de reemplazo", "arriendo auto taller incluido"
  ],
  "19_Economia_Circular": [
    "economia circular automotriz chile", "renting sustentable vehiculos", "suscripcion auto ecologico", "huella carbono auto arriendo", "movilidad verde santiago"
  ],
  "20_Sistemas_ADAS": [
    "sistemas adas seguridad auto", "asistencia conduccion adas chile", "suscripcion auto familiar seguro", "tecnologia prevencion accidentes auto", "autos con adas mittago"
  ],

  // Mitta Rent a Car (20 artículos)
  "01_Guia_Arriendo_Aeropuertos": [
    "rent a car aeropuerto santiago", "arrendar auto aeropuerto chile", "guia arriendo auto aeropuerto", "rent a car santiago terminal", "mitta rent a car aeropuerto"
  ],
  "02_Requisitos_Extranjeros": [
    "arriendo auto extranjero chile", "requisitos rent a car extranjeros", "licencia conducir extranjero chile", "arrendar auto pasaporte chile", "mitta requisitos extranjeros"
  ],
  "03_Arriendo_Primera_Vez": [
    "arrendar auto primera vez chile", "guia paso a paso rent a car", "garantia arriendo auto tarjeta", "requisitos arrendar auto chile", "consejos primer arriendo auto"
  ],
  "04_Seguros_Coberturas": [
    "seguros rent a car chile", "cobertura cdw arriendo auto", "seguro pai rent a car", "deducible arriendo auto chile", "mitta seguros cobertura"
  ],
  "05_Devolver_Otra_Ciudad": [
    "arrendar auto devolver otra ciudad", "servicio drop off rent a car", "arriendo auto santiago a regiones", "devolver auto otra sucursal", "mitta drop off chile"
  ],
  "06_Cruzar_Argentina": [
    "cruzar a argentina auto arrendado", "permiso internacional argentina auto", "seguro obligatorio argentina arriendo", "viajar a argentina auto chile", "requisitos aduana argentina mitta"
  ],
  "07_Carretera_Austral": [
    "carretera austral auto arrendado", "que auto arrendar carretera austral", "arriendo camioneta carretera austral", "ruta carretera austral consejos", "mitta rent a car patagonia"
  ],
  "08_San_Pedro_Atacama": [
    "arrendar auto san pedro atacama", "rutas san pedro atacama auto", "arriendo 4x4 san pedro atacama", "bencina san pedro de atacama", "mitta atacama rent a car"
  ],
  "09_Top_Roadtrips_Chile": [
    "mejores roadtrips chile auto", "rutas para viajar auto chile", "arriendo auto vacaciones chile", "roadtrip chile norte a sur", "mitta itinerarios viaje auto"
  ],
  "10_Temporada_Nieve": [
    "arriendo auto nieve chile", "cadenas nieve auto arriendo", "arriendo suv farellones mitta", "viaje centros de ski auto", "consejos conducir en nieve chile"
  ],
  "11_SUV_vs_Sedan": [
    "arriendo suv vs sedan chile", "que auto arrendar para viajar", "camioneta vs suv arriendo", "flota mitta rent a car", "mejor auto para rutas chile"
  ],
  "12_Camionetas_4x4": [
    "arriendo camionetas 4x4 chile", "camioneta minera arriendo mitta", "requisitos arriendo camioneta 4x4", "mejor camioneta para offroad", "rent a car camioneta santiago"
  ],
  "13_Precios_Arriendo_2026": [
    "precio arriendo auto chile 2026", "cuanto cuesta rent a car chile", "tarifas arriendo autos sucursales", "arriendo auto economico santiago", "mitta precios y ofertas"
  ],
  "14_Matrimonios_Eventos": [
    "arriendo auto matrimonio chile", "auto premium para eventos santiago", "arriendo auto de lujo bodas", "vehiculo de lujo chofer mitta", "mitta autos premium eventos"
  ],
  "15_Fin_Semana_Largo": [
    "arrendar auto fin de semana largo", "escapadas fin de semana auto", "arriendo auto santiago feriado", "reservar rent a car anticipado", "mitta ofertas fin de semana"
  ],
  "16_Pana_Accidente": [
    "pana auto arrendado que hacer", "accidente auto rent a car chile", "asistencia en ruta mitta telefono", "choque auto arriendo denuncia", "mitta asistencia de emergencia"
  ],
  "17_Ninos_Sillas_Infantiles": [
    "silla bebe auto arriendo chile", "alzador infantil rent a car", "ley silla de seguridad niños", "arrendar auto con silla bebe", "mitta equipamiento infantil"
  ],
  "18_Viajar_Mascotas": [
    "viajar con mascotas auto arriendo", "normativa mascotas auto chile", "arrendar auto pet friendly", "caja transporte perro auto", "mitta viajar con mascotas"
  ],
  "19_Multas_TAG": [
    "multas auto arrendado chile", "cobro tag rent a car mitta", "quien paga multas transito arriendo", "peajes electronicos auto arrendado", "mitta cobros tag regions"
  ],
  "20_Checklist_Retiro": [
    "checklist arrendar auto chile", "que revisar al retirar rent a car", "contrato arriendo auto inspeccion", "devolucion auto daños mitta", "mitta entrega de vehiculo"
  ],

  // Cyber 2026 (7 artículos)
  "02_Reserva_Cyber_2026": [
    "ofertas cyber arriendo autos", "descuentos cyberday rent a car", "reserva auto cyber monday mitta", "cyberday chile arriendo autos", "mitta ofertas cyber 2026"
  ],
  "02_Suscripcion_Pre_Cyber_2026": [
    "comprar vs suscribir auto cyber", "ofertas cyberday suscripcion auto", "conviene comprar auto cyber", "suscripcion auto pre cyberday", "mittago ofertas cyber 2026"
  ],
  "03_Arriendo_vs_Suscripcion_Cyber": [
    "arriendo vs suscripcion autos cyber", "diferencia rent a car y renting", "suscripcion autos cyber monday", "arrendar auto por meses cyber", "mitta ofertas cyber de movilidad"
  ],
  "04_MittaGO_Pymes_Cyber_2026": [
    "suscripcion autos pymes cyber", "renting mensual empresas cyberday", "descuento renting pyme cyber", "vehiculos comerciales cyberday mittago", "flota pymes cyber monday 2026"
  ],
  "04_RentACar_Invierno_Cyber_2026": [
    "arrendar camioneta 4x4 cyber", "ofertas cyber rent a car nieve", "arrendar suv vacaciones invierno", "descuento arriendo auto julio chile", "mitta cyberday destinos nieve"
  ],
  "05_MittaGO_Stock_SUV_Cyber_2026": [
    "mejores suv suscripcion cyber", "stock suv mittago cyberday", "arriendo mensual suv cyber monday", "suscripcion suv familiar chile", "mittago ofertas cyber stock"
  ],
  "05_RentACar_Errores_Cyber_2026": [
    "errores arrendar auto cyber", "consejos reservar rent a car cyberday", "evitar estafas cyber arriendo auto", "letra chica cyberday mitta", "arriendo auto cyber monday guia"
  ]
};

const folderMap = {
  'MittaGO': path.join(CONTENIDOS, 'MittaGO', 'finales'),
  'Mitta Rent a Car': path.join(CONTENIDOS, 'Mitta_Rent_a_Car', 'finales'),
  'Cyber 2026 (Borradores)': path.join(CONTENIDOS, 'Cyber_2026', 'finales')
};

// Helper para encontrar el archivo HTML
function findHtmlFile(folderPath, id) {
  if (!fs.existsSync(folderPath)) return null;
  const files = fs.readdirSync(folderPath);
  const match = files.find(f => {
    const base = f.replace('.html', '');
    return base === id || base === id + '_v2';
  });
  return match ? path.join(folderPath, match) : null;
}

let updatedCount = 0;

Object.keys(keywordsMap).forEach(id => {
  const keywords = keywordsMap[id];
  const keywordsStr = keywords.join(', ');
  
  // Determinar marca y buscar el archivo
  let brand = 'MittaGO';
  if (id.toLowerCase().includes('cyber')) {
    brand = 'Cyber 2026 (Borradores)';
  } else if (id.startsWith('01_Guia') || id.startsWith('02_Req') || id.startsWith('03_Arr') || id.startsWith('04_Seg') || id.startsWith('05_Dev') || id.startsWith('06_Cru') || id.startsWith('07_Car') || id.startsWith('08_San') || id.startsWith('09_Top') || id.startsWith('10_Tem') || id.startsWith('11_SUV') || id.startsWith('12_Cam') || id.startsWith('13_Pre') || id.startsWith('14_Mat') || id.startsWith('15_Fin') || id.startsWith('16_Pan') || id.startsWith('17_Nin') || id.startsWith('18_Via') || id.startsWith('19_Mul') || id.startsWith('20_Che')) {
    brand = 'Mitta Rent a Car';
  }

  const folder = folderMap[brand];
  const filePath = findHtmlFile(folder, id);
  if (!filePath) {
    console.error(`[ERROR] No se encontró HTML para el ID "${id}"`);
    return;
  }

  let html = fs.readFileSync(filePath, 'utf8');
  const originalHtml = html;

  // 1. Actualizar keywords en el <head>
  const newKeywordsTag = `<meta name="keywords" content="${keywordsStr}">`;
  if (html.includes('name="keywords"') || html.includes('name="Keywords"')) {
    html = html.replace(/<meta\s+name="keywords"\s+content=".*?"\s*\/?>/i, newKeywordsTag);
  } else {
    // Inserción justo abajo de description
    html = html.replace(/(<meta\s+name="description"\s+content=".*?"\s*\/?>)/i, `$1\n    ${newKeywordsTag}`);
  }

  // 2. Actualizar tag-pills en el <header class="meta-header">
  let startIdx = html.indexOf('<header class="meta-header">');
  let isHeaderTag = true;
  if (startIdx === -1) {
    startIdx = html.indexOf('<div class="meta-header">');
    isHeaderTag = false;
  }

  if (startIdx !== -1) {
    let articleIdx = html.indexOf('<article');
    if (articleIdx === -1) {
      articleIdx = html.indexOf('<div class="article-content">');
    }

    if (articleIdx !== -1) {
      const headerContent = html.substring(startIdx, articleIdx);
      const lastCloseTagIdx = isHeaderTag ? headerContent.lastIndexOf('</header>') : headerContent.lastIndexOf('</div>');
      const closeTagLength = isHeaderTag ? 9 : 6;

      if (lastCloseTagIdx !== -1) {
        const headerBlockToReplace = html.substring(startIdx, startIdx + lastCloseTagIdx + closeTagLength);
        
        // Re-extraer título, pilar, marca, slug y descripción desde el bloque existente
        const titleMatch = headerBlockToReplace.match(/<strong>T[íi]tulo:<\/strong>\s*(.*?)(?:<\/div>|$)/i);
        const titleVal = titleMatch ? titleMatch[1].trim() : '';

        const pilarMatch = headerBlockToReplace.match(/<strong>Pilar:<\/strong>\s*(.*?)(?:<\/div>|$)/i);
        const pilarVal = pilarMatch ? pilarMatch[1].trim() : '';

        const marcaMatch = headerBlockToReplace.match(/<strong>Marca:<\/strong>\s*(.*?)(?:<\/div>|$)/i);
        const marcaVal = marcaMatch ? marcaMatch[1].trim() : '';

        const slugMatch = headerBlockToReplace.match(/<strong>Ruta\/Slug:<\/strong>\s*(.*?)(?:<\/div>|$)/i) ||
                          headerBlockToReplace.match(/<strong>Slug:<\/strong>\s*(.*?)(?:<\/div>|$)/i);
        const slugVal = slugMatch ? slugMatch[1].trim() : '';

        const descMatch = headerBlockToReplace.match(/<strong>Descripci[óo]n meta:<\/strong>\s*(.*?)(?:<\/div>|$)/i);
        const descVal = descMatch ? descMatch[1].trim() : '';

        // Construir la nueva Ficha Técnica con las 5 keywords exactas
        const newHeaderBlock = `<header class="meta-header">
        <h3>Ficha Técnica del Artículo</h3>
        <div><strong>Título:</strong> ${titleVal}</div>
        <div><strong>Pilar:</strong> ${pilarVal}</div>
        <div><strong>Marca:</strong> ${marcaVal}</div>
        <div><strong>Ruta/Slug:</strong> ${slugVal}</div>
        <div><strong>Descripción meta:</strong> ${descVal}</div>
        <div class="meta-tags">
            ${keywords.map(k => `<span class="tag-pill">${k}</span>`).join('\n            ')}
        </div>
    </header>`;

        html = html.replace(headerBlockToReplace, newHeaderBlock);
      }
    }
  }

  if (html !== originalHtml) {
    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`[OK] Actualizadas 5 keywords en: ${path.basename(filePath)}`);
    updatedCount++;
  }
});

console.log(`\n=== KEYWORDS ACTUALIZADAS: ${updatedCount} ===`);
