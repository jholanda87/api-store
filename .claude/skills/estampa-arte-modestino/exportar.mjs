// Exporta um SVG em PNG (300 dpi no tamanho real) ou PDF (tamanho real, vetor).
// Uso: node exportar.mjs arte.svg saida.png [--dpi 300]
//      node exportar.mjs arte.svg saida.pdf
// Precisa do Playwright com Chromium (no Claude Code na nuvem já vem instalado).
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const [entrada, saida, ...resto] = process.argv.slice(2);
if (!entrada || !saida) {
  console.error("uso: node exportar.mjs arte.svg saida.png|saida.pdf [--dpi 300]");
  process.exit(2);
}
const dpiArg = resto.indexOf("--dpi");
const dpi = dpiArg >= 0 ? Number(resto[dpiArg + 1]) : 300;

const svg = readFileSync(entrada, "utf8");
const unidade = { mm: 1, cm: 10, in: 25.4, pt: 25.4 / 72, px: 25.4 / 96, "": 25.4 / 96 };
const medida = (nome) => {
  const m = svg.match(new RegExp(`<svg[^>]*\\s${nome}="([\\d.]+)\\s*(mm|cm|in|pt|px|)"`));
  return m ? Number(m[1]) * unidade[m[2]] : null;
};
const larg = medida("width");
const alt = medida("height");
if (!larg || !alt) {
  console.error("O SVG precisa de width/height com unidade (ex.: 90mm).");
  process.exit(2);
}

const browser = await chromium.launch();
const page = await browser.newPage();
const html = `<!doctype html><html><head><style>
  @page { size: ${larg}mm ${alt}mm; margin: 0 }
  html, body { margin: 0; padding: 0; background: transparent }
  svg { display: block; width: ${larg}mm; height: ${alt}mm }
</style></head><body>${svg.replace(/<\?xml[^>]*>/, "")}</body></html>`;
await page.setContent(html, { waitUntil: "load" });

if (saida.endsWith(".pdf")) {
  await page.pdf({ path: saida, width: `${larg}mm`, height: `${alt}mm`, printBackground: true });
} else {
  // 96 px por polegada na tela; escala para o dpi pedido.
  const escala = dpi / 96;
  const w = Math.ceil((larg / 25.4) * 96);
  const h = Math.ceil((alt / 25.4) * 96);
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: escala });
  const p2 = await ctx.newPage();
  await p2.setContent(html, { waitUntil: "load" });
  await p2.screenshot({ path: saida, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
}
await browser.close();
console.log(saida);
