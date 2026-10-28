"""Padroniza fotos da vitrine (loja, catálogo do Instagram/WhatsApp, story) da Modestino.

python3 .claude/skills/estudio-criativo-modestino/foto.py <foto.jpg> [<foto2> ...] [--foco x,y] [--saida loja/estudio/vitrine]

Para cada foto: corrige a orientação, aplica a mesma cor dos vídeos (predefinição "Modestino":
contraste +8, saturação −8, leve calor, nitidez leve) e exporta três cortes a partir do ponto de
foco (padrão: centro, 40% da altura, para pegar peito e gola, não o rosto):
  <nome>-produto.jpg   2048×2560 (4:5, página de produto da Shopify)
  <nome>-catalogo.jpg  1080×1080 (1:1, catálogo Meta/WhatsApp)
  <nome>-story.jpg     1080×1920 (9:16, story/capa de Reel)
Recorte de fundo e sombra (Photoroom) é um passo à parte e gasta créditos: só com o ok do Jorge.
"""
import argparse
import pathlib
import subprocess

GRADE = "eq=contrast=1.08:saturation=0.92:gamma_r=1.02:gamma_b=0.98,unsharp=5:5:0.3"
CORTES = {'produto': (2048, 2560), 'catalogo': (1080, 1080), 'story': (1080, 1920)}


def tamanho(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                          '-of', 'csv=p=0:s=x', str(p)], capture_output=True, text=True).stdout.strip()
    w, h = out.split('x')[:2]
    return int(w), int(h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fotos', nargs='+')
    ap.add_argument('--foco', default='0.5,0.4', help='ponto de foco x,y de 0 a 1')
    ap.add_argument('--saida', default='loja/estudio/vitrine')
    a = ap.parse_args()
    fx, fy = (float(v) for v in a.foco.split(','))
    saida = pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    for f in a.fotos:
        f = pathlib.Path(f)
        w, h = tamanho(f)
        for nome, (tw, th) in CORTES.items():
            # maior recorte na proporção alvo que cabe na foto, centrado no foco
            r = tw / th
            cw, ch = (w, round(w / r)) if w / h < r else (round(h * r), h)
            x = min(max(round(fx * w - cw / 2), 0), w - cw)
            y = min(max(round(fy * h - ch / 2), 0), h - ch)
            alvo = saida / f"{f.stem}-{nome}.jpg"
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(f), '-vf',
                            f"crop={cw}:{ch}:{x}:{y},scale={tw}:{th}:flags=lanczos,{GRADE}", '-q:v', '3', str(alvo)], check=True)
            aviso = '  (ampliada: foto pequena para este corte)' if cw < tw else ''
            print(f'{alvo}{aviso}')


if __name__ == '__main__':
    main()
