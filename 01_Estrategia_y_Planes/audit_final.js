#!/usr/bin/env node
/**
 * audit_final.js — Script de Auditoría Automatizada v3.0
 * Proyecto: MITTA / MittaGO — INMedios
 *
 * Ejecuta los checks cuantitativos de las 15 capas del Manual de Auditoría.
 *
 * Uso:
 *   node audit_final.js --brand mitta  --dir ./02_Contenidos_Redactados/Mitta/finales/
 *   node audit_final.js --brand mittago --dir ./02_Contenidos_Redactados/MittaGO/finales/
 */

const fs = require('fs');
const path = require('path');

// ─── CLI Args ────────────────────────────────────────────────
const args = process.argv.slice(2);
const brandIdx = args.indexOf('--brand');
const dirIdx = args.indexOf('--dir');

if (brandIdx === -1 || dirIdx === -1) {
  console.error('Uso: node audit_final.js --brand <mitta|mittago> --dir <ruta>');
  process.exit(1);
}

const BRAND = args[brandIdx + 1]; // 'mitta' | 'mittago'
const DIR = args[dirIdx + 1];

if (!['mitta', 'mittago'].includes(BRAND)) {
  console.error('Brand debe ser "mitta" o "mittago"');
  process.exit(1);
}

// ─── Constants ───────────────────────────────────────────────
const DOMAIN_MITTA = 'mitta.cl';
const DOMAIN_MITTAGO = 'mittago.cl';

const MULETILLAS_IA = [
  'es importante destacar que',
  'cabe mencionar que',
  'en este sentido',
  'sin lugar a dudas',
  'en la actualidad',
  'es fundamental señalar',
  'no hay que olvidar que',
  'vale la pena mencionar',
  'es importante señalar',
  'como hemos mencionado',
  'a lo largo de este artículo',
  'en conclusión podemos decir',
];

const EEAT_MARKERS = [
  /mitsui/i,
  /65\s*años/i,
  /sucursal/i,
  /presencia\s+(en\s+)?\d+\s+región/i,
  /80\+?\s*sucursales/i,
  /asistencia\s+24/i,
  /asistencia\s+en\s+ruta/i,
  /carbon\s*neutral/i,
  /certificaci/i,
  /tag\s+incluido/i,
  /segundo\s+conductor\s+sin\s+costo/i,
  /aeropuerto\s+arturo\s+merino/i,
  /amb/i,
  /cmf/i,
  /cuota\s+fija/i,
  /todo\s+incluido/i,
];

const TERMINOS_PROHIBIDOS_MITTAGO = [
  // "arriendo" como referencia al servicio de MittaGO (no como comparación a otro modelo)
  // Se busca en contexto amplio
];

// ─── Helpers ─────────────────────────────────────────────────
function stripHtml(html) {
  return html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&[a-z]+;/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function countWords(text) {
  return text.split(/\s+/).filter(w => w.length > 0).length;
}

function extractBetween(html, startTag, endTag) {
  const startIdx = html.indexOf(startTag);
  if (startIdx === -1) return null;
  const endIdx = html.indexOf(endTag, startIdx);
  if (endIdx === -1) return null;
  return html.substring(startIdx + startTag.length, endIdx);
}

// ─── Checks ──────────────────────────────────────────────────
function auditFile(filePath) {
  const html = fs.readFileSync(filePath, 'utf-8');
  const filename = path.basename(filePath);
  const results = [];

  // ── C4: AEO Block ──
  const hasAnswerBlock = /class="answer-block"/i.test(html);
  results.push({
    capa: 'C4', check: 'Bloque AEO presente',
    pass: hasAnswerBlock, severity: 'ERROR',
  });

  if (hasAnswerBlock) {
    const abMatch = html.match(/class="answer-block"[^>]*>([\s\S]*?)<\/div>/i);
    if (abMatch) {
      const abText = stripHtml(abMatch[1]);
      const abWords = countWords(abText);
      results.push({
        capa: 'C4', check: `Extensión AEO (${abWords} palabras)`,
        pass: abWords >= 30 && abWords <= 50, severity: 'WARNING',
      });
    }
  }

  // ── C5: H1 único ──
  const h1Matches = html.match(/<h1[\s>]/gi) || [];
  results.push({
    capa: 'C5', check: `H1 único (${h1Matches.length} encontrados)`,
    pass: h1Matches.length === 1, severity: 'ERROR',
  });

  // ── C5: IDs en H2 ──
  const h2All = html.match(/<h2[\s][^>]*>/gi) || [];
  const h2WithId = html.match(/<h2[^>]*\sid="[^"]+"/gi) || [];
  results.push({
    capa: 'C5', check: `IDs en H2 (${h2WithId.length}/${h2All.length})`,
    pass: h2All.length > 0 && h2All.length === h2WithId.length, severity: 'WARNING',
  });

  // ── C5: Tabla HTML ──
  const tables = html.match(/<table[\s>]/gi) || [];
  results.push({
    capa: 'C5', check: `Tablas HTML (${tables.length})`,
    pass: tables.length >= 1, severity: 'WARNING',
  });

  // ── C6: JSON-LD ──
  const jsonLdMatch = html.match(/<script\s+type="application\/ld\+json">([\s\S]*?)<\/script>/i);
  let jsonParsed = false;
  let jsonData = null;
  if (jsonLdMatch) {
    try {
      jsonData = JSON.parse(jsonLdMatch[1]);
      jsonParsed = true;
    } catch (e) {
      jsonParsed = false;
    }
  }
  results.push({
    capa: 'C6', check: 'JSON-LD parseable',
    pass: jsonParsed, severity: 'ERROR',
  });

  // ── C6: Nodos @graph ──
  if (jsonData) {
    const graph = jsonData['@graph'] || [jsonData];
    const types = graph.map(n => n['@type']).flat();
    const hasArticle = types.includes('Article') || types.includes('BlogPosting');
    const hasFAQ = types.includes('FAQPage');
    // BreadcrumbList may be in a separate JSON-LD block
    const allJsonLd = html.match(/<script\s+type="application\/ld\+json">([\s\S]*?)<\/script>/gi) || [];
    let hasBreadcrumb = types.includes('BreadcrumbList');
    if (!hasBreadcrumb) {
      allJsonLd.forEach(block => {
        if (block.includes('BreadcrumbList')) hasBreadcrumb = true;
      });
    }
    results.push({
      capa: 'C6', check: `Nodos Schema (Article:${hasArticle} FAQ:${hasFAQ} Bread:${hasBreadcrumb})`,
      pass: hasArticle && hasFAQ, severity: 'ERROR',
    });
    results.push({
      capa: 'C6', check: 'BreadcrumbList en Schema',
      pass: hasBreadcrumb, severity: 'WARNING',
    });

    // ── C6: Dominio Schema ──
    const jsonStr = JSON.stringify(jsonData);
    const expectedDomain = BRAND === 'mitta' ? DOMAIN_MITTA : DOMAIN_MITTAGO;
    const wrongDomain = BRAND === 'mitta' ? DOMAIN_MITTAGO : DOMAIN_MITTA;

    // Check @id fields for wrong domain
    const idMatches = jsonStr.match(/"@id"\s*:\s*"[^"]+"/gi) || [];
    const wrongDomainInId = idMatches.some(m => m.includes(wrongDomain) && !m.includes(expectedDomain));
    results.push({
      capa: 'C6', check: `Dominio Schema (@id correcto: ${expectedDomain})`,
      pass: !wrongDomainInId, severity: 'ERROR',
    });

    // Check logo URL
    const logoMatches = jsonStr.match(/"url"\s*:\s*"https?:\/\/[^"]*logo[^"]*"/gi) || [];
    const wrongLogo = logoMatches.some(m => m.includes(wrongDomain) && !m.includes(expectedDomain));
    results.push({
      capa: 'C6', check: `Logo URL (dominio: ${expectedDomain})`,
      pass: !wrongLogo, severity: 'ERROR',
    });
  }

  // ── C7: Frontmatter ──
  const hasFrontmatter = /^---\s*\n/.test(html) || /class="meta-header"/i.test(html);
  results.push({
    capa: 'C7', check: 'Frontmatter / Meta header',
    pass: hasFrontmatter, severity: 'ERROR',
  });

  // ── C7: Meta title length ──
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  if (titleMatch) {
    const titleLen = titleMatch[1].trim().length;
    results.push({
      capa: 'C7', check: `Meta title (${titleLen} chars)`,
      pass: titleLen >= 50 && titleLen <= 65, severity: 'WARNING',
    });
  }

  // ── C7: Meta description length ──
  const descMatch = html.match(/<meta\s+name="description"\s+content="([^"]*)"/i);
  if (descMatch) {
    const descLen = descMatch[1].length;
    results.push({
      capa: 'C7', check: `Meta description (${descLen} chars)`,
      pass: descLen >= 110 && descLen <= 160, severity: 'WARNING',
    });
  }

  // ── C8: Breadcrumbs ──
  const hasBreadcrumb = /class="breadcrumb"/i.test(html);
  results.push({
    capa: 'C8', check: 'Breadcrumbs presentes',
    pass: hasBreadcrumb, severity: 'ERROR',
  });

  // ── C8: CTA ──
  const expectedCtaDomain = BRAND === 'mitta' ? 'mitta.cl' : 'mittago.cl';
  const ctaRegex = new RegExp(`href="https?://(www\\.)?${expectedCtaDomain.replace('.', '\\.')}`, 'i');
  const hasCta = ctaRegex.test(html);
  results.push({
    capa: 'C8', check: `CTA con enlace a ${expectedCtaDomain}`,
    pass: hasCta, severity: 'ERROR',
  });

  // ── C9: Extensión editorial ──
  // Strip everything except the article body
  const bodyText = stripHtml(html);
  const totalWords = countWords(bodyText);
  results.push({
    capa: 'C9', check: `Extensión editorial (${totalWords} palabras)`,
    pass: totalWords >= 800 && totalWords <= 2000, severity: 'ERROR',
  });

  // ── C9: Párrafos ≤80 palabras ──
  const paragraphs = html.match(/<p[^>]*>([\s\S]*?)<\/p>/gi) || [];
  let longParas = 0;
  paragraphs.forEach(p => {
    const pText = stripHtml(p);
    if (countWords(pText) > 80) longParas++;
  });
  results.push({
    capa: 'C9', check: `Párrafos >80 palabras (${longParas} encontrados)`,
    pass: longParas === 0, severity: 'WARNING',
  });

  // ── C9: Muletillas IA ──
  const lowerHtml = html.toLowerCase();
  let muletillasFound = [];
  MULETILLAS_IA.forEach(m => {
    if (lowerHtml.includes(m)) muletillasFound.push(m);
  });
  results.push({
    capa: 'C9', check: `Muletillas IA (${muletillasFound.length})`,
    pass: muletillasFound.length === 0, severity: 'WARNING',
    detail: muletillasFound.length > 0 ? muletillasFound.join(', ') : undefined,
  });

  // ── C9: FAQ count ──
  // Articles use <div class="faq-question"> or <div class="faq-item"> or <strong>¿...
  const faqItems = html.match(/class="faq-item"/gi) || [];
  const faqQuestionsAlt = html.match(/class="faq-question"/gi) || [];
  const faqStrong = html.match(/<strong[^>]*>\s*¿[^<]+\?/gi) || [];
  const faqCount = Math.max(faqItems.length, faqQuestionsAlt.length, faqStrong.length);
  results.push({
    capa: 'C9', check: `FAQ count (${faqCount}, esperado: 3)`,
    pass: faqCount >= 3, severity: 'ERROR',
  });

  // ── C10: Terminología prohibida MittaGO ──
  if (BRAND === 'mittago') {
    // Check for "arriendo" or "alquiler" used as the service name (not in comparisons)
    // Simple heuristic: count occurrences outside of comparison contexts
    const arriendoCount = (lowerHtml.match(/\barriendo\b/g) || []).length;
    const alquilerCount = (lowerHtml.match(/\balquiler\b/g) || []).length;
    // Allow "arriendo" in comparison contexts (e.g., "vs", "diferencia", "a diferencia del")
    // but flag if appears >3 times (likely used as main term)
    results.push({
      capa: 'C10', check: `Término "arriendo" en MittaGO (${arriendoCount} ocurrencias)`,
      pass: arriendoCount <= 3, severity: 'WARNING',
      detail: arriendoCount > 3 ? 'Posible uso de "arriendo" como nombre del servicio MittaGO' : undefined,
    });
    results.push({
      capa: 'C10', check: `Término "alquiler" en MittaGO (${alquilerCount})`,
      pass: alquilerCount === 0, severity: 'ERROR',
    });
  }

  // ── C11: E-E-A-T markers ──
  let eeatCount = 0;
  EEAT_MARKERS.forEach(regex => {
    if (regex.test(html)) eeatCount++;
  });
  results.push({
    capa: 'C11', check: `E-E-A-T markers (${eeatCount}, mín: 3)`,
    pass: eeatCount >= 3, severity: 'WARNING',
  });

  // ── C12: Enlaces internos ──
  const internalLinks = html.match(/href="\/[^"]*"/gi) || [];
  const mittaLinks = html.match(/href="https?:\/\/(www\.)?(mitta|mittago)\.cl\/[^"]*"/gi) || [];
  const totalInternalLinks = internalLinks.length + mittaLinks.length;
  results.push({
    capa: 'C12', check: `Enlaces internos (${totalInternalLinks}, mín: 2)`,
    pass: totalInternalLinks >= 2, severity: 'ERROR',
  });

  // ── C13: <main> wrapper ──
  const hasMain = /<main[\s>]/i.test(html);
  results.push({
    capa: 'C13', check: '<main> wrapper',
    pass: hasMain, severity: 'WARNING',
  });

  // ── C13: aria-label en breadcrumbs ──
  const hasAriaLabel = /class="breadcrumb"[^>]*aria-label/i.test(html) ||
                       /aria-label[^>]*class="breadcrumb"/i.test(html);
  results.push({
    capa: 'C13', check: 'aria-label en breadcrumbs',
    pass: hasAriaLabel, severity: 'WARNING',
  });

  // ── C13: <article> wrapper ──
  const hasArticle = /<article[\s>]/i.test(html);
  results.push({
    capa: 'C13', check: '<article> wrapper',
    pass: hasArticle, severity: 'WARNING',
  });

  return { filename, results };
}

// ─── Main ────────────────────────────────────────────────────
const files = fs.readdirSync(DIR)
  .filter(f => f.endsWith('.html'))
  .sort();

if (files.length === 0) {
  console.error(`No se encontraron archivos .html en: ${DIR}`);
  process.exit(1);
}

console.log(`\n╔══════════════════════════════════════════════════════════════╗`);
console.log(`║  AUDITORÍA AUTOMATIZADA v3.0 — ${BRAND.toUpperCase().padEnd(8)} (${files.length} artículos)   ║`);
console.log(`╚══════════════════════════════════════════════════════════════╝\n`);

let totalPass = 0;
let totalWarn = 0;
let totalError = 0;
let articlesClean = 0;

files.forEach((file, idx) => {
  const filePath = path.join(DIR, file);
  const { filename, results } = auditFile(filePath);

  const errors = results.filter(r => !r.pass && r.severity === 'ERROR');
  const warnings = results.filter(r => !r.pass && r.severity === 'WARNING');
  const passes = results.filter(r => r.pass);

  totalPass += passes.length;
  totalWarn += warnings.length;
  totalError += errors.length;

  const status = errors.length === 0 && warnings.length === 0
    ? '✅ PASS'
    : errors.length === 0
      ? `⚠️  ${warnings.length} warnings`
      : `❌ ${errors.length} errores, ${warnings.length} warnings`;

  if (errors.length === 0 && warnings.length === 0) articlesClean++;

  console.log(`[${String(idx + 1).padStart(2, '0')}] ${filename}`);
  console.log(`     ${status}`);

  if (errors.length > 0) {
    errors.forEach(e => {
      console.log(`     ❌ ${e.capa}: ${e.check}`);
      if (e.detail) console.log(`        → ${e.detail}`);
    });
  }
  if (warnings.length > 0) {
    warnings.forEach(w => {
      console.log(`     ⚠️  ${w.capa}: ${w.check}`);
      if (w.detail) console.log(`        → ${w.detail}`);
    });
  }
  console.log('');
});

// ── Summary ──
console.log(`╔══════════════════════════════════════════════════════════════╗`);
console.log(`║  RESUMEN: ${String(totalPass).padStart(3)} ✅ | ${String(totalWarn).padStart(3)} ⚠️  | ${String(totalError).padStart(3)} ❌                        ║`);
console.log(`║  Artículos sin errores: ${articlesClean}/${files.length}                                ║`);
console.log(`╚══════════════════════════════════════════════════════════════╝`);

process.exit(totalError > 0 ? 1 : 0);
