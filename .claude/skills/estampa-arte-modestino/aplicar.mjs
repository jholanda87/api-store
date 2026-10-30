// Aplica uma estampa (SVG) numa foto da camiseta, frente ou costas, em escala real.
//
// Uso:
//   node aplicar.mjs foto.png arte.svg saida.png --gola X,Y --axilas PX
//        [--posicao peito|frente|costas|nuca] [--lado-peito direita|esquerda]
//        [--giro 0] [--dobras 0.8]
//   node aplicar.mjs foto.png arte.svg saida.png --caixa X,Y,LARGURA   (posição manual)
//
// --gola: ponto central de baixo da gola na foto (pixels). Na foto de costas, a gola de trás.
// --axilas: largura da camiseta de axila a axila na foto (pixels). Com ela a escala sai real
//   (tamanho M = 54 cm). --lado-peito: o peito esquerdo de quem veste fica à direita na foto
//   de frente (padrão). --dobras: quanto as sombras do tecido passam por cima da tinta.
// fotos.json (opcional, ao lado das fotos): {"preta-costas.png": {"gola": [512, 210], "axilas": 640,
//   "lado": "costas", "cor": "preto"}}. Com ele, basta a foto, a arte e a --posicao.
// Serve para aprovar a estampa e para mostrar a ideia; não substitui a foto da peça real.
import { existsSync, readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { basename, dirname, extname, join } from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const args = process.argv.slice(2);
const [foto, arte, saida] = args;
const opt = (nome, padrao) => {
  const i = args.indexOf(`--${nome}`);
  return i >= 0 ? args[i + 1] : padrao;
};
if (!foto || !arte || !saida) {
  console.error("uso: node aplicar.mjs foto.png arte.svg saida.png --gola X,Y --axilas PX [--posicao frente]");
  process.exit(2);
}

const MEIO_PEITO_CM = 54; // tamanho M, axila a axila
// Topo da arte em cm abaixo da gola, e deslocamento lateral em cm (peito).
// Peito medido na primeira peça real (figura de 10 cm na off-white, 30/10/2026).
const LUGAR = { peito: [10, 7], frente: [8, 0], costas: [7, 0], nuca: [2.5, 0] };

const svg = readFileSync(arte, "utf8");
const un = { mm: 1, cm: 10, in: 25.4, pt: 25.4 / 72, px: 25.4 / 96, "": 25.4 / 96 };
const med = (n) => {
  const m = svg.match(new RegExp(`<svg[^>]*\\s${n}="([\\d.]+)\\s*(mm|cm|in|pt|px|)"`));
  return m ? (Number(m[1]) * un[m[2]]) / 10 : null; // cm
};
const artW = med("width");
const artH = med("height");
if (!artW || !artH) {
  console.error("A arte precisa de width/height em mm (rode estampa.py).");
  process.exit(2);
}

let x, y, w;
if (opt("caixa")) {
  [x, y, w] = opt("caixa").split(",").map(Number);
} else {
  // Sem --gola/--axilas, lê as medidas da foto em fotos.json, na mesma pasta da foto.
  let gola = opt("gola") && opt("gola").split(",").map(Number);
  let axilas = opt("axilas") && Number(opt("axilas"));
  const registro = join(dirname(foto), "fotos.json");
  if ((!gola || !axilas) && existsSync(registro)) {
    const m = JSON.parse(readFileSync(registro, "utf8"))[basename(foto)];
    if (m) {
      gola = gola || m.gola;
      axilas = axilas || m.axilas;
    }
  }
  if (!gola || !axilas) {
    console.error("Passe --gola X,Y e --axilas PX, registre a foto em fotos.json, ou use --caixa X,Y,LARGURA.");
    process.exit(2);
  }
  const [gx, gy] = gola;
  const pxcm = axilas / MEIO_PEITO_CM;
  const pos = opt("posicao", "frente");
  if (!LUGAR[pos]) {
    console.error(`posição desconhecida: ${pos}`);
    process.exit(2);
  }
  const [topo, lado] = LUGAR[pos];
  const sinal = opt("lado-peito", "direita") === "direita" ? 1 : -1;
  w = artW * pxcm;
  x = gx + sinal * lado * pxcm - w / 2;
  y = gy + topo * pxcm;
}
const h = (w * artH) / artW;
const giro = Number(opt("giro", 0));
const dobras = Number(opt("dobras", 0.8));

const mime = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp" }[
  extname(foto).toLowerCase()
];
const fotoUrl = `data:${mime};base64,${readFileSync(foto).toString("base64")}`;
const arteUrl = `data:image/svg+xml;base64,${Buffer.from(svg).toString("base64")}`;

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setContent("<!doctype html><html><body style='margin:0'><canvas id='c'></canvas></body></html>");
const png = await page.evaluate(
  async ({ fotoUrl, arteUrl, x, y, w, h, giro, dobras }) => {
    const carregar = (src) =>
      new Promise((ok, erro) => {
        const i = new Image();
        i.onload = () => ok(i);
        i.onerror = erro;
        i.src = src;
      });
    const f = await carregar(fotoUrl);
    const a = await carregar(arteUrl);
    const W = f.naturalWidth;
    const H = f.naturalHeight;
    const novo = () => {
      const c = document.createElement("canvas");
      c.width = W;
      c.height = H;
      return [c, c.getContext("2d", { willReadFrequently: true })];
    };
    const [cf, xf] = novo();
    xf.drawImage(f, 0, 0);
    const [ca, xa] = novo();
    xa.translate(x + w / 2, y);
    xa.rotate((giro * Math.PI) / 180);
    xa.drawImage(a, -w / 2, 0, w, h);
    const F = xf.getImageData(0, 0, W, H);
    const A = xa.getImageData(0, 0, W, H);
    // Luz média do tecido dentro da caixa da arte: referência das dobras.
    const lum = (d, i) => 0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2];
    let soma = 0;
    let n = 0;
    for (let i = 0; i < A.data.length; i += 4)
      if (A.data[i + 3] > 0) {
        soma += lum(F.data, i);
        n++;
      }
    const media = Math.max(n ? soma / n : 128, 8);
    for (let i = 0; i < A.data.length; i += 4) {
      const al = A.data[i + 3] / 255;
      if (!al) continue;
      const luz = Math.pow(Math.min(Math.max(lum(F.data, i) / media, 0.3), 1.6), dobras);
      const t = al * 0.96; // tinta nunca 100% chapada no tecido
      for (let k = 0; k < 3; k++)
        F.data[i + k] = Math.round((1 - t) * F.data[i + k] + t * Math.min(255, A.data[i + k] * luz));
    }
    xf.putImageData(F, 0, 0);
    return cf.toDataURL("image/png");
  },
  { fotoUrl, arteUrl, x, y, w, h, giro, dobras }
);
const { writeFileSync } = await import("node:fs");
writeFileSync(saida, Buffer.from(png.split(",")[1], "base64"));
await browser.close();
console.log(`${saida}  (arte ${artW.toFixed(1)} × ${artH.toFixed(1)} cm, ${Math.round(w)} px na foto)`);
