#!/usr/bin/env python3
"""Vetoriza um desenho a traço (foto ou PNG do papel) em SVG de uma tinta.

Uso:
  python3 vetorizar.py desenho.png saida.svg --altura-mm 70 [--corte x0,y0,x1,y1]
                       [--limiar 140] [--sujeira 12] [--cor "#22201D"]

Serve para o Cavalheiro e para desenhos à mão do Jorge: o traço original vira vetor,
sem redesenhar. --corte recorta em pixels da imagem original; --limiar separa traço
(escuro) de papel; --sujeira apaga manchas menores que isso (em pixels). Precisa de
Pillow e potracer (pip install pillow potracer). Sem eles: Adobe image_vectorize.
Confira sempre o resultado ao lado do original antes de usar.
"""

import argparse
import sys


def vetorizar(caminho, altura_mm, corte=None, limiar=140, sujeira=12, cor="#22201D"):
    try:
        import potrace
        from PIL import Image, ImageOps
    except ImportError:
        raise SystemExit("Falta biblioteca: pip install pillow potracer")
    img = ImageOps.grayscale(Image.open(caminho))
    if corte:
        img = img.crop(corte)
    # o Bitmap do potracer inverte: True é papel, False é traço
    dados = [[px >= limiar for px in linha] for linha in _linhas(img)]
    bm = potrace.Bitmap(dados)
    curvas = bm.trace(turdsize=sujeira, alphamax=1.0, opticurve=True, opttolerance=0.2)
    if not len(curvas):
        raise SystemExit("Nada encontrado: ajuste --limiar ou --corte.")
    xs, ys, d = [], [], []
    for c in curvas:
        sx, sy = c.start_point.x, c.start_point.y
        partes = ["M%.1f %.1f" % (sx, sy)]
        for seg in c.segments:
            if seg.is_corner:
                partes.append("L%.1f %.1fL%.1f %.1f" % (seg.c.x, seg.c.y, seg.end_point.x,
                                                       seg.end_point.y))
                pts = [seg.c, seg.end_point]
            else:
                partes.append("C%.1f %.1f %.1f %.1f %.1f %.1f" % (
                    seg.c1.x, seg.c1.y, seg.c2.x, seg.c2.y, seg.end_point.x, seg.end_point.y))
                pts = [seg.c1, seg.c2, seg.end_point]
            xs += [p.x for p in pts]
            ys += [p.y for p in pts]
        d.append("".join(partes) + "Z")
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    w, h = x1 - x0, y1 - y0
    largura_mm = altura_mm * w / h
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%.2fmm" height="%.2fmm" '
            'viewBox="%.1f %.1f %.1f %.1f">\n  <path fill="%s" fill-rule="evenodd" d="%s"/>\n'
            '</svg>\n' % (largura_mm, altura_mm, x0, y0, w, h, cor, "".join(d)))


def _linhas(img):
    w, h = img.size
    px = img.tobytes()  # modo L: um byte por pixel
    return [px[i * w:(i + 1) * w] for i in range(h)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("imagem")
    ap.add_argument("saida")
    ap.add_argument("--altura-mm", type=float, required=True)
    ap.add_argument("--corte")
    ap.add_argument("--limiar", type=int, default=140)
    ap.add_argument("--sujeira", type=int, default=12)
    ap.add_argument("--cor", default="#22201D")
    a = ap.parse_args(argv)
    corte = tuple(int(v) for v in a.corte.split(",")) if a.corte else None
    svg = vetorizar(a.imagem, a.altura_mm, corte, a.limiar, a.sujeira, a.cor)
    with open(a.saida, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(a.saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
