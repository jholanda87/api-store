"""Exclusivas · Assinatura MODESTINO (rabisco do Jorge), traço limpo e 3 faixas diagonais de cor.

Rode da raiz: python3 estampas/exclusivas/assinatura/assinatura.py
Lê rascunho-jorge.jpg, limpa o papel, refaz o traço pela linha central (espessura constante, pontas
redondas) e divide o desenho em 3 faixas na diagonal dos traços, uma tinta por faixa.
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cavalheiro-colorido'))
from colorir import traco_limpo, tracar_suave  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
LARGURA_MM = 300.0
# tecido: [(nome, hex, Pantone mais próximo)] da esquerda para a direita
PALETAS = {
    'preta': [('linho', '#ECE7DE', 'Pantone 9224 C'), ('ocre', '#C9A25E', 'Pantone 7562 C'),
              ('salvia', '#8E9B7A', 'Pantone 5625 C')],
    'mapple': [('linho', '#ECE7DE', 'Pantone 9224 C'), ('areia-dourada', '#D8B878', 'Pantone 7508 C'),
               ('azul-mar', '#9FB4B3', 'Pantone 5503 C')],
    'offwhite': [('carvao', '#22201D', 'Pantone Black 7 C'), ('mapple', '#5B3F30', 'Pantone 7533 C'),
                 ('oliva', '#6B7350', 'Pantone 5753 C')],
}


def main():
    g = np.asarray(Image.open(os.path.join(AQUI, 'rascunho-jorge.jpg')).convert('L'), float)
    g = g[540:1680, 200:1180]                                   # só o desenho
    papel = ndi.gaussian_filter(g, 40)
    norm = g / np.maximum(papel, 1)                              # tira a sombra e o cinza do papel
    linha = norm < 0.82
    linha = ndi.binary_opening(linha, iterations=1)
    lab, n = ndi.label(linha)
    tam = ndi.sum(linha, lab, range(1, n + 1))
    linha = np.isin(lab, [i + 1 for i, t in enumerate(tam) if t > 300])   # some com a moldura fraca e sujeira
    ys, xs = np.nonzero(linha)
    linha = linha[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    # amplia 2x antes de refazer: curvas mais redondas
    L = np.array(Image.fromarray(linha.astype('uint8') * 255).resize((linha.shape[1] * 2, linha.shape[0] * 2),
                                                                    Image.LANCZOS)) > 127
    h, w = L.shape
    mm_px = LARGURA_MM / w
    L = ndi.binary_closing(L, iterations=6)          # junta os traços duplos do grafite em um só
    traco = traco_limpo(L, mm_px, espessura_mm=3.2)
    traco = ndi.gaussian_filter(traco.astype(float), 3) > 0.5   # acabamento: borda lisa e redonda
    # faixas na diagonal dos traços (inclinação medida no rascunho: ~0,35 em x por 1 em y)
    yy, xx = np.mgrid[0:h, 0:w]
    u = xx - 0.35 * yy
    q1, q2 = np.quantile(u[traco], [1 / 3, 2 / 3])
    faixas = [traco & (u < q1), traco & (u >= q1) & (u < q2), traco & (u >= q2)]
    caminhos = [tracar_suave(f, 4) for f in faixas]
    for tecido, cores in PALETAS.items():
        grupos = '\n'.join('  <g id="tinta-%s"><title>%s</title><path fill="%s" fill-rule="evenodd" d="%s"/></g>'
                           % (n_, p, c, d) for (n_, c, p), d in zip(cores, caminhos))
        open(os.path.join(AQUI, 'assinatura-%s.svg' % tecido), 'w').write(
            '<svg xmlns="http://www.w3.org/2000/svg" width="%.1fmm" height="%.1fmm" viewBox="0 0 %d %d">\n'
            '  <title>Exclusivas · Assinatura MODESTINO (desenho do Jorge) · camiseta %s · 3 tintas</title>\n%s\n</svg>\n'
            % (LARGURA_MM, h * mm_px, w, h, tecido, grupos))
    print('ok', LARGURA_MM / 10, 'x', round(h * mm_px / 10, 1), 'cm')


if __name__ == '__main__':
    main()
