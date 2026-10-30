#!/usr/bin/env python3
"""Transforma uma foto ou desenho em pontilhismo ou hachura à mão, em SVG de uma tinta.

Uso:
  python3 textura.py foto.jpg saida.svg --largura-mm 90 [--modo pontilhismo|hachura]
                     [--ponto-mm 0.8] [--traco-mm 0.4] [--gama 1.4] [--corte x0,y0,x1,y1]
                     [--inverter] [--cor "#22201D"] [--semente 7]

Pontilhismo: pontos do mesmo tamanho, mais juntos onde a imagem é escura (como à mão,
com caneta nanquim). Hachura: traços paralelos em até 3 direções, cruzando nas sombras,
com o leve tremor da mão. --inverter para tinta clara em camiseta escura (os pontos vão
nas luzes). A foto tem que ser do Jorge (ou um desenho dele): a textura é da gente, o
assunto também. Precisa de Pillow (pip install pillow).
"""

import argparse
import math
import random
import sys


def carregar(caminho, largura_mm, passo_mm, corte, gama, inverter, desfoque=0.0):
    try:
        from PIL import Image, ImageFilter, ImageOps
    except ImportError:
        raise SystemExit("Falta o Pillow: pip install pillow")
    img = Image.open(caminho)
    if img.mode in ("RGBA", "LA", "P"):  # transparente vira papel: sem ponto
        img = img.convert("RGBA")
        papel = Image.new("RGBA", img.size, (0, 0, 0, 255) if inverter else (255, 255, 255, 255))
        img = Image.alpha_composite(papel, img)
    img = ImageOps.grayscale(img)
    if corte:
        img = img.crop(corte)
    if desfoque:
        img = img.filter(ImageFilter.GaussianBlur(desfoque))
    img = ImageOps.autocontrast(img, cutoff=1)
    w = max(1, int(round(largura_mm / passo_mm)))
    h = max(1, int(round(img.height * w / img.width)))
    img = img.resize((w, h))
    px = img.tobytes()
    escuro = []
    for y in range(h):
        linha = []
        for x in range(w):
            v = px[y * w + x] / 255.0
            d = v if inverter else 1.0 - v
            linha.append(d ** gama)
        escuro.append(linha)
    return escuro, w, h


def pontilhismo(escuro, w, h, passo, ponto, semente):
    """Dardos com distância mínima que cresce nas luzes (amostragem de Poisson variável)."""
    rnd = random.Random(semente)
    cel = ponto * 1.2
    grade = {}
    pontos = []
    largura, altura = w * passo, h * passo
    tentativas = int(largura * altura / (ponto * ponto) * 3)
    for _ in range(tentativas):
        x, y = rnd.uniform(0, largura), rnd.uniform(0, altura)
        d = escuro[min(h - 1, int(y / passo))][min(w - 1, int(x / passo))]
        if d < 0.04 or rnd.random() > d:
            continue
        r = ponto * (1.15 + 3.2 * (1 - d))  # distância mínima entre centros
        gx, gy = int(x / cel), int(y / cel)
        alcance = int(math.ceil(r / cel))
        livre = True
        for i in range(gx - alcance, gx + alcance + 1):
            for j in range(gy - alcance, gy + alcance + 1):
                for (px, py) in grade.get((i, j), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < r * r:
                        livre = False
                        break
                if not livre:
                    break
            if not livre:
                break
        if livre:
            grade.setdefault((gx, gy), []).append((x, y))
            pontos.append((x, y))
    return pontos, largura, altura


def hachura(escuro, w, h, passo, traco, semente):
    """Até 3 camadas de traços (45°, -45°, 0°): cada camada entra num nível de sombra."""
    rnd = random.Random(semente)
    largura, altura = w * passo, h * passo
    espaco = traco * 3.2
    camadas = [(math.radians(45), 0.18), (math.radians(-45), 0.45), (0.0, 0.72)]
    linhas = []
    diag = math.hypot(largura, altura)
    for ang, limiar in camadas:
        dx, dy = math.cos(ang), math.sin(ang)
        nx, ny = -dy, dx
        k = -diag / 2
        while k < diag / 2:
            k += espaco * rnd.uniform(0.85, 1.15)
            cx, cy = largura / 2 + nx * k, altura / 2 + ny * k
            seg = []
            t = -diag / 2
            while t < diag / 2:
                x, y = cx + dx * t, cy + dy * t
                dentro = 0 <= x < largura and 0 <= y < altura
                d = escuro[int(y / passo)][int(x / passo)] if dentro else 0
                if dentro and d > limiar:
                    tremor = rnd.uniform(-0.12, 0.12) * traco * 2
                    seg.append((x + nx * tremor, y + ny * tremor))
                elif len(seg) > 1:
                    linhas.append(seg)
                    seg = []
                else:
                    seg = []
                t += traco * 2
            if len(seg) > 1:
                linhas.append(seg)
    return [l for l in linhas if len(l) > 2], largura, altura


def svg(largura, altura, corpo, titulo):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%.2fmm" height="%.2fmm" '
            'viewBox="0 0 %.2f %.2f">\n  <title>%s</title>\n%s\n</svg>\n'
            % (largura, altura, largura, altura, titulo, corpo))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("imagem")
    ap.add_argument("saida")
    ap.add_argument("--largura-mm", type=float, required=True)
    ap.add_argument("--modo", choices=("pontilhismo", "hachura"), default="pontilhismo")
    ap.add_argument("--ponto-mm", type=float, default=0.8)
    ap.add_argument("--traco-mm", type=float, default=0.4)
    ap.add_argument("--gama", type=float, default=1.4)
    ap.add_argument("--desfoque", type=float, default=0.0, help="px; amacia desenho de traço fino")
    ap.add_argument("--corte")
    ap.add_argument("--inverter", action="store_true")
    ap.add_argument("--cor", default="#22201D")
    ap.add_argument("--semente", type=int, default=7)
    a = ap.parse_args(argv)
    corte = tuple(int(v) for v in a.corte.split(",")) if a.corte else None
    passo = 0.25
    escuro, w, h = carregar(a.imagem, a.largura_mm, passo, corte, a.gama, a.inverter, a.desfoque)
    if a.modo == "pontilhismo":
        pts, lw, lh = pontilhismo(escuro, w, h, passo, a.ponto_mm, a.semente)
        r = a.ponto_mm / 2
        # um path só com todos os pontos (arquivo leve); cada ponto é um círculo de 4 arcos
        d = "".join("M%.2f %.2fa%.3f %.3f 0 1 0 %.3f 0a%.3f %.3f 0 1 0 %.3f 0Z"
                    % (x - r, y, r, r, 2 * r, r, r, -2 * r) for x, y in pts)
        corpo = '  <path fill="%s" d="%s"/>' % (a.cor, d)
        info = "%d pontos de %.1f mm" % (len(pts), a.ponto_mm)
    else:
        linhas, lw, lh = hachura(escuro, w, h, passo, a.traco_mm, a.semente)
        d = "".join("M" + "L".join("%.2f %.2f" % p for p in l) for l in linhas)
        corpo = ('  <path fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round" '
                 'stroke-linejoin="round" d="%s"/>' % (a.cor, a.traco_mm, d))
        info = "%d traços de %.2f mm" % (len(linhas), a.traco_mm)
    with open(a.saida, "w", encoding="utf-8") as fh:
        fh.write(svg(lw, lh, corpo, "%s de %s" % (a.modo, a.imagem.split("/")[-1])))
    print("%s  (%s, %.1f × %.1f cm)" % (a.saida, info, lw / 10, lh / 10))
    return 0


if __name__ == "__main__":
    sys.exit(main())
