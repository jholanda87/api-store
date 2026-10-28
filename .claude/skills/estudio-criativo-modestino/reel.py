"""Monta um Reel 1080×1920 da Modestino a partir de cortes de vídeo bruto (ffmpeg).

python3 .claude/skills/estudio-criativo-modestino/reel.py loja/estudio/lotes/<lote>/<reel>.json

O JSON lista os cortes (vídeo, início, fim, enquadramento, overlay PNG feito com arte.js) e a
tela final. Aplica a predefinição de cor "Modestino" (a mesma do CapCut: contraste +8,
saturação −8, temperatura levemente quente, nitidez leve), corta em 9:16 com o foco na roupa,
encaixa os textos e exporta sem áudio (a música em alta é escolhida no Instagram).
Também salva uma folha de quadros (1 por corte) para conferir que nenhum corte quebra as regras.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[3]
GRADE = "eq=contrast=1.08:saturation=0.92:gamma_r=1.02:gamma_b=0.98,unsharp=5:5:0.35"


def rodar(cmd):
    subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)


def caminho(p, base):
    p = pathlib.Path(p)
    return p if p.is_absolute() else (base / p).resolve()


def main(arq):
    arq = pathlib.Path(arq).resolve()
    spec = json.loads(arq.read_text())
    base = arq.parent
    saida = caminho(spec.get('saida', f"{spec['nome']}.mp4"), base)
    fps = spec.get('fps', 30)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        partes = []
        for i, c in enumerate(spec['cortes']):
            # enquadramento: [x, y, largura] no quadro original em pé (720×1280); altura = largura × 16/9
            x, y, w = c.get('quadro', [0, 0, 720])
            h = round(w * 16 / 9)
            filtro = f"crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos,{GRADE},fps={fps},setsar=1"
            entradas = ['-ss', str(c['inicio']), '-to', str(c['fim']), '-i', str(caminho(c['video'], base))]
            if c.get('overlay'):
                entradas += ['-loop', '1', '-i', str(caminho(c['overlay'], base))]
                dur = c['fim'] - c['inicio']
                filtro = (f"[0:v]{filtro}[v];[1:v]format=rgba,fade=t=in:st=0:d=0.18:alpha=1[o];"
                          f"[v][o]overlay=0:0:shortest=1,trim=duration={dur}[s]")
                mapa = ['-filter_complex', filtro, '-map', '[s]']
            else:
                mapa = ['-vf', filtro]
            parte = tmp / f'p{i:02d}.mp4'
            rodar(['ffmpeg', '-v', 'error', '-y', *entradas, *mapa, '-an',
                   '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', str(parte)])
            partes.append(parte)
        if spec.get('final'):
            f = spec['final']
            parte = tmp / 'final.mp4'
            rodar(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', str(f.get('duracao', 1.6)),
                   '-i', str(caminho(f['png'], base)), '-vf', f"scale=1080:1920,fps={fps},format=yuv420p,fade=t=in:st=0:d=0.25",
                   '-c:v', 'libx264', '-crf', '18', str(parte)])
            partes.append(parte)
        lista = tmp / 'lista.txt'
        lista.write_text(''.join(f"file '{p}'\n" for p in partes))
        saida.parent.mkdir(parents=True, exist_ok=True)
        rodar(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lista),
               '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p',
               '-movflags', '+faststart', '-an', str(saida)])
        # folha de conferência: um quadro do meio de cada corte
        quadros = []
        for i, p in enumerate(partes):
            q = tmp / f'q{i:02d}.png'
            rodar(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.6', '-i', str(p), '-frames:v', '1', '-vf', 'scale=216:384', str(q)])
            quadros.append(q)
        entradas = sum([['-i', str(q)] for q in quadros], [])
        rodar(['ffmpeg', '-v', 'error', '-y', *entradas, '-filter_complex',
               ''.join(f'[{i}:v]' for i in range(len(quadros))) + f'hstack=inputs={len(quadros)}',
               str(saida.with_name(saida.stem + '-quadros.png'))])
    dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(saida)],
                         capture_output=True, text=True).stdout.strip()
    nome = saida.relative_to(RAIZ) if saida.is_relative_to(RAIZ) else saida
    print(f'{nome} · {float(dur):.1f} s')


if __name__ == '__main__':
    main(sys.argv[1])
