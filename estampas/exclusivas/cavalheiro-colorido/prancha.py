"""Exclusivas · O Cavalheiro na paleta da prancha de moda (Le Follet, c. 1840), com sombra de aquarela.

Rode da raiz: python3 estampas/exclusivas/cavalheiro-colorido/prancha.py caminho/img-000.png
Referência do Jorge: a figura da esquerda da prancha "Le Follet Courrier des Salons" (domínio público).
Desenho: o nosso Cavalheiro (sozinho, mão no bolso), com o traço limpo da versão 2.
Padrão Modestino: costas 35 cm, traço linho na preta e na mapple, carvão na off-white.
Policromática (DTF): sai PNG com transparência a ~280 dpi no tamanho real, mais o SVG para o mockup.
"""
import base64, io, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from colorir import traco_limpo  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
ALTURA_MM, ESCALA = 350.0, 2

# cores da prancha (figura da esquerda)
COR = {
    'fraque': (31, 61, 51), 'colete': (227, 207, 160), 'camisa': (244, 239, 227), 'gravata': (28, 26, 25),
    'pele': (231, 190, 152), 'luva': (233, 216, 162), 'calca': (237, 227, 200), 'cartola': (140, 139, 134),
    'sapato': (28, 26, 25),
}
REGIOES = {  # números do mapa de áreas (traço dilatado 4 px); 69 e 118 são vãos: ficam vazados
    'fraque': [27, 36, 50, 56, 63, 72, 82, 95], 'colete': [60, 64, 66, 78, 79, 83], 'camisa': [33, 47],
    'gravata': [44], 'pele': [4, 24], 'luva': [90], 'calca': [85, 113], 'sapato': [129, 134, 137],
}
TRACO = {'preta': (242, 238, 230), 'mapple': (242, 238, 230), 'offwhite': (34, 32, 29)}
FRAQUE_NA_PRETA = (44, 85, 70)  # o verde da prancha sumiria no preto: um tom acima, mesma família


def sombra(m, mm_px):
    """Tom 0 (luz) a 1 (sombra) dentro da área: luz de cima à esquerda, escurece junto da borda."""
    ys, xs = np.nonzero(m)
    h, w = m.shape
    xr = (np.arange(w)[None, :] - xs.min()) / max(1, xs.max() - xs.min())
    yr = (np.arange(h)[:, None] - ys.min()) / max(1, ys.max() - ys.min())
    borda = np.exp(-ndi.distance_transform_edt(m) / (3.0 / mm_px))
    t = 0.5 * xr + 0.3 * yr + 0.5 * borda * (xr > 0.3)
    return np.clip(ndi.gaussian_filter(t, 6), 0, 1)


def main(fonte):
    a = np.array(Image.open(fonte).convert('L').crop((340, 320, 1020, 2240)))
    linha = a < 140
    lab, _ = ndi.label(~ndi.binary_dilation(linha, iterations=4))
    lab9, _ = ndi.label(~ndi.binary_dilation(linha, iterations=9))
    cartola = lab9 == lab9[120, 495]                     # a cartola só fecha com dilatação maior
    h, w = a.shape
    H, W = h * ESCALA, w * ESCALA
    mm_px = ALTURA_MM / H
    up = lambda m: np.array(Image.fromarray(m.astype('uint8') * 255).resize((W, H), Image.NEAREST)) > 0
    # bengala: o original é traço duplo de caneta (vira "corrente"); sai e entra uma vara reta no mesmo eixo
    c, d = np.array([113.86, 1589.04]), np.array([-0.25794, 0.96616])   # eixo medido no desenho
    def no_eixo(y):
        return c + d * ((y - c[1]) / d[1])
    topo, ponta = no_eixo(900.0), no_eixo(1851.0)
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.abs((xx - c[0]) * d[1] - (yy - c[1]) * d[0])
    linha = linha & ~((dist < 22) & (yy > 935) & (yy < 1880))
    # traço limpo no tamanho original (contínuo) e só depois ampliado com suavização
    t1 = traco_limpo(linha, ALTURA_MM / h).astype('uint8') * 255
    from PIL import ImageDraw
    ImageDraw.Draw(t1_img := Image.fromarray(t1)).line([tuple(topo), tuple(ponta)], fill=255,
                                                     width=max(3, int(round(2.0 / (ALTURA_MM / h)))))
    t1 = np.array(t1_img)
    traco = np.array(Image.fromarray(t1).resize((W, H), Image.LANCZOS).filter(
        __import__('PIL.ImageFilter', fromlist=['x']).GaussianBlur(1.2))) > 127

    for tecido in ('preta', 'mapple', 'offwhite'):
        rgb = np.zeros((H, W, 3))
        alfa = np.zeros((H, W))
        grupos = dict(REGIOES)
        for nome in list(grupos) + ['cartola']:
            m1 = cartola if nome == 'cartola' else np.isin(lab, grupos[nome])
            m = ndi.binary_dilation(up(m1), iterations=10)     # encosta no traço, por baixo dele
            base = np.array(FRAQUE_NA_PRETA if (nome == 'fraque' and tecido == 'preta') else COR[nome], float)
            t = sombra(m, mm_px)[..., None]
            luz = np.clip((0.22 - t) / 0.22, 0, 1) * 0.18
            cor = base * (1 - 0.42 * t) * (1 - luz) + 255 * luz
            textura = 1 + 0.025 * ndi.gaussian_filter(np.random.default_rng(7).standard_normal((H, W)), 2)[..., None]
            cor = np.clip(cor * textura, 0, 255)
            rgb[m] = cor[m]
            alfa[m] = 1
        rgb[traco] = TRACO[tecido]
        alfa[traco] = 1
        png = Image.fromarray(np.dstack([rgb, alfa * 255]).astype('uint8'), 'RGBA')
        arq = os.path.join(AQUI, 'cavalheiro-prancha-%s.png' % tecido)
        png.save(arq, dpi=(int(H / (ALTURA_MM / 25.4)),) * 2)
        buf = io.BytesIO(); png.save(buf, 'PNG')
        open(arq.replace('.png', '.svg'), 'w').write(
            '<svg xmlns="http://www.w3.org/2000/svg" width="%.1fmm" height="%.1fmm" viewBox="0 0 %d %d">'
            '<image width="%d" height="%d" href="data:image/png;base64,%s"/></svg>'
            % (W * mm_px, ALTURA_MM, W, H, W, H, base64.b64encode(buf.getvalue()).decode()))
    print('ok', W, 'x', H, 'px ·', round(W * mm_px / 10, 1), 'x', ALTURA_MM / 10, 'cm ·',
          int(H / (ALTURA_MM / 25.4)), 'dpi')


if __name__ == '__main__':
    main(sys.argv[1])
