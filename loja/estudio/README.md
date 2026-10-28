# Estúdio criativo da Modestino

Etapa 13 da máquina de vendas: artes, comunicação visual, carrosséis, stories, Reels, edição de foto e vídeo e fotos da vitrine. O objetivo é levar gente nova do Instagram e do WhatsApp até a loja e transformar isso em venda. Habilidade: `estudio-criativo-modestino` (em `.claude/skills/`).

| arquivo | para quê |
| --- | --- |
| `estrategia.md` | diagnóstico com os números reais, funil, pilares, ritmo, caminho até a loja, metas |
| `padroes.md` | sistema visual, formatos, tipografia, cor, briefing de foto e vídeo, vitrine, checklist |
| `referencias.md` | o que os especialistas ensinam e como vira regra aqui (com fontes) |
| `calendario.md` | semana modelo, pautas das 2 primeiras semanas, registro e vencedores |
| `modelos/` | JSONs prontos para `arte.js` (carrossel, story, capa, textos de Reel, destaques) e para `reel.py` |
| `lotes/AAAA-MM-DD/` | cada lote: um JSON por peça e as saídas geradas |
| `entrada/` | material bruto (fotos e vídeos), fora do Git |
| `vitrine/` | recortes, efeitos e saídas de IA (`recorte.py`, `efeitos.py`, `ia.py`), fora do Git |

## Ferramentas (em `.claude/skills/estudio-criativo-modestino/`)

```bash
# artes (carrossel, story, capa, textos de vídeo) a partir de um JSON
node .claude/skills/estudio-criativo-modestino/arte.js loja/estudio/lotes/2026-11-02/carrossel.json
# Reel de cortes (9:16, cor da marca, textos, fechamento com o Cavalheiro)
python3 .claude/skills/estudio-criativo-modestino/reel.py loja/estudio/lotes/2026-11-02/reel.json
# peça sem fundo com IA local gratuita (loja 4:5, feed, catálogo 1:1, story 9:16 e PNG transparente)
python3 .claude/skills/estudio-criativo-modestino/recorte.py loja/estudio/entrada/*.jpg --fundo linho
# efeitos sem custo: peça flutuando, troca de cor no ritmo, zoom até a gola
python3 .claude/skills/estudio-criativo-modestino/efeitos.py flutuar loja/estudio/vitrine/<foto>-recorte.png
# IA paga por uso (fal.ai, chave FAL_KEY): manequim invisível, passar, cenário; vídeo 360°, vestir, esticar, cair
python3 .claude/skills/estudio-criativo-modestino/ia.py imagem manequim loja/estudio/entrada/<foto>.jpg
python3 .claude/skills/estudio-criativo-modestino/ia.py video giro360 loja/estudio/vitrine/ia/<foto>-manequim.png
# fotos da vitrine só cortadas e com cor (sem tirar fundo)
python3 .claude/skills/estudio-criativo-modestino/foto.py loja/estudio/entrada/*.jpg --foco 0.5,0.4
# links rastreados para cada canal
python3 .claude/skills/estudio-criativo-modestino/utm.py lote01 --peca carrossel --destino /products/kit-3-camisetas-basicas-modestino
```

No JSON de arte, `*palavra*` vira destaque com fundo areia; foto que ainda não existe aparece como espaço reservado `[FOTO: …]`, para revisar o modelo antes da sessão de fotos.
