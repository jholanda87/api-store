#!/usr/bin/env python3
"""Confere se uma estampa em SVG está pronta para ir para a camiseta.

Uso:
  python3 estampa.py arte.svg [--tecnica silk|dtf|bordado] [--posicao peito|frente|costas|nuca|manga]
                              [--max-tintas 2] [--largura-cm 9] [--vazado "#1E1D1C"]
                              [--marca loja/marca.json] [--json]

Lê o SVG (só biblioteca padrão), descobre o tamanho real, as tintas, o traço mais fino
em milímetros e o contraste de cada tinta nas três cores da camiseta. Sai com código 1
se houver ERRO. Também é importado por separar.py e mockup.py.
"""

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"

# Cores das camisetas (aproximadas pela identidade; confirmar com a amostra de tecido).
CAMISETAS = {"preto": "#1E1D1C", "mapple": "#5B3F30", "off-white": "#ECE7DE"}

# Tintas sugeridas: a paleta da marca mais branco e preto de gráfica.
PALETA = {
    "#ECE7DE": "linho", "#E4DDD0": "linho escuro", "#CBBFAE": "areia", "#6E675F": "grafite",
    "#5B3F30": "mapple", "#22201D": "carvão", "#1E1D1C": "carvão fundo",
    "#FFFFFF": "branco", "#000000": "preto",
}

# Traço mínimo (mm) e tintas que cada técnica aceita sem dor.
TECNICAS = {
    "silk": {"traco_min": 0.5, "detalhe_min": 0.8, "degrade": "erro"},
    "dtf": {"traco_min": 0.3, "detalhe_min": 0.5, "degrade": "aviso"},
    "bordado": {"traco_min": 1.0, "detalhe_min": 1.5, "degrade": "erro"},
}

# Maior lado da arte (cm) que funciona em cada posição, camiseta P a GG.
# Peito 4 a 6 cm é o busto do guia; frente 7 cm é a figura e nome.
POSICOES = {
    "peito": (4, 10), "frente": (7, 28), "costas": (10, 32), "nuca": (1, 8), "manga": (1, 8),
}

SHAPES = {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "text", "use"}
NOMES = {"black": "#000000", "white": "#FFFFFF", "red": "#FF0000", "blue": "#0000FF",
         "green": "#008000", "gray": "#808080", "grey": "#808080"}
UNIDADES = {"mm": 1.0, "cm": 10.0, "in": 25.4, "pt": 25.4 / 72, "px": 25.4 / 96, "": 25.4 / 96}


def local(tag):
    return tag.split("}")[-1] if isinstance(tag, str) else ""


def cor(valor):
    """Normaliza uma cor para #RRGGBB. None = sem tinta. 'url' = degradê/padrão."""
    if valor is None:
        return None
    v = valor.strip().lower()
    if v in ("none", "transparent", ""):
        return None
    if v.startswith("url("):
        return "url"
    if v in NOMES:
        return NOMES[v]
    m = re.fullmatch(r"#([0-9a-f]{3})", v)
    if m:
        return "#" + "".join(c * 2 for c in m.group(1)).upper()
    m = re.fullmatch(r"#([0-9a-f]{6})", v)
    if m:
        return v.upper()
    m = re.fullmatch(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", v)
    if m:
        return "#" + "".join("%02X" % min(255, int(x)) for x in m.groups())
    return "?" + valor.strip()


def estilo(el):
    """Propriedades de pintura do elemento (atributo e style inline; style vence)."""
    props = {}
    for k in ("fill", "stroke", "stroke-width", "opacity", "fill-opacity", "stroke-opacity"):
        if el.get(k) is not None:
            props[k] = el.get(k)
    for parte in (el.get("style") or "").split(";"):
        if ":" in parte:
            k, v = parte.split(":", 1)
            k = k.strip()
            if k in ("fill", "stroke", "stroke-width", "opacity", "fill-opacity", "stroke-opacity"):
                props[k] = v.strip()
    return props


def numero(v, padrao=0.0):
    m = re.match(r"\s*(-?[\d.]+(?:e-?\d+)?)", str(v or ""))
    return float(m.group(1)) if m else padrao


def contraste(a, b):
    def lum(h):
        rgb = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def clara(h):
    return contraste(h, "#000000") > contraste(h, "#FFFFFF")


def tamanho_mm(root, largura_cm=None):
    """(largura_mm, altura_mm, mm_por_unidade) ou None se não der para saber."""
    vb = [numero(x) for x in re.split(r"[\s,]+", (root.get("viewBox") or "").strip()) if x]
    if len(vb) != 4 or vb[2] <= 0 or vb[3] <= 0:
        return None
    if largura_cm:
        escala = largura_cm * 10 / vb[2]
        return vb[2] * escala, vb[3] * escala, escala
    w = root.get("width") or ""
    m = re.fullmatch(r"\s*([\d.]+)\s*(mm|cm|in|pt|px|)\s*", w)
    if not m or not m.group(2) or m.group(2) == "px":
        return None
    largura = float(m.group(1)) * UNIDADES[m.group(2)]
    escala = largura / vb[2]
    return largura, vb[3] * escala, escala


def pinturas(root):
    """Cada forma com a tinta efetiva (herança de grupo). Lista de dicts na ordem de pintura."""
    saida = []

    def andar(el, herdado):
        tag = local(el.tag)
        if tag in ("defs", "clipPath", "mask", "symbol", "metadata", "title", "desc", "style"):
            return
        p = dict(herdado)
        p.update(estilo(el))
        p["_op"] = herdado.get("_op", 1.0) * numero(estilo(el).get("opacity", 1), 1.0)
        if tag in SHAPES:
            fill = None if tag == "line" else cor(p.get("fill", "#000000"))
            stroke = cor(p.get("stroke"))
            saida.append({
                "el": el, "tag": tag, "fill": fill, "stroke": stroke,
                "stroke_width": numero(p.get("stroke-width", 1), 1.0) if stroke else 0.0,
                "opacity": p["_op"] * numero(p.get("fill-opacity", 1), 1.0),
                "stroke_opacity": p["_op"] * numero(p.get("stroke-opacity", 1), 1.0),
            })
        for filho in el:
            andar(filho, p)

    andar(root, {})
    return saida


def tintas(formas, vazado=None):
    usadas = []
    for f in formas:
        for c in (f["fill"], f["stroke"]):
            if c and c != "url" and not c.startswith("?") and c != vazado and c not in usadas:
                usadas.append(c)
    return usadas


def avaliar(svg_texto, tecnica="silk", posicao=None, max_tintas=2, largura_cm=None,
            vazado=None, evitar=()):
    """Devolve {'tamanho_cm', 'tintas', 'camisetas', 'problemas': [{nivel, msg}]}."""
    problemas = []

    def add(nivel, msg):
        problemas.append({"nivel": nivel, "msg": msg})

    regra = TECNICAS[tecnica]
    vazado = cor(vazado) if vazado else None
    try:
        root = ET.fromstring(svg_texto)
    except ET.ParseError as e:
        return {"tamanho_cm": None, "tintas": [], "camisetas": {},
                "problemas": [{"nivel": "ERRO", "msg": "SVG inválido: %s" % e}]}

    medida = tamanho_mm(root, largura_cm)
    if medida is None:
        add("ERRO", "Sem tamanho real: use viewBox e width/height em mm (ex.: width=\"90mm\"), "
                    "ou passe --largura-cm.")
        escala = None
    else:
        escala = medida[2]

    todas = list(root.iter())
    tags = {local(e.tag) for e in todas}
    if tags & {"linearGradient", "radialGradient", "pattern"}:
        add("ERRO" if regra["degrade"] == "erro" else "AVISO",
            "Degradê/padrão: %s não reproduz bem. Use cor chapada ou retícula desenhada."
            % tecnica)
    if "filter" in tags:
        add("ERRO" if regra["degrade"] == "erro" else "AVISO",
            "Filtro (sombra, desfoque): não existe em tinta. Tire.")
    if "image" in tags:
        add("ERRO", "Tem imagem (bitmap) dentro: a arte autoral é vetor do começo ao fim.")
    if "text" in tags:
        add("ERRO", "Tem <text>: converta em curvas (curvas.py) para a gráfica não trocar a fonte.")
    if "style" in tags and re.search(r"\.[\w-]+\s*\{[^}]*(fill|stroke)", svg_texto):
        add("AVISO", "Cor por classe CSS: separar.py só lê fill/stroke no próprio elemento.")

    formas = pinturas(root)
    if not formas:
        add("ERRO", "Nenhuma forma desenhada.")

    for f in formas:
        if f["fill"] == "url" or f["stroke"] == "url":
            continue
        for c in (f["fill"], f["stroke"]):
            if c and c.startswith("?"):
                add("ERRO", "Cor que não entendi: %s (use #RRGGBB)." % c[1:])
        if f["opacity"] < 1 or (f["stroke"] and f["stroke_opacity"] < 1):
            add("ERRO" if regra["degrade"] == "erro" else "AVISO",
                "Transparência em <%s>: tinta não tem meio-tom. Use outra tinta ou retícula."
                % f["tag"])
            break

    usadas = tintas(formas, vazado)
    if len(usadas) > max_tintas:
        add("ERRO", "%d tintas (%s); o limite desta estampa é %d. Minimalismo: corte uma."
            % (len(usadas), ", ".join(usadas), max_tintas))
    for c in usadas:
        if c not in PALETA:
            add("INFO", "Tinta %s fora da paleta da marca: tudo bem se for de propósito." % c)

    if escala:
        finos = [f["stroke_width"] * escala for f in formas if f["stroke"] and f["stroke_width"]]
        if finos and min(finos) < regra["traco_min"]:
            add("ERRO", "Traço de %.2f mm: o mínimo em %s é %.1f mm. Engrosse ou aumente a arte."
                % (min(finos), tecnica, regra["traco_min"]))
        pequenos = []
        for f in formas:
            el = f["el"]
            if f["tag"] == "circle":
                pequenos.append(2 * numero(el.get("r")) * escala)
            elif f["tag"] == "rect":
                pequenos.append(min(numero(el.get("width")), numero(el.get("height"))) * escala)
        pequenos = [p for p in pequenos if p > 0]
        if pequenos and min(pequenos) < regra["detalhe_min"]:
            add("AVISO", "Detalhe de %.2f mm: abaixo de %.1f mm some ou entope em %s."
                % (min(pequenos), regra["detalhe_min"], tecnica))
        larg_cm = medida[0] / 10
        maior = max(medida[0], medida[1]) / 10
        if posicao:
            lo, hi = POSICOES[posicao]
            if not lo <= maior <= hi:
                add("AVISO", "%.1f cm no maior lado, no %s; o usual é %d a %d cm."
                    % (maior, posicao, lo, hi))
        if larg_cm > 32 or medida[1] / 10 > 40:
            add("AVISO", "Maior que 32 × 40 cm: passa da área útil de quase toda tela e do GG.")

    baixo = svg_texto.lower()
    for nome in evitar:
        if nome and nome.lower() in baixo:
            add("ERRO", "Nome de outra marca no arquivo: %s." % nome)
    if "cavalheiro" in baixo:
        add("INFO", "Leva o Cavalheiro: só o vetor oficial de estampas/marca/, sem distorcer, "
                    "redesenhar nem trocar o traço. Altura mínima: figura 5 cm, busto 3 cm, "
                    "cartola 1 cm (guia de identidade).")

    camisetas = {}
    for nome, fundo in CAMISETAS.items():
        r = {c: round(contraste(c, fundo), 2) for c in usadas}
        melhor = max(r.values()) if r else 0
        base = tecnica == "silk" and not clara(fundo) and any(clara(c) for c in usadas)
        camisetas[nome] = {"contraste": r, "funciona": melhor >= 3,
                           "tom_sobre_tom": bool(r) and melhor < 1.6, "base_branca": base}
        if r and melhor < 1.3:
            add("AVISO", "Na camiseta %s a estampa quase some (contraste %.2f). "
                         "Só use se o tom sobre tom for a ideia." % (nome, melhor))
        if base:
            add("INFO", "Na %s, tinta clara em silk pede base branca (+1 tela) "
                        "ou corrosão/base d'água: pergunte à gráfica." % nome)

    return {
        "tamanho_cm": [round(medida[0] / 10, 1), round(medida[1] / 10, 1)] if medida else None,
        "tintas": usadas, "camisetas": camisetas, "problemas": problemas,
    }


def ler_evitar(caminho):
    if not caminho:
        return []
    try:
        return json.load(open(caminho, encoding="utf-8")).get("avoid", [])
    except (OSError, ValueError):
        return []


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("svg")
    ap.add_argument("--tecnica", choices=sorted(TECNICAS), default="silk")
    ap.add_argument("--posicao", choices=sorted(POSICOES))
    ap.add_argument("--max-tintas", type=int, default=2)
    ap.add_argument("--largura-cm", type=float)
    ap.add_argument("--vazado", help="cor que é o próprio tecido (não conta como tinta)")
    ap.add_argument("--marca", help="loja/marca.json (nomes que não podem aparecer)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    texto = open(a.svg, encoding="utf-8").read()
    r = avaliar(texto, a.tecnica, a.posicao, a.max_tintas, a.largura_cm, a.vazado,
                ler_evitar(a.marca))
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        t = r["tamanho_cm"]
        print("Estampa: %s" % a.svg)
        print("Tamanho: %s" % ("%.1f × %.1f cm" % tuple(t) if t else "desconhecido"))
        print("Tintas (%d): %s" % (len(r["tintas"]), ", ".join(
            "%s %s" % (c, PALETA.get(c, "")) for c in r["tintas"]) or "nenhuma"))
        for nome, c in r["camisetas"].items():
            pares = ", ".join("%s %.1f" % (k, v) for k, v in c["contraste"].items())
            nota = "ok" if c["funciona"] else ("tom sobre tom" if c["tom_sobre_tom"] else "fraco")
            print("  camiseta %-9s %-14s %s" % (nome, nota, pares))
        for p in r["problemas"]:
            print("%-5s %s" % (p["nivel"], p["msg"]))
        erros = sum(p["nivel"] == "ERRO" for p in r["problemas"])
        print("Pronta para a gráfica." if not erros else "%d erro(s): corrija antes do mockup." % erros)
    return 1 if any(p["nivel"] == "ERRO" for p in r["problemas"]) else 0


if __name__ == "__main__":
    sys.exit(main())
