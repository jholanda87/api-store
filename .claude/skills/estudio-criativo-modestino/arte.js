// Gera artes da Modestino (carrossel 1080×1350, story/capa de Reel 1080×1920, overlays transparentes)
// a partir de um JSON, com os tokens, as fontes e o Cavalheiro da marca.
//
//   node .claude/skills/estudio-criativo-modestino/arte.js loja/estudio/lotes/<lote>/<peca>.json
//
// Saída: PNGs na pasta "saida" do JSON (padrão: ao lado do JSON, em <nome>/), um por lâmina,
// e uma folha de prévia <nome>-previa.png. Tipos de lâmina: capa-foto, foto, texto, fecho, overlay.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const RAIZ = path.resolve(__dirname, '../../..');
const DESIGN = path.join(RAIZ, 'loja/design');
const tokens = JSON.parse(fs.readFileSync(path.join(DESIGN, 'tokens.json'), 'utf8'));
const C = tokens.color;
const b64 = (p) => fs.readFileSync(p).toString('base64');
const fonte = (familia, arq, peso, estilo) =>
  `@font-face{font-family:'${familia}';src:url(data:font/woff2;base64,${b64(path.join(DESIGN, 'fonts', arq))}) format('woff2');font-weight:${peso};font-style:${estilo}}`;
const FONTES = [
  fonte('Instrument Serif', 'instrument-serif-latin-400-normal.woff2', 400, 'normal'),
  fonte('Instrument Serif', 'instrument-serif-latin-400-italic.woff2', 400, 'italic'),
  fonte('Instrument Sans', 'instrument-sans-latin-400-normal.woff2', 400, 'normal'),
  fonte('Instrument Sans', 'instrument-sans-latin-600-normal.woff2', 600, 'normal'),
  fonte('Geist Mono', 'geist-mono-latin-400-normal.woff2', 400, 'normal'),
].join('');
const LOGO = {
  carvao: `data:image/png;base64,${b64(path.join(DESIGN, 'logo/cavalheiro-busto-carvao.png'))}`,
  linho: `data:image/png;base64,${b64(path.join(DESIGN, 'logo/cavalheiro-busto-linho.png'))}`,
};
const FUNDOS = {
  linho: { bg: C.bg, fg: C.text, sub: C['text-muted'], logo: 'carvao' },
  areia: { bg: C.surface, fg: C.text, sub: C['text-muted'], logo: 'carvao' },
  carvao: { bg: C['surface-dark'], fg: C['text-on-dark'], sub: C['text-muted-on-dark'], logo: 'linho' },
  mapple: { bg: C.accent, fg: C['on-accent'], sub: C['text-muted-on-dark'], logo: 'linho' },
};
const FORMATOS = { feed: [1080, 1350], story: [1080, 1920] };
const esc = (s = '') => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// *palavra* vira destaque com fundo areia (marca da capa do método de carrossel).
const marca = (s = '') => esc(s).replace(/\*(.+?)\*/g, '<mark>$1</mark>').replace(/\n/g, '<br>');

function css(w, h, safe) {
  return `${FONTES}
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{width:${w}px;height:${h}px;overflow:hidden;background:transparent}
  .l{position:relative;width:${w}px;height:${h}px;overflow:hidden;font-family:'Instrument Sans',sans-serif;-webkit-font-smoothing:antialiased}
  .pad{position:absolute;inset:${safe.top}px 88px ${safe.bottom}px 88px;display:flex;flex-direction:column}
  h1,h2{font-family:'Instrument Serif',serif;font-weight:400;letter-spacing:-0.01em;line-height:1.02}
  h1{font-size:118px}h2{font-size:92px}
  h1 em,h2 em{font-style:italic}
  mark{background:${C.highlight};color:${C.text};padding:0 .12em;border-radius:6px}
  p{font-size:40px;line-height:1.35;max-width:24ch}
  .mono{font-family:'Geist Mono',monospace;font-size:30px;letter-spacing:.02em}
  .nome{font-weight:600;font-size:30px;letter-spacing:.32em}
  .foto{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .grad{position:absolute;inset:0;background:${tokens.overlay ? tokens.overlay.hero : 'none'}}
  .marca{display:flex;align-items:center;gap:22px}
  .marca img{height:84px}
  .num{position:absolute;right:88px;top:${safe.top}px;font-family:'Geist Mono',monospace;font-size:28px;opacity:.75}
  .caixa{display:inline-block;background:${C['surface-dark']};color:${C['text-on-dark']};font-weight:600;font-size:56px;line-height:1.2;padding:22px 34px;border-radius:14px;max-width:880px}
  `;
}

// Foto da lâmina; se o arquivo ainda não existe (modelo sem foto), desenha um espaço reservado legível.
function fotoTag(l) {
  const p = l.foto ? path.resolve(RAIZ, l.foto) : '';
  if (p && fs.existsSync(p)) {
    const tipo = p.toLowerCase().endsWith('.png') ? 'png' : 'jpeg';
    return `<img class="foto" src="data:image/${tipo};base64,${b64(p)}" style="object-position:${l.posicao || 'center 30%'}">`;
  }
  return `<div class="foto" style="background:${C.border};display:grid;place-items:center"><span class="mono" style="color:${C.text}">[FOTO: ${esc(l.foto || 'a definir')}]</span></div>`;
}

function lamina(l, i, total, fmt) {
  const [w, h] = FORMATOS[fmt];
  const safe = fmt === 'story' ? { top: 250, bottom: 380 } : { top: 96, bottom: 96 };
  const f = FUNDOS[l.fundo || 'linho'];
  const num = l.numero === false || total < 2 ? '' : `<div class="num" style="color:${l.tipo.includes('foto') ? C['text-on-dark'] : f.fg}">${String(i + 1).padStart(2, '0')}/${String(total).padStart(2, '0')}</div>`;
  let corpo = '';
  if (l.tipo === 'capa-foto' || l.tipo === 'foto') {
    corpo = `${fotoTag(l)}
      <div class="grad"></div>
      <div class="pad" style="justify-content:flex-end;color:${C['text-on-dark']}">
        ${l.tipo === 'capa-foto' ? `<h1>${marca(l.titulo)}</h1>` : `<h2>${marca(l.titulo)}</h2>`}
        ${l.texto ? `<p style="margin-top:28px;color:${C['text-on-dark']}">${marca(l.texto)}</p>` : ''}
        ${l.rodape ? `<div class="mono" style="margin-top:36px">${esc(l.rodape)}</div>` : ''}
      </div>${num}`;
  } else if (l.tipo === 'texto') {
    corpo = `<div class="pad" style="justify-content:center;color:${f.fg}">
        <h2>${marca(l.titulo)}</h2>
        ${l.texto ? `<p style="margin-top:36px;color:${f.sub}">${marca(l.texto)}</p>` : ''}
        ${l.rodape ? `<div class="mono" style="margin-top:44px;color:${f.sub}">${esc(l.rodape)}</div>` : ''}
      </div>${num}`;
  } else if (l.tipo === 'fecho') {
    corpo = `<div class="pad" style="justify-content:center;align-items:center;text-align:center;color:${f.fg}">
        <img src="${LOGO[f.logo]}" style="height:150px;margin-bottom:28px" alt="">
        <div class="nome" style="margin-bottom:52px">MODESTINO</div>
        <h2 style="font-size:84px">${marca(l.titulo)}</h2>
        ${l.texto ? `<p style="margin:32px auto 0;color:${f.sub}">${marca(l.texto)}</p>` : ''}
        ${l.rodape ? `<div class="mono" style="margin-top:44px;color:${f.sub}">${esc(l.rodape)}</div>` : ''}
      </div>`;
  } else if (l.tipo === 'overlay') {
    // texto de vídeo: fundo transparente, caixa carvão no terço inferior (ou topo, para pergunta)
    const top = l.posicao === 'topo' ? safe.top : null;
    corpo = `<div style="position:absolute;left:88px;right:88px;${top !== null ? `top:${top}px` : `bottom:${safe.bottom + 60}px`};text-align:center">
        <span class="caixa">${marca(l.titulo)}</span></div>`;
  }
  const bg = l.tipo === 'overlay' ? 'transparent' : f.bg;
  return { w, h, html: `<!doctype html><html><head><meta charset="utf-8"><style>${css(w, h, safe)}</style></head><body><div class="l" style="background:${bg}">${corpo}</div></body></html>` };
}

(async () => {
  const arq = process.argv[2];
  if (!arq) { console.error('uso: node arte.js <peca.json>'); process.exit(1); }
  const spec = JSON.parse(fs.readFileSync(arq, 'utf8'));
  const fmt = spec.formato || 'feed';
  const saida = path.resolve(path.dirname(arq), spec.saida || spec.nome);
  fs.mkdirSync(saida, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: FORMATOS[fmt][0], height: FORMATOS[fmt][1] }, deviceScaleFactor: 1 });
  const arquivos = [];
  for (const [i, l] of spec.laminas.entries()) {
    const { html } = lamina(l, i, spec.laminas.length, fmt);
    await page.setContent(html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const nomeArq = path.join(saida, `modestino-${spec.nome}-${String(i + 1).padStart(2, '0')}.png`);
    await page.screenshot({ path: nomeArq, omitBackground: l.tipo === 'overlay' });
    arquivos.push(nomeArq);
  }
  // folha de prévia (lâminas lado a lado, reduzidas)
  const thumbs = arquivos.map((a) => `<img src="data:image/png;base64,${b64(a)}" style="width:270px;margin:6px;background:#888">`).join('');
  await page.setViewportSize({ width: Math.min(arquivos.length, 6) * 282 + 12, height: 200 });
  await page.setContent(`<body style="margin:0;background:#3a3836;display:flex;flex-wrap:wrap;align-items:flex-start;padding:6px">${thumbs}</body>`);
  await page.screenshot({ path: path.join(saida, `${spec.nome}-previa.png`), fullPage: true });
  await browser.close();
  console.log(`${arquivos.length} arte(s) em ${path.relative(RAIZ, saida)}`);
})();
