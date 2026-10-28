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
| `vitrine/` | fotos padronizadas para loja, catálogo e story (`foto.py`) |

## Ferramentas (em `.claude/skills/estudio-criativo-modestino/`)

```bash
# artes (carrossel, story, capa, textos de vídeo) a partir de um JSON
node .claude/skills/estudio-criativo-modestino/arte.js loja/estudio/lotes/2026-11-02/carrossel.json
# Reel de cortes (9:16, cor da marca, textos, fechamento com o Cavalheiro)
python3 .claude/skills/estudio-criativo-modestino/reel.py loja/estudio/lotes/2026-11-02/reel.json
# fotos da vitrine (produto 4:5, catálogo 1:1, story 9:16)
python3 .claude/skills/estudio-criativo-modestino/foto.py loja/estudio/entrada/*.jpg --foco 0.5,0.4
# links rastreados para cada canal
python3 .claude/skills/estudio-criativo-modestino/utm.py lote01 --peca carrossel --destino /products/kit-3-camisetas-basicas-modestino
```

No JSON de arte, `*palavra*` vira destaque com fundo areia; foto que ainda não existe aparece como espaço reservado `[FOTO: …]`, para revisar o modelo antes da sessão de fotos.
