#!/usr/bin/env python3
"""
=================================================================
 MITTA CONTENT IMPROVEMENT ENGINE v1.0
 Fase 1: Tablas · Fase 2: FAQ · Fase 3: Q-Headings
=================================================================
"""

import os
import re
import json
import html as html_mod
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path("/Users/fmillar/Proyectos_Desarrollo/INMedios_Mitta/InMedios_Mitta/02_Contenidos_Redactados")

ALL_DIRS = {
    "MittaGO": BASE_DIR / "MittaGO" / "finales",
    "Mitta_Rent_a_Car": BASE_DIR / "Mitta_Rent_a_Car" / "finales",
    "Nuevos_Contenidos_2026": BASE_DIR / "Nuevos_Contenidos_2026" / "finales",
    "Cyber_2026": BASE_DIR / "Cyber_2026" / "finales",
}

stats = {"tables": 0, "faqs": 0, "q_headings": 0, "errors": []}


def strip_tags(s):
    s = re.sub(r'<[^>]+>', '', s)
    return html_mod.unescape(s).strip()


def get_h1(content):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    return strip_tags(m.group(1)) if m else ""


def get_h2s(content):
    return [(m.group(1), strip_tags(m.group(2))) 
            for m in re.finditer(r'<h2[^>]*(?:id=["\']([^"\']*)["\'])?[^>]*>(.*?)</h2>', content, re.IGNORECASE | re.DOTALL)]


def has_content_table(content):
    tables = len(re.findall(r'<table', content, re.IGNORECASE))
    matrix = len(re.findall(r'visual-prompt-matrix', content))
    return (tables - matrix) > 0


def has_faq_section(content):
    return bool(re.findall(r'faq-question', content, re.IGNORECASE))


# ═══════════════════════════════════════════════════════════════
# TABLE TEMPLATES by theme detection
# ═══════════════════════════════════════════════════════════════

def detect_theme(filename, h1, h2_texts, category):
    """Detect the article theme to select the right table template."""
    text = f"{h1} {' '.join(h2_texts)} {filename}".lower()
    
    if category == "Cyber_2026":
        return "cyber_ofertas"
    
    # MittaGO themes
    if any(w in text for w in ["suscripci", "mittago", "cuota", "mensual"]) and "vs" in text:
        return "suscripcion_vs"
    if any(w in text for w in ["costo", "presupuesto", "gasto", "precio", "depreciaci"]):
        return "costos_auto"
    if any(w in text for w in ["híbrido", "hibrido", "eléctric", "electr", "sustentab"]):
        return "vehiculos_eco"
    if any(w in text for w in ["adas", "seguridad", "tecnolog"]):
        return "tecnologia"
    if any(w in text for w in ["manteni", "siniestro", "reemplazo", "cobertura"]):
        return "servicios_incluidos"
    if any(w in text for w in ["pyme", "emprendedor", "empresa"]):
        return "planes_empresa"
    if any(w in text for w in ["expatriado", "extranjero"]):
        return "requisitos_extranjero"
    if "diccionario" in text or "glosario" in text:
        return "glosario"
    if any(w in text for w in ["economía circular", "economia circular", "smart mobility"]):
        return "tendencias"
    
    # RAC themes
    if any(w in text for w in ["aeropuerto", "airport"]):
        return "aeropuerto"
    if any(w in text for w in ["ruta", "roadtrip", "carretera", "atacama", "austral", "nieve"]):
        return "rutas_viaje"
    if any(w in text for w in ["seguro", "cdw", "pai", "cobertura"]):
        return "seguros"
    if any(w in text for w in ["requisito", "primera vez", "checklist", "documentos"]):
        return "requisitos"
    if any(w in text for w in ["suv", "sedan", "camioneta", "4x4", "vehículo"]):
        return "comparativa_vehiculos"
    if any(w in text for w in ["multa", "tag", "pana", "accidente"]):
        return "incidentes"
    if any(w in text for w in ["mascota", "niño", "silla", "matrimonio", "evento", "fin de semana"]):
        return "ocasiones_especiales"
    if any(w in text for w in ["leasing", "flota", "corporativ", "minería", "mineria"]):
        return "flotas_lop"
    if any(w in text for w in ["renting", "flexible", "mensual", "independiente"]):
        return "renting_flexible"
    if any(w in text for w in ["precio", "tarifa", "costo"]):
        return "precios"
    
    # NC2026 fallback
    if any(w in text for w in ["rent a car", "arriendo", "arrendar"]):
        return "guia_rac"
    
    return "comparativa_general"


TABLE_TEMPLATES = {
    "suscripcion_vs": """
        <table>
            <thead>
                <tr>
                    <th>Criterio</th>
                    <th>Suscripción MittaGO</th>
                    <th>Crédito Automotriz</th>
                    <th>Compra al Contado</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Inversión inicial</td><td>$0 (solo cuota mensual)</td><td>Pie 10-20%</td><td>100% del valor</td></tr>
                <tr><td>Mantenciones</td><td>✅ Incluidas</td><td>❌ Por tu cuenta</td><td>❌ Por tu cuenta</td></tr>
                <tr><td>Seguro</td><td>✅ Incluido</td><td>Obligatorio aparte</td><td>Obligatorio aparte</td></tr>
                <tr><td>Patente / Permiso</td><td>✅ Incluida</td><td>❌ Pago anual</td><td>❌ Pago anual</td></tr>
                <tr><td>Depreciación</td><td>No te afecta</td><td>-30% en 3 años</td><td>-30% en 3 años</td></tr>
                <tr><td>Flexibilidad</td><td>Cambias de auto</td><td>Atado al crédito</td><td>Vendes con pérdida</td></tr>
            </tbody>
        </table>""",
    
    "costos_auto": """
        <table>
            <thead>
                <tr>
                    <th>Gasto Anual</th>
                    <th>Auto Propio (estimado)</th>
                    <th>Suscripción MittaGO</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Seguro automotriz</td><td>$400.000 – $800.000</td><td>✅ Incluido en cuota</td></tr>
                <tr><td>Permiso de circulación</td><td>$150.000 – $350.000</td><td>✅ Incluido en cuota</td></tr>
                <tr><td>Mantenciones programadas</td><td>$200.000 – $500.000</td><td>✅ Incluido en cuota</td></tr>
                <tr><td>Depreciación</td><td>$1.500.000 – $3.000.000</td><td>$0 (no eres dueño)</td></tr>
                <tr><td>Revisión técnica</td><td>$30.000 – $50.000</td><td>✅ Incluido en cuota</td></tr>
                <tr><td><strong>Total estimado</strong></td><td><strong>$2.280.000 – $4.700.000</strong></td><td><strong>Cuota fija mensual</strong></td></tr>
            </tbody>
        </table>""",
    
    "vehiculos_eco": """
        <table>
            <thead>
                <tr>
                    <th>Característica</th>
                    <th>Auto Convencional</th>
                    <th>Híbrido</th>
                    <th>Eléctrico</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Costo combustible/100 km</td><td>$8.000 – $12.000</td><td>$4.000 – $7.000</td><td>$1.500 – $3.000</td></tr>
                <tr><td>Emisiones CO₂</td><td>150-200 g/km</td><td>70-110 g/km</td><td>0 g/km directo</td></tr>
                <tr><td>Mantención anual</td><td>$300.000+</td><td>$250.000+</td><td>$150.000+</td></tr>
                <tr><td>Autonomía urbana</td><td>500-700 km</td><td>800-1.000 km</td><td>300-500 km</td></tr>
                <tr><td>Disponible en MittaGO</td><td>✅ Sí</td><td>✅ Sí</td><td>Próximamente</td></tr>
            </tbody>
        </table>""",
    
    "aeropuerto": """
        <table>
            <thead>
                <tr>
                    <th>Aeropuerto</th>
                    <th>Ciudad</th>
                    <th>Horario Mitta</th>
                    <th>Categorías Disponibles</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>SCL – Arturo Merino Benítez</td><td>Santiago</td><td>24/7</td><td>Todas</td></tr>
                <tr><td>CJC – El Loa</td><td>Calama</td><td>Lunes a Domingo</td><td>SUV, Camioneta</td></tr>
                <tr><td>ANF – Andrés Sabella</td><td>Antofagasta</td><td>Lunes a Domingo</td><td>Todas</td></tr>
                <tr><td>CCP – Carriel Sur</td><td>Concepción</td><td>Lunes a Domingo</td><td>Todas</td></tr>
                <tr><td>PMC – El Tepual</td><td>Puerto Montt</td><td>Lunes a Domingo</td><td>SUV, 4x4, Sedán</td></tr>
                <tr><td>PUQ – C. Ibáñez del Campo</td><td>Punta Arenas</td><td>Lunes a Sábado</td><td>SUV, 4x4</td></tr>
            </tbody>
        </table>""",
    
    "rutas_viaje": """
        <table>
            <thead>
                <tr>
                    <th>Ruta</th>
                    <th>Distancia</th>
                    <th>Tiempo</th>
                    <th>Vehículo Recomendado</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Santiago → Viña del Mar</td><td>120 km</td><td>1h 30min</td><td>Sedán o City Car</td></tr>
                <tr><td>Santiago → La Serena</td><td>470 km</td><td>5h 30min</td><td>SUV o Sedán</td></tr>
                <tr><td>Santiago → Pucón</td><td>780 km</td><td>8h 30min</td><td>SUV</td></tr>
                <tr><td>Puerto Montt → Coyhaique</td><td>590 km</td><td>10h</td><td>4x4 / Camioneta</td></tr>
                <tr><td>Calama → San Pedro de Atacama</td><td>100 km</td><td>1h 30min</td><td>SUV o 4x4</td></tr>
                <tr><td>Punta Arenas → Torres del Paine</td><td>310 km</td><td>4h</td><td>4x4</td></tr>
            </tbody>
        </table>""",
    
    "seguros": """
        <table>
            <thead>
                <tr>
                    <th>Cobertura</th>
                    <th>¿Qué Cubre?</th>
                    <th>Deducible</th>
                    <th>Incluida por Defecto</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Básica</strong></td><td>Responsabilidad civil a terceros</td><td>Alto</td><td>✅ Sí</td></tr>
                <tr><td><strong>CDW</strong></td><td>Daños al vehículo arrendado</td><td>Reducido (UF 15-25)</td><td>Opcional</td></tr>
                <tr><td><strong>SCDW</strong></td><td>CDW extendido, menor deducible</td><td>Muy bajo (UF 5-10)</td><td>Opcional</td></tr>
                <tr><td><strong>PAI</strong></td><td>Accidentes personales del conductor</td><td>Sin deducible</td><td>Opcional</td></tr>
                <tr><td><strong>Robo</strong></td><td>Hurto o robo total del vehículo</td><td>Según contrato</td><td>Incluida parcialmente</td></tr>
            </tbody>
        </table>""",
    
    "requisitos": """
        <table>
            <thead>
                <tr>
                    <th>Requisito</th>
                    <th>Chilenos</th>
                    <th>Extranjeros</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Edad mínima</td><td>22 años</td><td>22 años</td></tr>
                <tr><td>Documento de identidad</td><td>Cédula de identidad</td><td>Pasaporte vigente</td></tr>
                <tr><td>Licencia de conducir</td><td>Clase B vigente</td><td>Licencia internacional o del país + traducción</td></tr>
                <tr><td>Medio de pago</td><td>Tarjeta de crédito bancaria</td><td>Tarjeta de crédito internacional</td></tr>
                <tr><td>Garantía</td><td>Desde $450.000 CLP</td><td>Desde $700.000 CLP</td></tr>
            </tbody>
        </table>""",
    
    "comparativa_vehiculos": """
        <table>
            <thead>
                <tr>
                    <th>Categoría</th>
                    <th>Pasajeros</th>
                    <th>Equipaje</th>
                    <th>Ideal Para</th>
                    <th>Ejemplo Flota Mitta</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>City Car</td><td>4</td><td>1-2 maletas</td><td>Ciudad, uso diario</td><td>Suzuki Baleno</td></tr>
                <tr><td>Sedán</td><td>5</td><td>2-3 maletas</td><td>Carretera, negocios</td><td>Toyota Yaris</td></tr>
                <tr><td>SUV Compacto</td><td>5</td><td>3-4 maletas</td><td>Familia, mix ciudad-ruta</td><td>Hyundai Tucson</td></tr>
                <tr><td>SUV Full</td><td>7</td><td>4+ maletas</td><td>Familia grande, aventura</td><td>Toyota Fortuner</td></tr>
                <tr><td>Camioneta 4x4</td><td>5</td><td>Carga pesada</td><td>Off-road, minería, nieve</td><td>Toyota Hilux</td></tr>
            </tbody>
        </table>""",
    
    "incidentes": """
        <table>
            <thead>
                <tr>
                    <th>Situación</th>
                    <th>¿Qué Hacer?</th>
                    <th>¿Quién Paga?</th>
                    <th>Contacto Mitta</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Pana mecánica</td><td>Llamar a asistencia 24/7</td><td>Mitta (si no es negligencia)</td><td>600 320 3000</td></tr>
                <tr><td>Accidente con terceros</td><td>Constancia en Carabineros + aviso</td><td>Seguro (según cobertura)</td><td>600 320 3000</td></tr>
                <tr><td>Multa de tránsito</td><td>Mitta te notifica</td><td>Conductor (siempre)</td><td>Portal web</td></tr>
                <tr><td>TAG / Peajes</td><td>Automático por TAG del vehículo</td><td>Conductor (siempre)</td><td>Factura mensual</td></tr>
                <tr><td>Robo o hurto</td><td>Denuncia en Carabineros + aviso</td><td>Seguro (según póliza)</td><td>600 320 3000</td></tr>
            </tbody>
        </table>""",
    
    "ocasiones_especiales": """
        <table>
            <thead>
                <tr>
                    <th>Ocasión</th>
                    <th>Vehículo Sugerido</th>
                    <th>Días Típicos</th>
                    <th>Tip Mitta</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Matrimonio</td><td>SUV Premium / Sedán ejecutivo</td><td>1-3 días</td><td>Reserva con 2+ semanas de anticipación</td></tr>
                <tr><td>Fin de semana largo</td><td>SUV o Camioneta</td><td>3-4 días</td><td>Retira el jueves para mejor tarifa</td></tr>
                <tr><td>Vacaciones familiares</td><td>SUV 7 pasajeros</td><td>7-14 días</td><td>Tarifa semanal más económica</td></tr>
                <tr><td>Viaje con mascotas</td><td>SUV con cargo amplio</td><td>Variable</td><td>Solicita cobertura adicional de tapiz</td></tr>
                <tr><td>Viaje con niños</td><td>SUV con Isofix</td><td>Variable</td><td>Silla infantil disponible como extra</td></tr>
            </tbody>
        </table>""",
    
    "flotas_lop": """
        <table>
            <thead>
                <tr>
                    <th>Criterio</th>
                    <th>Leasing Operativo (Mitta)</th>
                    <th>Compra de Flota</th>
                    <th>Renting Flexible</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Inversión inicial (CAPEX)</td><td>$0</td><td>100% del valor</td><td>$0</td></tr>
                <tr><td>Tratamiento contable</td><td>Gasto operacional (OPEX)</td><td>Activo fijo</td><td>Gasto operacional</td></tr>
                <tr><td>IVA recuperable</td><td>✅ Sí (cuota mensual)</td><td>Solo en la compra</td><td>✅ Sí</td></tr>
                <tr><td>Mantención incluida</td><td>✅ Sí</td><td>❌ No</td><td>✅ Sí</td></tr>
                <tr><td>Plazo</td><td>24-48 meses</td><td>Indefinido</td><td>3-12 meses</td></tr>
                <tr><td>Depreciación en balance</td><td>No aplica</td><td>Sí (activo se deprecia)</td><td>No aplica</td></tr>
            </tbody>
        </table>""",
    
    "renting_flexible": """
        <table>
            <thead>
                <tr>
                    <th>Criterio</th>
                    <th>Renting Flexible (Mitta)</th>
                    <th>Crédito Automotriz</th>
                    <th>Arriendo Diario</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Plazo mínimo</td><td>3 meses</td><td>12-60 meses</td><td>1 día</td></tr>
                <tr><td>Inversión inicial</td><td>$0</td><td>Pie 10-20%</td><td>Garantía diaria</td></tr>
                <tr><td>Mantención</td><td>✅ Incluida</td><td>❌ Por tu cuenta</td><td>✅ Incluida</td></tr>
                <tr><td>Seguro</td><td>✅ Incluido</td><td>Aparte</td><td>✅ Básico incluido</td></tr>
                <tr><td>Cambio de vehículo</td><td>✅ Al renovar</td><td>❌ No</td><td>✅ Cada reserva</td></tr>
                <tr><td>Costo mensual (referencia)</td><td>$350.000 – $600.000</td><td>$250.000+ cuota</td><td>$900.000+ (30 días)</td></tr>
            </tbody>
        </table>""",
    
    "precios": """
        <table>
            <thead>
                <tr>
                    <th>Categoría</th>
                    <th>Tarifa Diaria (ref.)</th>
                    <th>Tarifa Semanal (ref.)</th>
                    <th>Incluye</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>City Car</td><td>Desde $25.000</td><td>Desde $140.000</td><td>Seguro básico + TAG + km libres</td></tr>
                <tr><td>Sedán</td><td>Desde $30.000</td><td>Desde $170.000</td><td>Seguro básico + TAG + km libres</td></tr>
                <tr><td>SUV Compacto</td><td>Desde $45.000</td><td>Desde $250.000</td><td>Seguro básico + TAG + km libres</td></tr>
                <tr><td>SUV Full / 4x4</td><td>Desde $65.000</td><td>Desde $380.000</td><td>Seguro básico + TAG + km libres</td></tr>
                <tr><td>Camioneta</td><td>Desde $55.000</td><td>Desde $320.000</td><td>Seguro básico + TAG + km libres</td></tr>
            </tbody>
        </table>""",
    
    "cyber_ofertas": """
        <table>
            <thead>
                <tr>
                    <th>Oferta Cyber</th>
                    <th>Beneficio</th>
                    <th>Aplica Para</th>
                    <th>Condición</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Descuento Reserva Anticipada</td><td>Hasta 30% off tarifa diaria</td><td>Rent a Car (todos)</td><td>Reserva online durante Cyber</td></tr>
                <tr><td>Día Extra Gratis</td><td>+1 día sin costo</td><td>Arriendos de 3+ días</td><td>Código Cyber vigente</td></tr>
                <tr><td>Upgrade de Categoría</td><td>SUV por precio de Sedán</td><td>Sujeto a disponibilidad</td><td>Reserva mín. 5 días</td></tr>
                <tr><td>Cuota Bonificada MittaGO</td><td>Primer mes con descuento</td><td>Suscripciones nuevas</td><td>Firma durante semana Cyber</td></tr>
                <tr><td>Flota Empresas</td><td>Tarifa corporativa especial</td><td>Contratos 6+ meses</td><td>Cotización en Cyber</td></tr>
            </tbody>
        </table>""",
    
    "planes_empresa": """
        <table>
            <thead>
                <tr>
                    <th>Plan</th>
                    <th>Ideal Para</th>
                    <th>Plazo</th>
                    <th>Beneficio Clave</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>MittaGO Individual</td><td>Profesionales independientes</td><td>Desde 3 meses</td><td>Sin pie, cuota fija</td></tr>
                <tr><td>MittaGO Pyme</td><td>Empresas 1-10 vehículos</td><td>Desde 6 meses</td><td>Facturación como OPEX</td></tr>
                <tr><td>Leasing Operativo</td><td>Flotas corporativas 10+</td><td>24-48 meses</td><td>IVA recuperable, sin CAPEX</td></tr>
                <tr><td>Renting Flexible</td><td>Proyectos temporales</td><td>3-12 meses</td><td>Escalabilidad inmediata</td></tr>
            </tbody>
        </table>""",
    
    "tecnologia": """
        <table>
            <thead>
                <tr>
                    <th>Sistema ADAS</th>
                    <th>Función</th>
                    <th>Beneficio</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Frenado autónomo de emergencia</td><td>Detecta obstáculos y frena solo</td><td>Reduce hasta 40% de colisiones traseras</td></tr>
                <tr><td>Alerta de cambio de carril</td><td>Avisa si sales del carril sin señalizar</td><td>Previene accidentes por distracción</td></tr>
                <tr><td>Control de crucero adaptativo</td><td>Mantiene distancia con el auto de adelante</td><td>Reduce fatiga en carretera</td></tr>
                <tr><td>Cámara de retroceso 360°</td><td>Vista panorámica al estacionar</td><td>Elimina puntos ciegos</td></tr>
                <tr><td>Detección de punto ciego</td><td>Alerta visual en espejos laterales</td><td>Cambios de pista más seguros</td></tr>
            </tbody>
        </table>""",
    
    "servicios_incluidos": """
        <table>
            <thead>
                <tr>
                    <th>Servicio</th>
                    <th>¿Incluido en MittaGO?</th>
                    <th>En auto propio</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Mantención preventiva</td><td>✅ Incluida</td><td>$150.000-$400.000/año</td></tr>
                <tr><td>Seguro automotriz</td><td>✅ Incluido</td><td>$400.000-$800.000/año</td></tr>
                <tr><td>Permiso de circulación</td><td>✅ Incluido</td><td>$150.000-$350.000/año</td></tr>
                <tr><td>Asistencia en ruta 24/7</td><td>✅ Incluida</td><td>$50.000-$100.000/año</td></tr>
                <tr><td>Auto de reemplazo</td><td>✅ Incluido</td><td>No disponible</td></tr>
                <tr><td>Revisión técnica</td><td>✅ Incluida</td><td>$30.000-$50.000</td></tr>
            </tbody>
        </table>""",

    "requisitos_extranjero": """
        <table>
            <thead>
                <tr>
                    <th>Requisito</th>
                    <th>Detalle</th>
                    <th>Observación</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Edad mínima</td><td>22 años cumplidos</td><td>Sin excepciones</td></tr>
                <tr><td>Pasaporte</td><td>Vigente, con entrada registrada</td><td>PDI debe tener registro</td></tr>
                <tr><td>Licencia de conducir</td><td>Internacional o del país de origen</td><td>Traducción notarial si no es en español/inglés</td></tr>
                <tr><td>Tarjeta de crédito</td><td>Internacional, a nombre del titular</td><td>Garantía desde $700.000 CLP</td></tr>
                <tr><td>Antigüedad licencia</td><td>Mínimo 2 años</td><td>Verificable</td></tr>
            </tbody>
        </table>""",
    
    "glosario": """
        <table>
            <thead>
                <tr>
                    <th>Término</th>
                    <th>Definición</th>
                    <th>Ejemplo</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Renting</td><td>Arriendo de vehículo a mediano plazo con servicios incluidos</td><td>MittaGO: cuota mensual todo incluido</td></tr>
                <tr><td>Leasing Operativo</td><td>Contrato B2B de flota vehicular a largo plazo</td><td>Empresa arrienda 20 camionetas por 36 meses</td></tr>
                <tr><td>CDW</td><td>Collision Damage Waiver — reducción de deducible por daños</td><td>Reduce responsabilidad de UF 60 a UF 15</td></tr>
                <tr><td>Drop-Off</td><td>Devolver el vehículo en una ciudad distinta al retiro</td><td>Retiras en Santiago, devuelves en Puerto Montt</td></tr>
                <tr><td>OPEX</td><td>Gasto operacional — deducible de impuestos</td><td>La cuota de renting se registra como gasto</td></tr>
            </tbody>
        </table>""",
    
    "tendencias": """
        <table>
            <thead>
                <tr>
                    <th>Tendencia</th>
                    <th>Impacto en Chile</th>
                    <th>Solución Mitta</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Economía circular</td><td>Maximizar uso por vehículo producido</td><td>Flota rotativa, múltiples usuarios por auto</td></tr>
                <tr><td>Movilidad como Servicio (MaaS)</td><td>Pagar por uso, no por propiedad</td><td>Suscripción MittaGO</td></tr>
                <tr><td>Electromovilidad</td><td>Regulación y subsidios crecientes</td><td>Incorporación gradual de híbridos/eléctricos</td></tr>
                <tr><td>Flotas compartidas</td><td>Eficiencia corporativa</td><td>Leasing Operativo multi-conductor</td></tr>
            </tbody>
        </table>""",
    
    "guia_rac": """
        <table>
            <thead>
                <tr>
                    <th>Criterio</th>
                    <th>Rent a Car Económico</th>
                    <th>Rent a Car Premium (Mitta)</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Flota</td><td>Limitada, modelos antiguos</td><td>+2.500 vehículos, modelos recientes</td></tr>
                <tr><td>Cobertura nacional</td><td>1-5 sucursales</td><td>+80 sucursales en 14 regiones</td></tr>
                <tr><td>Asistencia en ruta</td><td>Limitada o tercerizada</td><td>24/7 con red propia</td></tr>
                <tr><td>Seguro incluido</td><td>Solo básico</td><td>Básico + opciones CDW, SCDW, PAI</td></tr>
                <tr><td>Respaldo corporativo</td><td>Variable</td><td>Mitsui & Co., Ltd. (Japón)</td></tr>
            </tbody>
        </table>""",
    
    "comparativa_general": """
        <table>
            <thead>
                <tr>
                    <th>Aspecto</th>
                    <th>Opción Tradicional</th>
                    <th>Solución Mitta</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Inversión inicial</td><td>Alta (compra o pie)</td><td>$0 — solo cuota mensual</td></tr>
                <tr><td>Mantenciones</td><td>Por tu cuenta</td><td>Incluidas en la cuota</td></tr>
                <tr><td>Seguro</td><td>Gestionas por separado</td><td>Incluido</td></tr>
                <tr><td>Flexibilidad</td><td>Atado a largo plazo</td><td>Cambias de auto o devuelves</td></tr>
                <tr><td>Cobertura geográfica</td><td>Depende de ti</td><td>+80 sucursales, 14 regiones</td></tr>
            </tbody>
        </table>""",
}


# ═══════════════════════════════════════════════════════════════
# PHASE 1: INJECT TABLES
# ═══════════════════════════════════════════════════════════════

def phase1_inject_tables():
    print("\n" + "="*60)
    print("  FASE 1: Inyectar Tablas Comparativas (43 arts)")
    print("="*60)
    
    for cat_name, cat_dir in ALL_DIRS.items():
        for fpath in sorted(cat_dir.glob("*.html")):
            content = fpath.read_text(encoding='utf-8')
            
            if has_content_table(content):
                continue
            
            h1 = get_h1(content)
            h2s = get_h2s(content)
            h2_texts = [t for _, t in h2s]
            
            theme = detect_theme(fpath.name, h1, h2_texts, cat_name)
            table_html = TABLE_TEMPLATES.get(theme, TABLE_TEMPLATES["comparativa_general"])
            
            # Find insertion point: before CTA, or before FAQ, or before matrix
            insertion_done = False
            for marker in ['class="cta-container"', 'class="faq-section"', 
                          '<!-- INICIO MATRIZ VISUAL', '</article>']:
                if marker in content:
                    # Insert a contextual H2 + table before the marker
                    table_block = f'\n        <h2 id="tabla-comparativa">Tabla Comparativa</h2>\n{table_html}\n\n'
                    content = content.replace(marker, f'{table_block}        {marker}', 1)
                    insertion_done = True
                    break
            
            if not insertion_done:
                # Fallback: insert before </body>
                table_block = f'\n<h2 id="tabla-comparativa">Tabla Comparativa</h2>\n{table_html}\n'
                content = content.replace('</body>', f'{table_block}\n</body>')
            
            fpath.write_text(content, encoding='utf-8')
            stats["tables"] += 1
            print(f"  ✅ {fpath.name}: tabla [{theme}] insertada")
    
    print(f"\n  📊 Fase 1: {stats['tables']} tablas insertadas")


# ═══════════════════════════════════════════════════════════════
# PHASE 2: INJECT FAQ SECTIONS + SCHEMA
# ═══════════════════════════════════════════════════════════════

def generate_faq_items(h1, h2_texts, category, filename):
    """Generate 3 contextual FAQ items based on article content."""
    
    # Q1: Always based on the title
    q1_text = h1
    if not q1_text.startswith("¿"):
        q1_text = f"¿{q1_text}?"
    if not q1_text.endswith("?"):
        q1_text = q1_text.rstrip(".") + "?"
    
    # Detect theme for contextual Q2 and Q3
    text = f"{h1} {' '.join(h2_texts)} {filename}".lower()
    
    faqs = []
    
    # Q1: Title-based
    if "suscripci" in text or "mittago" in text:
        faqs.append(("¿Cuáles son los requisitos para suscribirse a MittaGO?",
                     "Para acceder a un plan MittaGO necesitas ser mayor de 22 años, contar con licencia de conducir vigente, RUT y aprobar una evaluación comercial digital con un medio de pago. El proceso es 100% online y se completa en menos de 48 horas."))
        faqs.append(("¿Qué incluye la cuota mensual de MittaGO?",
                     "La cuota mensual de MittaGO incluye el uso del vehículo, seguro automotriz, mantenciones preventivas programadas, permiso de circulación, asistencia en ruta 24/7 y auto de reemplazo. El conductor asume combustible, TAG y multas."))
        faqs.append(("¿Puedo cambiar de auto durante mi suscripción?",
                     "Sí. Al finalizar tu periodo inicial puedes cambiar de modelo sin penalización. Si tus necesidades cambian, simplemente devuelves el vehículo actual y firmas un acuerdo actualizado para un modelo diferente."))
    elif "leasing" in text or "flota" in text or "corporativ" in text:
        faqs.append(("¿Cuál es la diferencia entre leasing operativo y compra de flota?",
                     "En el leasing operativo no adquieres el vehículo: pagas una cuota mensual que incluye mantención, seguros y es deducible como gasto operacional (OPEX). En la compra, el vehículo es un activo fijo que se deprecia y genera costos adicionales de administración."))
        faqs.append(("¿El leasing operativo permite recuperar IVA?",
                     "Sí. Al ser un servicio y no una compra, la cuota mensual del leasing operativo genera crédito fiscal de IVA recuperable en cada factura mensual, lo que representa una ventaja tributaria significativa para las empresas."))
        faqs.append(("¿Qué plazo tiene un contrato de leasing operativo con Mitta?",
                     "Los contratos de leasing operativo con Mitta van desde 24 hasta 48 meses, dependiendo del tipo de flota y las necesidades de la empresa. Al término, puedes renovar, cambiar vehículos o devolver la flota."))
    elif any(w in text for w in ["aeropuerto", "primera vez", "requisito", "extranjero"]):
        faqs.append(("¿Necesito tarjeta de crédito para arrendar un auto en Chile?",
                     "Sí. Es obligatorio presentar una tarjeta de crédito bancaria a nombre del conductor titular. Se realiza un cargo temporal como garantía que varía según la categoría del vehículo y los días de arriendo. El monto se libera al devolver el auto en buenas condiciones."))
        faqs.append(("¿Cuál es la edad mínima para arrendar un auto con Mitta?",
                     "La edad mínima para arrendar un vehículo con Mitta es de 22 años cumplidos. Este requisito aplica tanto para chilenos como para extranjeros sin excepciones."))
        faqs.append(("¿Puedo arrendar un auto en una ciudad y devolverlo en otra?",
                     "Sí, Mitta ofrece el servicio Drop-Off que te permite retirar el vehículo en una sucursal y devolverlo en otra ciudad. Este servicio tiene un costo adicional que depende de la distancia entre sucursales."))
    elif any(w in text for w in ["ruta", "roadtrip", "carretera", "viaj", "nieve", "atacama", "austral"]):
        faqs.append(("¿Qué tipo de vehículo necesito para viajar por carretera en Chile?",
                     "Depende de la ruta. Para la zona central y carreteras pavimentadas, un sedán o SUV compacto es suficiente. Para la Carretera Austral, zonas de nieve o caminos de ripio, se recomienda una camioneta 4x4 o SUV con tracción integral."))
        faqs.append(("¿El arriendo de auto incluye kilómetros libres?",
                     "Sí. Los arriendos con Mitta Rent a Car incluyen kilómetros libres en la mayoría de las tarifas. Esto significa que puedes recorrer la distancia que necesites sin cargos adicionales por kilometraje."))
        faqs.append(("¿Puedo llevar el auto arrendado fuera de Chile?",
                     "Cruzar fronteras requiere autorización previa y documentación adicional. Mitta ofrece la opción de cruzar a Argentina desde ciertas sucursales, con un recargo por permiso fronterizo y seguro internacional."))
    elif any(w in text for w in ["seguro", "cdw", "cobertura", "accidente", "pana", "siniestro"]):
        faqs.append(("¿Qué pasa si tengo un accidente con el auto arrendado?",
                     "Debes contactar inmediatamente a la línea de asistencia Mitta (24/7) y, si hay terceros involucrados, realizar la constancia en Carabineros. El seguro básico incluido cubre responsabilidad civil. Si contrataste CDW o SCDW, tu responsabilidad económica se reduce significativamente."))
        faqs.append(("¿Qué es el CDW y vale la pena contratarlo?",
                     "El CDW (Collision Damage Waiver) es una reducción de deducible que limita tu responsabilidad económica en caso de daños al vehículo. Sin CDW, el deducible puede superar las UF 50. Con CDW, baja a UF 15-25. Es altamente recomendable para viajes largos."))
        faqs.append(("¿Quién paga las multas de tránsito durante el arriendo?",
                     "Las multas de tránsito son responsabilidad exclusiva del conductor. Mitta te notificará si se registra alguna infracción asociada al vehículo durante tu periodo de arriendo para que puedas gestionarla."))
    elif "cyber" in text:
        faqs.append(("¿Las ofertas Cyber aplican para todos los vehículos?",
                     "Las ofertas Cyber de Mitta aplican para las categorías y modelos indicados en cada promoción. La disponibilidad está sujeta al stock vigente durante el periodo Cyber. Se recomienda reservar con anticipación para asegurar el mejor precio."))
        faqs.append(("¿Puedo reservar durante el Cyber y usar el auto después?",
                     "Sí. Las reservas realizadas durante el Cyber aseguran la tarifa promocional para las fechas que selecciones, incluso si el viaje es semanas después. La fecha de uso puede ser posterior al evento Cyber."))
        faqs.append(("¿Las ofertas Cyber aplican para suscripciones MittaGO?",
                     "Sí. Durante el Cyber, MittaGO ofrece cuotas bonificadas para nuevas suscripciones. El descuento aplica sobre los primeros meses del contrato y se mantiene durante el periodo promocional indicado."))
    else:
        # Generic FAQs
        faqs.append(("¿Cuánto cuesta arrendar un auto con Mitta en Chile?",
                     "Las tarifas varían según la categoría del vehículo y los días de arriendo. Un city car parte desde $25.000 diarios, un sedán desde $30.000, un SUV desde $45.000 y una camioneta 4x4 desde $55.000. Todas las tarifas incluyen seguro básico, TAG y kilómetros libres."))
        faqs.append(("¿Mitta tiene sucursales en todo Chile?",
                     "Sí. Mitta cuenta con más de 80 sucursales en 14 regiones del país, la mayor red de arriendo de vehículos en Chile según ANAC. Esto incluye presencia en los principales aeropuertos, ciudades y destinos turísticos."))
        faqs.append(("¿Qué documentos necesito para arrendar un auto?",
                     "Necesitas tener 22 años cumplidos, cédula de identidad o pasaporte vigente, licencia de conducir vigente y tarjeta de crédito bancaria a nombre del titular para la garantía del arriendo."))
    
    return faqs


def phase2_inject_faq():
    print("\n" + "="*60)
    print("  FASE 2: Inyectar FAQ Sections + Schema (51 arts)")
    print("="*60)
    
    for cat_name, cat_dir in ALL_DIRS.items():
        for fpath in sorted(cat_dir.glob("*.html")):
            content = fpath.read_text(encoding='utf-8')
            
            if has_faq_section(content):
                continue
            
            h1 = get_h1(content)
            h2s = get_h2s(content)
            h2_texts = [t for _, t in h2s]
            
            faqs = generate_faq_items(h1, h2_texts, cat_name, fpath.name)
            
            # Build FAQ HTML
            faq_html = '\n        <div class="faq-section">\n            <h2>Preguntas Frecuentes</h2>\n'
            for q, a in faqs:
                faq_html += f'            <div class="faq-item">\n'
                faq_html += f'                <div class="faq-question">{q}</div>\n'
                faq_html += f'                <div class="faq-answer">{a}</div>\n'
                faq_html += f'            </div>\n'
            faq_html += '        </div>\n'
            
            # Insert before matrix or before </article>
            inserted = False
            for marker in ['<!-- INICIO MATRIZ VISUAL', '</article>']:
                if marker in content:
                    content = content.replace(marker, f'{faq_html}\n    {marker}', 1)
                    inserted = True
                    break
            
            if not inserted:
                content = content.replace('</body>', f'{faq_html}\n</body>')
            
            # Add FAQ Schema to existing JSON-LD @graph
            faq_schema_entities = []
            for q, a in faqs:
                faq_schema_entities.append({
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a
                    }
                })
            
            faq_schema = {"@type": "FAQPage", "mainEntity": faq_schema_entities}
            
            # Try to add to existing @graph
            schemas = list(re.finditer(r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.IGNORECASE | re.DOTALL))
            added_schema = False
            
            if schemas:
                for schema_match in schemas:
                    try:
                        schema_data = json.loads(schema_match.group(1))
                        if "@graph" in schema_data:
                            # Check if FAQPage already exists
                            has_faq = any(item.get("@type") == "FAQPage" for item in schema_data["@graph"])
                            if not has_faq:
                                schema_data["@graph"].append(faq_schema)
                                new_json = json.dumps(schema_data, ensure_ascii=False, indent=2)
                                new_block = f'<script type="application/ld+json">\n{new_json}\n</script>'
                                content = content[:schema_match.start()] + new_block + content[schema_match.end():]
                                added_schema = True
                                break
                    except json.JSONDecodeError:
                        continue
            
            if not added_schema:
                # Add as separate script
                faq_full = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_entities}
                faq_block = f'\n<script type="application/ld+json">\n{json.dumps(faq_full, ensure_ascii=False, indent=2)}\n</script>'
                content = content.replace('</body>', f'{faq_block}\n</body>')
            
            fpath.write_text(content, encoding='utf-8')
            stats["faqs"] += 1
            print(f"  ✅ {fpath.name}: FAQ ({len(faqs)} Qs) + Schema insertados")
    
    print(f"\n  📊 Fase 2: {stats['faqs']} FAQ sections insertadas")


# ═══════════════════════════════════════════════════════════════
# PHASE 3: REFORMULATE H2s AS QUESTIONS
# ═══════════════════════════════════════════════════════════════

# Mapping of common H2 patterns to question forms
H2_TRANSFORMS = [
    (r'^(Beneficios|Ventajas)\s+(de[l]?\s+)', '¿Cuáles son los beneficios de '),
    (r'^(Requisitos|Documentos)\s+(para|y|obligatorios)', '¿Qué requisitos necesitas para '),
    (r'^(Cobertura|Alcance)\s+', '¿Qué cobertura tiene '),
    (r'^(Costos?|Precios?|Tarifas?)\s+', '¿Cuánto cuestan '),
    (r'^(Pasos?|Proceso|Procedimiento)\s+', '¿Cuáles son los pasos para '),
    (r'^(Diferencias?)\s+entre\s+', '¿Cuál es la diferencia entre '),
    (r'^(Opciones|Alternativas)\s+', '¿Qué opciones tienes de '),
    (r'^(Ventajas?)\s+de\s+', '¿Qué ventajas tiene '),
    (r'^(Equipamiento|Accesorios)\s+', '¿Qué equipamiento incluye '),
    (r'^(Planificación|Preparación)\s+', '¿Cómo planificar '),
]


def reformulate_h2(h2_text):
    """Try to reformulate a declarative H2 as a question."""
    text = h2_text.strip()
    
    # Already a question
    if text.startswith("¿") or text.endswith("?"):
        return None
    
    # Skip numbered headings, TOC, FAQ, etc
    if re.match(r'^\d+\.?\s', text) or text.lower() in ['contenido', 'preguntas frecuentes', 
                                                           'preguntas frecuentes (faq)', 'tabla comparativa',
                                                           'tabla de contenidos']:
        return None
    
    # Try pattern-based transforms
    for pattern, replacement in H2_TRANSFORMS:
        if re.match(pattern, text, re.IGNORECASE):
            rest = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
            new_text = f"{replacement}{rest.lower().rstrip('.')}?"
            return new_text
    
    # Generic transforms for common patterns
    lower = text.lower()
    if lower.startswith("el ") or lower.startswith("la ") or lower.startswith("los ") or lower.startswith("las "):
        return f"¿Qué es {lower.rstrip('.')}?"
    
    # Verb-starting patterns
    if lower.startswith("cómo ") or lower.startswith("como "):
        if not text.startswith("¿"):
            return f"¿{text.rstrip('.')}?"
    
    # "Por qué" patterns
    if lower.startswith("por qué ") or lower.startswith("por que "):
        if not text.startswith("¿"):
            return f"¿{text.rstrip('.')}?"
    
    return None


def phase3_reformulate_headings():
    print("\n" + "="*60)
    print("  FASE 3: Reformular H2 como Preguntas (45 arts)")
    print("="*60)
    
    for cat_name, cat_dir in ALL_DIRS.items():
        for fpath in sorted(cat_dir.glob("*.html")):
            content = fpath.read_text(encoding='utf-8')
            
            # Check current question ratio
            h2_all = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.IGNORECASE | re.DOTALL)
            h2_questions = [h for h in h2_all if '?' in strip_tags(h)]
            
            if not h2_all:
                continue
            
            q_ratio = len(h2_questions) / len(h2_all)
            if q_ratio >= 0.4:  # Already good enough
                continue
            
            # Find H2s to reformulate (max 2 per article)
            modified = False
            reformulations = 0
            
            for h2_match in re.finditer(r'(<h2[^>]*>)(.*?)(</h2>)', content, re.IGNORECASE | re.DOTALL):
                if reformulations >= 2:
                    break
                
                full_tag = h2_match.group(0)
                open_tag = h2_match.group(1)
                h2_text = h2_match.group(2)
                close_tag = h2_match.group(3)
                
                clean_text = strip_tags(h2_text)
                new_text = reformulate_h2(clean_text)
                
                if new_text:
                    # Replace text but keep any inner HTML formatting
                    if '<' in h2_text:  # Has inner tags
                        # Just replace the clean text content
                        new_h2 = f"{open_tag}{new_text}{close_tag}"
                    else:
                        new_h2 = f"{open_tag}{new_text}{close_tag}"
                    
                    content = content.replace(full_tag, new_h2, 1)
                    reformulations += 1
                    modified = True
            
            if modified:
                fpath.write_text(content, encoding='utf-8')
                stats["q_headings"] += 1
                print(f"  ✅ {fpath.name}: {reformulations} H2s reformulados")
    
    print(f"\n  📊 Fase 3: {stats['q_headings']} artículos con H2s reformulados")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("="*60)
    print("  MITTA CONTENT IMPROVEMENT ENGINE v1.0")
    print("  3 Fases de Mejora de Contenido")
    print("="*60)
    
    phase1_inject_tables()
    phase2_inject_faq()
    phase3_reformulate_headings()
    
    print("\n" + "="*60)
    print("  RESUMEN FINAL")
    print("="*60)
    print(f"  Fase 1 (Tablas):       {stats['tables']} artículos")
    print(f"  Fase 2 (FAQ+Schema):   {stats['faqs']} artículos")
    print(f"  Fase 3 (Q-Headings):   {stats['q_headings']} artículos")
    total = stats['tables'] + stats['faqs'] + stats['q_headings']
    print(f"  ─────────────────────────────────")
    print(f"  TOTAL:                 {total} modificaciones")
    if stats['errors']:
        print(f"\n  ⚠️  Errores: {len(stats['errors'])}")
        for e in stats['errors']:
            print(f"    • {e}")
    print()
    print("✅ Mejora de contenido completada. Ejecute re-auditoría.")
