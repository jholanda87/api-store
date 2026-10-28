"""Vídeos de efeito a partir da peça recortada (PNG de recorte.py ou ia.py), sem custo e sem conector.

python3 .claude/skills/estudio-criativo-modestino/efeitos.py <efeito> <peca.png> [<peca2.png> ...] [opções]

Efeitos (1080×1920, 30 fps, sem áudio: a música em alta entra no Instagram):
  flutuar   a peça flutua e respira em loop perfeito (6 s)          — capa de Reel, story, fundo de anúncio
  cores     troca de peça no ritmo, com leve "pulo" a cada corte    — "Três cores, várias combinações." (uma PNG por cor)
  zoom      aproxima devagar até um detalhe (--foco x,y de 0 a 1)  — "olhe de perto": gola, etiqueta, costura
Opções: --fundo linho|areia|carvao|mapple  --segundos N  --batida 0.6 (cores)  --foco 0.5,0.12 (zoom)  --saida arquivo.mp4
Giro de 360°, tecido esticando e peça "vestida" por corpo invisível: ia.py video (gerado por IA).
"""
import argparse
import math
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from recorte import FUNDOS, rgb, C  # noqa: E402

W, H, FPS = 1080, 1920, 30


def preparar(png, ocupa=0.78):
    p = Image.open(png).convert('RGBA')
    p = p.crop(p.getbbox())
    esc = min(W * ocupa / p.width, H * 0.62 / p.height)
    return p.resize((round(p.width * esc), round(p.height * esc)), Image.LANCZOS)


def fundo_com_sombra(cor, p, y, escala=1.0):
    tela = Image.new('RGBA', (W, H), rgb(cor) + (255,))
    if sum(rgb(cor)) < 300:
        return tela
    pw, ph = p.size
    sw = max(1, round(pw * 0.8 * escala))
    sombra = Image.new('L', (W, H), 0)
    base = p.split()[3].resize((sw, max(1, round(ph * 0.07))))
    sombra.paste(255, ((W - sw) // 2, y + ph + 70), base)
    sombra = sombra.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.3 * escala))
    return Image.composite(Image.new('RGBA', (W, H), rgb(C['surface-dark']) + (255,)), tela, sombra)


def flutuar(pecas, a):
    p = preparar(pecas[0])
    y0 = round((H - p.height) * 0.42)
    n = round(a.segundos * FPS)
    for i in range(n):
        t = i / n
        dy = round(-26 * math.sin(2 * math.pi * t))
        # a sombra encolhe quando a peça sobe: dá a sensação de altura
        tela = fundo_com_sombra(FUNDOS[a.fundo], p, y0 - dy // 2, escala=1 - 0.12 * (-dy / 26))
        tela.alpha_composite(p, ((W - p.width) // 2, y0 + dy))
        yield tela


def cores(pecas, a):
    ps = [preparar(x) for x in pecas]
    n = round(a.segundos * FPS)
    passo = max(1, round(a.batida * FPS))
    for i in range(n):
        k, f = (i // passo) % len(ps), (i % passo) / passo
        pulo = 1 + 0.06 * math.exp(-f * 8)          # entra 6% maior e assenta
        p = ps[k].resize((round(ps[k].width * pulo), round(ps[k].height * pulo)), Image.BILINEAR)
        y = round((H - p.height) * 0.42)
        tela = fundo_com_sombra(FUNDOS[a.fundo], p, y)
        tela.alpha_composite(p, ((W - p.width) // 2, y))
        yield tela


def zoom(pecas, a):
    fx, fy = (float(v) for v in a.foco.split(','))
    p = Image.open(pecas[0]).convert('RGBA')
    p = p.crop(p.getbbox())
    base = Image.new('RGBA', p.size, rgb(FUNDOS[a.fundo]) + (255,))
    base.alpha_composite(p)
    n = round(a.segundos * FPS)
    for i in range(n):
        t = i / max(1, n - 1)
        e = t * t * (3 - 2 * t)                       # começa e termina suave
        # janela 9:16 que vai da peça inteira até ~1/4 da largura, centrada no foco
        cw = p.width * (1.15 - 0.85 * e)
        ch = cw * H / W
        cx = p.width / 2 + (fx * p.width - p.width / 2) * e
        cy = p.height / 2 + (fy * p.height - p.height / 2) * e
        caixa = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        fundo = Image.new('RGBA', (round(cw), round(ch)), rgb(FUNDOS[a.fundo]) + (255,))
        x0, y0 = round(caixa[0]), round(caixa[1])
        fundo.alpha_composite(base.crop((max(0, x0), max(0, y0), min(p.width, x0 + fundo.width), min(p.height, y0 + fundo.height))),
                              (max(0, -x0), max(0, -y0)))
        yield fundo.resize((W, H), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('efeito', choices=['flutuar', 'cores', 'zoom'])
    ap.add_argument('pecas', nargs='+')
    ap.add_argument('--fundo', default='linho', choices=FUNDOS)
    ap.add_argument('--segundos', type=float, default=6)
    ap.add_argument('--batida', type=float, default=0.6)
    ap.add_argument('--foco', default='0.5,0.12')
    ap.add_argument('--saida')
    a = ap.parse_args()
    saida = pathlib.Path(a.saida or pathlib.Path(a.pecas[0]).with_name(f'{pathlib.Path(a.pecas[0]).stem}-{a.efeito}.mp4'))
    ff = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
                           '-movflags', '+faststart', str(saida)], stdin=subprocess.PIPE)
    for quadro in {'flutuar': flutuar, 'cores': cores, 'zoom': zoom}[a.efeito](a.pecas, a):
        ff.stdin.write(np.asarray(quadro.convert('RGB')).tobytes())
    ff.stdin.close()
    ff.wait()
    print(saida)


if __name__ == '__main__':
    main()
