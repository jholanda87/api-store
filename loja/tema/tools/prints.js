// Prints da prévia local em 390 e 1440 px + checagens (rolagem lateral, erros no console).
// node loja/tema/tools/prints.js  (depois de python3 loja/tema/tools/previa.py)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const dir = path.resolve(__dirname, '../previa');
const out = path.resolve(__dirname, '../../clone-screens');
fs.mkdirSync(out, { recursive: true });
const paginas = fs.readdirSync(dir).filter((f) => f.endsWith('.html')).map((f) => f.slice(0, -5));
(async () => {
  const browser = await chromium.launch();
  const relatorio = [];
  for (const largura of [390, 1440]) {
    const ctx = await browser.newContext({ viewport: { width: largura, height: largura === 390 ? 844 : 900 }, deviceScaleFactor: 1 });
    for (const p of paginas) {
      const page = await ctx.newPage();
      const erros = [];
      page.on('console', (m) => { if (m.type() === 'error') erros.push(m.text()); });
      page.on('pageerror', (e) => erros.push(String(e)));
      await page.goto('http://localhost:8765/' + p + '.html');
      await page.waitForTimeout(250);
      const lateral = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      await page.screenshot({ path: path.join(out, `${p}-${largura}.png`), fullPage: true });
      if (['inicio', 'produto'].includes(p)) await page.screenshot({ path: path.join(out, `${p}-${largura}-dobra.png`) });
      relatorio.push({ pagina: p, largura, rolagem_lateral_px: lateral, erros });
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
  console.log(JSON.stringify(relatorio, null, 1));
})();
