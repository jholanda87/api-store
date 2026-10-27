"""Gera as variáveis CSS a partir de loja/design/tokens.json.

python3 loja/tema/tools/gerar_tokens.py
Escreve loja/design/tokens.css (com @font-face relativo) e loja/tema/assets/modestino-tokens.css (sem fontes;
no tema as fontes entram por snippets/modestino-head.liquid, com asset_url).
"""
import json, pathlib

raiz = pathlib.Path(__file__).resolve().parents[3]
t = json.loads((raiz / 'loja/design/tokens.json').read_text())

def rem(px):
    return f"{px / 16:g}rem"

linhas = [':root {']
linhas += [f"  --color-{k}: {v};" for k, v in t['color'].items()]
linhas += [f"  --font-{k}: {v};" for k, v in t['font'].items()]
for k, v in t['type'].items():
    linhas.append(f"  --text-{k}-size: {rem(v['size'])}; --text-{k}-line: {rem(v['line'])}; --text-{k}-weight: {v['weight']};")
linhas += [f"  --space-{i}: {rem(v)};" for i, v in enumerate(t['space'])]
linhas += [f"  --radius-{k}: {v}px;" for k, v in t['radius'].items()]
linhas += [f"  --size-{k}: {v}px;" for k, v in t.get('size', {}).items()]
if 'measure' in t:
    linhas.append(f"  --measure: {t['measure']};")
linhas += [f"  --shadow-{k}: {v};" for k, v in t['shadow'].items()]
linhas += [f"  --motion-{k}: {v};" for k, v in t['motion'].items()]
linhas.append('}')
corpo = '\n'.join(linhas) + '\n'

fontes = [
    ('Instrument Serif', 'instrument-serif-latin-400-normal.woff2', 400, 'normal'),
    ('Instrument Serif', 'instrument-serif-latin-400-italic.woff2', 400, 'italic'),
    ('Instrument Sans', 'instrument-sans-latin-400-normal.woff2', 400, 'normal'),
    ('Instrument Sans', 'instrument-sans-latin-600-normal.woff2', 600, 'normal'),
    ('Geist Mono', 'geist-mono-latin-400-normal.woff2', 400, 'normal'),
]
ff = ''.join(
    f"@font-face {{ font-family: '{n}'; src: url('fonts/{a}') format('woff2'); font-weight: {w}; font-style: {s}; font-display: swap; }}\n"
    for n, a, w, s in fontes)
cab = '/* Gerado de tokens.json por loja/tema/tools/gerar_tokens.py. Não editar à mão. */\n'
(raiz / 'loja/design/tokens.css').write_text(cab + ff + '\n' + corpo)
(raiz / 'loja/tema/assets/modestino-tokens.css').write_text(cab + corpo)
print('ok')
