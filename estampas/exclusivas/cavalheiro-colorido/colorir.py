"""Exclusivas · O Cavalheiro colorido (costas, 35 cm). Traço original do guia, preenchido por áreas.

Rode da raiz: python3 estampas/exclusivas/cavalheiro-colorido/colorir.py caminho/img-000.png
(img-000.png = página 1 do 'Modestino — O Cavalheiro.pdf', extraída com pdfimages).
Traço na tinta principal do tecido; fraque na tinta fria; colete, rosto e mão na tinta quente;
calça, cartola e sapatos ficam no tecido (vazado). Até 3 tintas por camiseta.
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0, '.claude/skills/estampa-arte-modestino')
import vetorizar  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
ALTURA_MM = 350.0
PALETAS = {  # tecido: (traço, quente, fria)
    'preta': ('#ECE7DE', '#C9A25E', '#8E9B7A'),
    'mapple': ('#ECE7DE', '#D8B878', '#9FB4B3'),
    'offwhite': ('#22201D', '#5B3F30', '#6B7350'),
}
FRAQUE = [27, 56, 69, 82, 95, 66, 36]       # regiões do mapa (dilatação 4 px)
QUENTE = [60, 47, 64, 79, 4, 24, 90]        # colete, rosto, pescoço, mão


def main(fonte):
    a = np.array(Image.open(fonte).convert('L').crop((340, 320, 1020, 2240)))
    linha = a < 140
    lab, _ = ndi.label(~ndi.binary_dilation(linha, iterations=4))
    mm_px = ALTURA_MM / a.shape[0]
    def mascara(ids):
        m = np.isin(lab, ids)
        return ndi.binary_dilation(m, iterations=5) & ~linha | m  # encosta no traço, por baixo dele
    camadas = {'fria': mascara(FRAQUE), 'quente': mascara(QUENTE)}
    L = Image.fromarray(np.where(linha, 0, 255).astype('uint8'))
    camadas['traco'] = np.array(vetorizar.garantir(L, mm_px, 0.8)) == 0
    caminhos = {}
    for nome, m in camadas.items():
        d, _ = vetorizar.tracar(Image.fromarray(np.where(m, 0, 255).astype('uint8')), 128, 6)
        caminhos[nome] = ''.join(d)
    h, w = a.shape
    for tecido, (traco, quente, fria) in PALETAS.items():
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%.1fmm" height="%.1fmm" viewBox="0 0 %d %d">\n'
               '  <title>Exclusivas · O Cavalheiro colorido · costas 35 cm · camiseta %s · 3 tintas</title>\n'
               '  <g id="tinta-fria"><path fill="%s" fill-rule="evenodd" d="%s"/></g>\n'
               '  <g id="tinta-quente"><path fill="%s" fill-rule="evenodd" d="%s"/></g>\n'
               '  <g id="tinta-traco"><path fill="%s" fill-rule="evenodd" d="%s"/></g>\n</svg>\n'
               % (w * mm_px, ALTURA_MM, w, h, tecido, fria, caminhos['fria'], quente, caminhos['quente'],
                  traco, caminhos['traco']))
        open(os.path.join(AQUI, 'cavalheiro-colorido-%s.svg' % tecido), 'w').write(svg)
    print('ok', round(w * mm_px / 10, 1), 'x', ALTURA_MM / 10, 'cm')


if __name__ == '__main__':
    main(sys.argv[1])
