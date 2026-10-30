#!/usr/bin/env python3
"""Separa uma ilustração colorida em até 3 tintas exatas e vetoriza uma camada por tinta.

Uso:
  python3 cores.py arte.png saida.svg --tecido preto|mapple|off-white
                   [--altura-max-mm 350] [--largura-max-mm 320] [--garantir-mm 0.6]

Cada pixel vai para a cor mais próxima (no espaço Lab) entre o tecido e as 3 tintas da paleta
daquele tecido. O que fica na cor do tecido não leva tinta (vazado). Manchas menores que o
detalhe mínimo somem; traço fino de cada tinta cresce até --garantir-mm (serigrafia sem falha).
O SVG sai com um <g> por tinta, na ordem de impressão (preenchimentos antes, traço por cima),
pronto para separar.py e estampa.py. Precisa de numpy, scipy, scikit-image, Pillow e potracer.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vetorizar  # noqa: E402

# Paletas por tecido (30/10/2026): a primeira tinta é o traço; as outras duas, preenchimento.
# Contraste de cada tinta com o tecido: todas 4:1 ou mais.
PALETAS = {
    "preto": {"tecido": "#1E1D1C", "tintas": [("linho", "#ECE7DE"), ("ocre", "#C9A25E"),
                                               ("salvia", "#8E9B7A")]},
    "mapple": {"tecido": "#5B3F30", "tintas": [("linho", "#ECE7DE"), ("areia-dourada", "#D8B878"),
                                                ("azul-mar", "#9FB4B3")]},
    "off-white": {"tecido": "#ECE7DE", "tintas": [("carvao", "#22201D"), ("mapple", "#5B3F30"),
                                                   ("oliva", "#6B7350")]},
}


def rgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def separar_cores(caminho, tecido, garantir_mm=0.6, altura_max=350.0, largura_max=320.0):
    import numpy as np
    from PIL import Image
    from scipy.ndimage import median_filter
    from skimage.color import rgb2lab
    from skimage.morphology import remove_small_objects

    pal = PALETAS[tecido]
    cores = [pal["tecido"]] + [c for _, c in pal["tintas"]]
    img = Image.open(caminho).convert("RGB")
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
    lab = rgb2lab(np.asarray(img) / 255.0)
    ref = rgb2lab(np.array([[rgb(c) for c in cores]]) / 255.0)[0]
    dist = ((lab[:, :, None, :] - ref[None, None, :, :]) ** 2).sum(-1)
    rotulo = dist.argmin(-1).astype(np.uint8)

    tinta_total = rotulo > 0
    ys, xs = np.nonzero(tinta_total)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rotulo = rotulo[y0:y1, x0:x1]
    h, w = rotulo.shape
    escala = min(altura_max / h, largura_max / w)  # mm por pixel
    # o tecido que aparece dentro da arte (sombra em pontos, contorno vazado) também precisa do
    # mínimo: cresce até garantir_mm antes de limpar, senão a tinta fecha e a sombra some
    vazado = np.array(vetorizar.garantir(Image.fromarray(np.where(rotulo == 0, 0, 255).astype(
        "uint8")), escala, garantir_mm)) == 0
    rotulo[vazado] = 0
    rotulo = median_filter(rotulo, size=3)  # tira o chuvisco
    largura_mm, altura_mm = w * escala, h * escala
    minimo_px = max(4, int((garantir_mm / escala) ** 2))

    camadas, info = [], []
    for k, (nome, cor) in enumerate(pal["tintas"], start=1):
        try:  # scikit-image 0.26+ usa max_size; versões antigas, min_size
            mask = remove_small_objects(rotulo == k, max_size=minimo_px)
        except TypeError:
            mask = remove_small_objects(rotulo == k, min_size=minimo_px)
        area = 100.0 * mask.sum() / max(1, tinta_total[y0:y1, x0:x1].sum())
        if area < 0.5:  # tinta que quase não aparece não vale uma tela
            info.append((nome, cor, area, "descartada (menos de 0,5% da arte)"))
            continue
        L = Image.fromarray(np.where(mask, 0, 255).astype("uint8"))
        L = vetorizar.garantir(L, escala, garantir_mm)
        d, _ = vetorizar.tracar(L, 128, 4)
        camadas.append((k, nome, cor, d))
        info.append((nome, cor, area, "ok"))
    # imprime os preenchimentos antes e o traço (tinta 1) por cima
    camadas.sort(key=lambda c: 0 if c[0] > 1 else 1)
    grupos = "\n".join('  <g id="tinta-%s"><path fill="%s" fill-rule="evenodd" d="%s"/></g>'
                       % (nome, cor, "".join(d)) for _, nome, cor, d in camadas)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%.2fmm" height="%.2fmm" '
           'viewBox="0 0 %d %d">\n  <title>%d tintas · camiseta %s</title>\n%s\n</svg>\n'
           % (largura_mm, altura_mm, w, h, len(camadas), tecido, grupos))
    return svg, info, (largura_mm, altura_mm)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("imagem")
    ap.add_argument("saida")
    ap.add_argument("--tecido", choices=sorted(PALETAS), required=True)
    ap.add_argument("--altura-max-mm", type=float, default=350.0)
    ap.add_argument("--largura-max-mm", type=float, default=320.0)
    ap.add_argument("--garantir-mm", type=float, default=0.6)
    a = ap.parse_args(argv)
    svg, info, (lw, lh) = separar_cores(a.imagem, a.tecido, a.garantir_mm, a.altura_max_mm,
                                        a.largura_max_mm)
    with open(a.saida, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("%s  %.1f × %.1f cm" % (a.saida, lw / 10, lh / 10))
    for nome, cor, area, nota in info:
        print("  %-14s %s  %5.1f%% da arte  %s" % (nome, cor, area, nota))
    return 0


if __name__ == "__main__":
    sys.exit(main())
