#!/usr/bin/env python3
"""Estoque disponível da Modestino, a partir do Painel. Só biblioteca padrão.

Lê o data/state.json do Painel da Modestino (lotes, vendas e saídas sem venda)
e calcula quanto há de cada cor e tamanho. Serve para conferir o estoque antes
de publicar na loja, para gerar a planilha de estoque da loja virtual e para
avisar quando é hora de pedir lote novo.

    python3 estoque.py state.json
    python3 estoque.py state.json --csv loja/estoque.csv      # para importar na loja
    python3 estoque.py state.json --json

Regras (as mesmas do Painel e da Central):

- disponível = lotes - linhas de vendas - linhas de saídas (brinde, defeito,
  uso, extravio). Encomendas (`custom: true`) e vendas sem `lines` não saem
  do estoque da coleção.
- gatilho de reposição: 50 peças no total (seção 3 da Central).
- variante com 0 peça fica "esgotada" e não pode aparecer como disponível na
  loja; com 1 ou 2 peças, "últimas peças".

Código de saída 1 se algum número ficar negativo (venda lançada sem estoque:
é pergunta para o Jorge, nunca ajuste silencioso).
"""

import argparse
import csv
import json
import sys

COLORS = {"preta": "Preto", "marrom": "Mapple Brown", "off": "Off White"}
SIZES = ["P", "M", "G", "GG"]
REORDER_AT = 50
LOW = 2


def compute(state):
    stock = {}
    for lot in (state.get("stock") or {}).get("lots", []):
        for color, sizes in (lot.get("qty") or {}).items():
            for size, n in sizes.items():
                stock[(color, size)] = stock.get((color, size), 0) + int(n)
    out_sales, out_moves = {}, {}
    for sale in state.get("sales", []):
        if sale.get("custom"):
            continue
        for ln in sale.get("lines") or []:
            k = (ln["color"], ln["size"])
            out_sales[k] = out_sales.get(k, 0) + int(ln.get("qty", 0))
    for mv in state.get("moves", []):
        for ln in mv.get("lines") or []:
            k = (ln["color"], ln["size"])
            out_moves[k] = out_moves.get(k, 0) + int(ln.get("qty", 0))
    keys = sorted(set(stock) | set(out_sales) | set(out_moves),
                  key=lambda k: (list(COLORS).index(k[0]) if k[0] in COLORS else 99,
                                 SIZES.index(k[1]) if k[1] in SIZES else 99))
    rows = []
    for k in keys:
        start = stock.get(k, 0)
        sold = out_sales.get(k, 0)
        moved = out_moves.get(k, 0)
        avail = start - sold - moved
        status = ("negativo" if avail < 0 else "esgotada" if avail == 0
                  else "últimas peças" if avail <= LOW else "ok")
        rows.append({"color": k[0], "color_name": COLORS.get(k[0], k[0]), "size": k[1],
                     "start": start, "sold": sold, "moves": moved,
                     "available": avail, "status": status})
    total = sum(max(r["available"], 0) for r in rows)
    return {"rows": rows, "total": total, "reorder": total <= REORDER_AT,
            "negative": [r for r in rows if r["available"] < 0]}


def render(result):
    out = ["%-13s %-3s %6s %6s %6s %6s  %s" % ("cor", "tam", "lote", "venda",
                                                "saída", "disp.", "situação")]
    for r in result["rows"]:
        out.append("%-13s %-3s %6d %6d %6d %6d  %s" % (
            r["color_name"], r["size"], r["start"], r["sold"], r["moves"],
            r["available"], r["status"]))
    out.append("")
    out.append("Total disponível: %d peças." % result["total"])
    if result["reorder"]:
        out.append("REPOSIÇÃO: chegou a %d peças ou menos. Pedir o lote novo (Lucas)."
                   % REORDER_AT)
    for r in result["negative"]:
        out.append("ERRO: %s %s ficou negativo (%d). Conferir lançamentos com o Jorge."
                   % (r["color_name"], r["size"], r["available"]))
    return "\n".join(out)


def write_csv(result, path, product="Camiseta Básica Modestino"):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["produto", "cor", "tamanho", "sku", "disponivel"])
        for r in result["rows"]:
            sku = "MOD-CAM-%s-%s" % (r["color"].upper(), r["size"])
            w.writerow([product, r["color_name"], r["size"], sku, max(r["available"], 0)])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("state", help="data/state.json do Painel")
    ap.add_argument("--csv", help="grava a planilha de estoque por variante")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        with open(args.state, encoding="utf-8") as fh:
            state = json.load(fh)
    except (OSError, ValueError) as exc:
        print("estoque: %s" % exc, file=sys.stderr)
        return 2
    result = compute(state)
    if args.csv:
        write_csv(result, args.csv)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render(result))
    return 1 if result["negative"] else 0


if __name__ == "__main__":
    sys.exit(main())
