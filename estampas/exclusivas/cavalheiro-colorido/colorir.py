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
import textura  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
ALTURA_MM = 350.0
PALETAS = {  # tecido: (traço, quente, fria)
    'preta': ('#ECE7DE', '#C9A25E', '#8E9B7A'),
    'mapple': ('#ECE7DE', '#D8B878', '#9FB4B3'),
    'offwhite': ('#22201D', '#5B3F30', '#6B7350'),
}
FRAQUE = [27, 56, 82, 95, 66, 36]           # regiões do mapa (dilatação 4 px); 69 = vão entre braço e tronco, fica vazado
QUENTE = [60, 47, 64, 79, 4, 24, 90]        # colete, rosto, pescoço, mão


VOLUME = '--volume' in sys.argv


def volume(lab, ids, mm_px, ponto_mm=0.8):
    """Sombra e luz em pontilhismo dentro das áreas coloridas (luz de cima à esquerda).
    Devolve duas máscaras de pontos (sombra, luz) no tamanho da imagem."""
    from skimage.draw import disk
    h, w = lab.shape
    tom = np.zeros((h, w))
    for k in ids:
        m = lab == k
        if not m.any():
            continue
        ys, xs = np.nonzero(m)
        x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        xr = (np.arange(w)[None, :] - x0) / max(1, x1 - x0)
        yr = (np.arange(h)[:, None] - y0) / max(1, y1 - y0)
        borda = np.exp(-ndi.distance_transform_edt(m) / (2.5 / mm_px))  # escurece junto do traço
        t = 0.55 * xr + 0.3 * yr + 0.45 * borda * (xr > 0.35)
        tom[m] = np.clip(t, 0, 1)[m]
    passo = 0.25  # mm, grade do pontilhismo
    g = Image.fromarray((tom * 255).astype('uint8')).resize((int(w * mm_px / passo), int(h * mm_px / passo)))
    escuro = (np.asarray(g) / 255.0)
    def pontos(campo):
        e = [[float(v) for v in linha] for linha in campo]
        pts, _, _ = textura.pontilhismo(e, campo.shape[1], campo.shape[0], passo, ponto_mm, 5)
        mask = np.zeros((h, w), bool)
        r = ponto_mm / 2 / mm_px
        for x, y in pts:
            rr, cc = disk((y / mm_px, x / mm_px), r, shape=(h, w))
            mask[rr, cc] = True
        return mask
    dentro = np.isin(lab, ids)
    sombra = pontos(np.clip((escuro - 0.33) * 1.8, 0, 1) ** 0.85) & dentro
    luz = pontos(np.clip((0.26 - escuro) * 3.0, 0, 1) * (escuro > 0)) & dentro
    return sombra, luz


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
    sombra, luz = volume(lab, FRAQUE + QUENTE, mm_px) if VOLUME else (None, None)
    h, w = a.shape
    sufixo = '-volume' if VOLUME else ''
    for tecido, (traco, quente, fria) in PALETAS.items():
        cam = {k: v.copy() for k, v in camadas.items()}
        if VOLUME:
            if tecido == 'offwhite':  # sombra em pontos de carvão; luz vaza o tecido claro
                cam['traco'] |= sombra; cam['fria'] &= ~(sombra | luz); cam['quente'] &= ~(sombra | luz)
            else:  # sombra vaza o tecido escuro; luz em pontos de linho (a tinta do traço)
                cam['fria'] &= ~(sombra | luz); cam['quente'] &= ~(sombra | luz); cam['traco'] |= luz
        caminhos = {}
        for nome, m in cam.items():
            d, _ = vetorizar.tracar(Image.fromarray(np.where(m, 0, 255).astype('uint8')), 128, 2)
            caminhos[nome] = ''.join(d)
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%.1fmm" height="%.1fmm" viewBox="0 0 %d %d">\n'
               '  <title>Exclusivas · O Cavalheiro colorido%s · costas 35 cm · camiseta %s · 3 tintas</title>\n'
               '  <g id="tinta-fria"><path fill="%s" fill-rule="evenodd" d="%s"/></g>\n'
               '  <g id="tinta-quente"><path fill="%s" fill-rule="evenodd" d="%s"/></g>\n'
               '  <g id="tinta-traco"><path fill="%s" fill-rule="evenodd" d="%s"/></g>\n</svg>\n'
               % (w * mm_px, ALTURA_MM, w, h, ' com volume' if VOLUME else '', tecido, fria, caminhos['fria'],
                  quente, caminhos['quente'], traco, caminhos['traco']))
        open(os.path.join(AQUI, 'cavalheiro-colorido%s-%s.svg' % (sufixo, tecido)), 'w').write(svg)
    print('ok', round(w * mm_px / 10, 1), 'x', ALTURA_MM / 10, 'cm')


if __name__ == '__main__':
    main(sys.argv[1])
