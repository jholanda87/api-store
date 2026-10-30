#!/usr/bin/env python3
"""Revisor de anúncios da Modestino. Só biblioteca padrão.

A versão Modestino do listing.py da Replica: em vez de App Store e Google
Play, confere a página de produto da loja e os anúncios de cada canal (SEO,
Mercado Livre, Shopee, Google Shopping, catálogo da Meta, legenda do
Instagram) contra os limites de cada canal E contra as regras da marca que
estão na Central Modestino.

    python3 vitrine.py loja/lancamento/anuncios.json
    python3 vitrine.py anuncios.json --avoid "Insider,Reserva"
    python3 vitrine.py anuncios.json --json

anuncios.json (veja vitrine.exemplo.json):

    {
      "avoid": ["nomes de outras marcas que não podem aparecer"],
      "limites": {"mercado_livre": {"titulo": 60}},      # opcional, sobrescreve
      "anuncios": [
        {"canal": "loja", "sku": "...", "titulo": "...", "descricao": "...",
         "seo_titulo": "...", "seo_descricao": "...", "preco": 80}
      ]
    }

Os limites abaixo são os de out/2026 e mudam: confira no painel do canal na
hora de publicar e, se mudou, sobrescreva em "limites". Código de saída 1 em
qualquer erro; 0 quando só há avisos.
"""

import argparse
import json
import re
import sys
import unicodedata

LIMITS = {
    "loja": {"titulo": 70, "seo_titulo": 70, "seo_descricao": 160, "descricao": 5000},
    "mercado_livre": {"titulo": 60, "descricao": 50000},
    "shopee": {"titulo": 120, "descricao": 3000},
    "google": {"titulo": 150, "descricao": 5000},
    "meta": {"titulo": 200, "descricao": 9999},
    "instagram": {"descricao": 2200},
    "whatsapp": {"titulo": 120, "descricao": 1000},
}
REQUIRED = {"titulo", "descricao"}
# Preços que existem hoje (Central, seção 3, revisão de 19 e 20/10).
PRICES = {80, 75, 70, 160, 150, 225, 210, 195}

# Regras da marca: (nível, padrão, mensagem)
RULES = [
    ("error", r"\b(100\s?% modal|só modal|nosso tecido (é )?(o )?modal|o tecido da modestino é (o )?modal)\b",
     "modal é um dos tecidos, não o tecido da marca. Composição só por peça (vem na etiqueta)."),
    ("error", r"\b(do treino ao (jantar|trabalho|escritório)|sem (precisar )?trocar|a mesma (peça|camiseta) (o dia (todo|inteiro)|do .* ao))",
     "um básico para cada ocasião: nunca sugerir a mesma peça em sequência."),
    ("warn", r"\b(não desbota|nunca desbota|não amassa|nunca amassa|anti.?odor|antibacteriano|proteção uv|fps ?\d+|não deforma nunca|garantia (eterna|vitalícia))\b",
     "promessa técnica: só entra se foi testada. Confirme o teste com o Jorge ou troque pela sensação."),
    ("warn", r"\bstreetwear\b",
     "a Modestino não é streetwear; é básico masculino versátil."),
    ("warn", r"\b(prezado|prezada|caro cliente)\b",
     "tom engessado. A voz é humana e direta."),
    ("warn", r"\b(básica|lisa)\b.{0,40}\b(estampa(da)?|cavalheiro (no|na) (peito|frente|costas))\b",
     "a Básica é lisa; estampa e Cavalheiro na roupa são da linha Estampada. Não misture as duas no mesmo anúncio."),
    ("warn", r"\b(compre (já|agora)|últimas unidades|corre que acaba|só hoje)\b",
     "venda de cara / urgência falsa. Educar antes de vender; escassez só se for real e o estoque confirmar."),
]
CLAIMS = re.compile(r"(\bmelhor (camiseta|marca|do brasil)\b|\bnº ?1\b|#\s?1\b|\bnúmero 1\b|\bimbatível\b)", re.I)
MONEY = re.compile(r"R\$\s?(\d{1,3}(?:\.\d{3})*)(?:,(\d{2}))?")


def length(text):
    text = unicodedata.normalize("NFC", text or "")
    return sum(1 for ch in text if unicodedata.category(ch) not in ("Mn", "Me")
               and ch not in ("‍", "️", "︎"))


def emoji_count(text):
    return sum(1 for ch in text or "" if ord(ch) >= 0x1F000 or unicodedata.category(ch) == "So")


def lint(data, avoid=None):
    issues = []
    limits = {k: dict(v) for k, v in LIMITS.items()}
    for canal, over in (data.get("limites") or {}).items():
        limits.setdefault(canal, {}).update(over)
    avoid = [a.strip() for a in (avoid or data.get("avoid") or []) if a.strip()]

    def add(level, idx, canal, field, msg):
        issues.append({"level": level, "anuncio": idx, "canal": canal,
                       "campo": field, "mensagem": msg})

    ads = data.get("anuncios") or []
    if not ads:
        add("error", "-", "-", "-", "nenhum anúncio em 'anuncios'")
    for i, ad in enumerate(ads, 1):
        canal = ad.get("canal", "")
        if canal not in limits:
            add("error", i, canal or "?", "canal", "canal desconhecido. Use: %s" % ", ".join(limits))
            continue
        for field in sorted(REQUIRED & set(limits[canal])):
            if not (ad.get(field) or "").strip():
                add("error", i, canal, field, "vazio")
        for field, limit in limits[canal].items():
            value = ad.get(field) or ""
            n = length(value)
            if n > limit:
                add("error", i, canal, field, "%d caracteres, o limite é %d (%d a mais)"
                    % (n, limit, n - limit))
        text_fields = {f: ad.get(f) or "" for f in ("titulo", "descricao", "seo_titulo", "seo_descricao")}
        for field, value in text_fields.items():
            if not value:
                continue
            for name in avoid:
                if re.search(r"(?<!\w)%s(?!\w)" % re.escape(name), value, re.I):
                    add("error", i, canal, field,
                        "cita '%s'. Nome de outra marca no anúncio dá denúncia e "
                        "derruba o anúncio. Diga o que a Modestino faz." % name)
            for level, pat, msg in RULES:
                m = re.search(pat, value, re.I)
                if m:
                    add(level, i, canal, field, "'%s': %s" % (m.group(0), msg))
            for m in MONEY.finditer(value):
                v = int(m.group(1).replace(".", ""))
                if v not in PRICES:
                    add("warn", i, canal, field, "R$ %s não é um preço da tabela da Central "
                        "(80, 75/70 sem embalagem, kits 160/150/225, empresa 210/195)." % m.group(1))
        title = ad.get("titulo") or ""
        if title:
            m = CLAIMS.search(title)
            if m:
                add("warn", i, canal, "titulo", "'%s' é afirmação de ranking que a marca não "
                    "consegue provar." % m.group(0))
            if emoji_count(title):
                add("warn", i, canal, "titulo", "emoji no título. Marketplaces recusam e a marca não usa.")
            caps = re.findall(r"\b[A-ZÀ-Ú]{4,}\b", title.replace("MODESTINO", ""))
            if caps:
                add("warn", i, canal, "titulo", "palavra toda em maiúscula: %s" % ", ".join(caps))
        if emoji_count(ad.get("descricao")) > 3:
            add("warn", i, canal, "descricao", "mais de 3 emojis. Sem emoji em excesso.")
        price = ad.get("preco")
        if price is not None and price not in PRICES:
            add("error", i, canal, "preco", "R$ %s fora da tabela da Central. Margem mínima de "
                "50%% depois de taxa e cupom: confira antes." % price)
        if canal in ("mercado_livre", "shopee") and price is not None and price < 80:
            add("warn", i, canal, "preco", "marketplace cobra de 12% a 20%: a Central diz que "
                "só entra quando o preço absorver a taxa.")
    return issues


def render(data, issues):
    out = []
    for i, ad in enumerate(data.get("anuncios") or [], 1):
        canal = ad.get("canal", "?")
        out.append("#%d %s %s" % (i, canal, ad.get("sku", "")))
        for field, limit in (LIMITS.get(canal) or {}).items():
            n = length(ad.get(field) or "")
            out.append("  %-14s %5d / %-5d %s" % (field, n, limit,
                                                  "PASSOU" if n > limit else ("ok" if n else "--")))
    out.append("")
    if not issues:
        out.append("Nenhum problema.")
    for it in issues:
        out.append("%-5s #%s %s.%s: %s" % ("ERRO" if it["level"] == "error" else "AVISO",
                                            it["anuncio"], it["canal"], it["campo"], it["mensagem"]))
    errs = sum(1 for it in issues if it["level"] == "error")
    out.append("")
    out.append("%d erros, %d avisos" % (errs, len(issues) - errs))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("anuncios", help="anuncios.json")
    ap.add_argument("--avoid", help="nomes separados por vírgula que não podem aparecer")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        with open(args.anuncios, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        print("vitrine: %s" % exc, file=sys.stderr)
        return 2
    issues = lint(data, args.avoid.split(",") if args.avoid else None)
    print(json.dumps(issues, ensure_ascii=False, indent=2) if args.json else render(data, issues))
    return 1 if any(it["level"] == "error" for it in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
