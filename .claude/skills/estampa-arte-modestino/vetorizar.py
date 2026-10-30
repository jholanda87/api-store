#!/usr/bin/env python3
"""Vetoriza um desenho a traço (foto ou PNG do papel) em SVG de uma tinta.

Uso:
  python3 vetorizar.py desenho.png saida.svg --altura-mm 70 [--corte x0,y0,x1,y1]
                       [--limiar 140] [--sujeira 12] [--cor "#22201D"]
                       [--ampliar 1] [--engrossar-mm 0] [--garantir-mm 0] [--traco-min-mm 0.8]

Serve para o Cavalheiro e para desenhos à mão do Jorge: o traço original vira vetor,
sem redesenhar. --corte recorta em pixels da imagem original; --limiar separa traço
(escuro) de papel; --sujeira apaga manchas menores que isso (em pixels). Precisa de
Pillow e potracer (pip install pillow potracer). Sem eles: Adobe image_vectorize.
--ampliar N aumenta e suaviza imagens pequenas antes de traçar. --garantir-mm (o melhor para
serigrafia) faz todo traço e ponto ter pelo menos essa espessura, crescendo só o que é fino, pela
linha central, sem empastar o resto (precisa de numpy e scikit-image). --engrossar-mm engrossa tudo
por igual e --traco-min-mm mede quanto do desenho é mais fino que isso
no tamanho final. Confira sempre o resultado ao lado do original antes de usar.
"""

import argparse
import sys


def garantir(img, mm_px, minimo_mm):
    """Cada traço passa a ter no mínimo minimo_mm: desenha um disco desse diâmetro ao longo
    do esqueleto (linha central) e junta com o desenho. O que já é grosso não muda."""
    import numpy as np
    from PIL import Image
    from scipy.ndimage import binary_dilation
    from skimage.morphology import disk, skeletonize
    tinta = np.array(img) == 0
    r = max(1, int(round(minimo_mm / mm_px / 2)))
    novo = tinta | binary_dilation(skeletonize(tinta), structure=disk(r))
    return Image.fromarray(np.where(novo, 0, 255).astype("uint8"))


def preparar(img, altura_mm, limiar, ampliar=1, engrossar_mm=0.0, traco_min_mm=0.0, garantir_mm=0.0):
    """Amplia, binariza e engrossa. Devolve a imagem em L (0 = traço) e a % fina demais."""
    from PIL import Image, ImageFilter
    if ampliar > 1:
        img = img.resize((img.width * ampliar, img.height * ampliar), Image.LANCZOS)
        img = img.filter(ImageFilter.GaussianBlur(ampliar / 3))
    img = img.point(lambda v: 0 if v < limiar else 255)
    mm_px = altura_mm / img.height
    if engrossar_mm > 0:  # MinFilter espalha o preto: o traço cresce dos dois lados
        k = max(3, int(round(engrossar_mm / mm_px)) | 1)
        img = img.filter(ImageFilter.MinFilter(k))
    if garantir_mm > 0:
        img = garantir(img, mm_px, garantir_mm)
    fino = 0.0
    if traco_min_mm > 0:  # abertura com um disco do diâmetro mínimo: some o que é mais fino
        try:
            import numpy as np
            from scipy.ndimage import binary_opening
            from skimage.morphology import disk
            tinta = np.array(img) == 0
            r = max(1, int(round(traco_min_mm / mm_px / 2)))
            aberto = binary_opening(tinta, structure=disk(r))
            fino = 100.0 * (tinta & ~aberto).sum() / max(1, tinta.sum())
        except ImportError:  # sem numpy: quadrado, mais rigoroso nas diagonais
            k = max(3, int(round(traco_min_mm / mm_px)) | 1)
            aberto = img.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MinFilter(k))
            tinta = img.histogram()[0]
            perdido = sum(1 for a, b in zip(img.tobytes(), aberto.tobytes()) if a == 0 and b != 0)
            fino = 100.0 * perdido / max(1, tinta)
    return img, fino


def vetorizar(caminho, altura_mm, corte=None, limiar=140, sujeira=12, cor="#22201D",
              ampliar=1, engrossar_mm=0.0, traco_min_mm=0.0, garantir_mm=0.0):
    try:
        import potrace
        from PIL import Image, ImageOps
    except ImportError:
        raise SystemExit("Falta biblioteca: pip install pillow potracer")
    img = ImageOps.grayscale(Image.open(caminho))
    if corte:
        img = img.crop(corte)
    img, fino = preparar(img, altura_mm, limiar, ampliar, engrossar_mm, traco_min_mm, garantir_mm)
    vetorizar.fino = fino
    d, (x0, y0, x1, y1) = tracar(img, limiar, sujeira)
    if not d:
        raise SystemExit("Nada encontrado: ajuste --limiar ou --corte.")
    w, h = x1 - x0, y1 - y0
    largura_mm = altura_mm * w / h
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%.2fmm" height="%.2fmm" '
            'viewBox="%.1f %.1f %.1f %.1f">\n  <path fill="%s" fill-rule="evenodd" d="%s"/>\n'
            '</svg>\n' % (largura_mm, altura_mm, x0, y0, w, h, cor, "".join(d)))


def tracar(img, limiar=128, sujeira=12):
    """Traça a imagem L (escuro = tinta) com o potrace. Devolve ([d, ...], caixa) em pixels."""
    import potrace
    # o Bitmap do potracer inverte: True é papel, False é traço
    dados = [[px >= limiar for px in linha] for linha in _linhas(img)]
    curvas = potrace.Bitmap(dados).trace(turdsize=sujeira, alphamax=1.0, opticurve=True,
                                         opttolerance=0.2)
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
    if not d:
        return [], (0, 0, 0, 0)
    return d, (min(xs), min(ys), max(xs), max(ys))


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
    ap.add_argument("--ampliar", type=int, default=1)
    ap.add_argument("--engrossar-mm", type=float, default=0.0)
    ap.add_argument("--garantir-mm", type=float, default=0.0)
    ap.add_argument("--traco-min-mm", type=float, default=0.0)
    a = ap.parse_args(argv)
    corte = tuple(int(v) for v in a.corte.split(",")) if a.corte else None
    svg = vetorizar(a.imagem, a.altura_mm, corte, a.limiar, a.sujeira, a.cor, a.ampliar,
                    a.engrossar_mm, a.traco_min_mm, a.garantir_mm)
    with open(a.saida, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(a.saida)
    if a.traco_min_mm:
        print("%.1f%% do traço mais fino que %.1f mm" % (vetorizar.fino, a.traco_min_mm))
    return 0


if __name__ == "__main__":
    sys.exit(main())
