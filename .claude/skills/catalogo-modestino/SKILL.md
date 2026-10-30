---
name: catalogo-modestino
description: "Use quando Jorge pedir para cadastrar produto, kit, cor, tamanho, foto, descrição ou atualizar o estoque da loja virtual da Modestino (ou do catálogo do Instagram/WhatsApp): monta o catálogo a partir do Painel e das fotos reais, no tom da marca."
---

# Catálogo e estoque da loja (a entrada da máquina)

O que entra na loja: produto, variante, foto, texto e estoque. Fonte dos números: o Painel da Modestino (`data/state.json`). Fonte das regras: a Central (seção 3) e `criar-conteudo-modestino`.

Ferramenta:

```bash
python3 .claude/skills/catalogo-modestino/estoque.py state.json                    # conferir
python3 .claude/skills/catalogo-modestino/estoque.py state.json --csv loja/estoque.csv
```

Ela calcula o disponível por cor e tamanho (lotes − vendas − brindes/defeitos/uso/extravio; encomendas não contam), marca "últimas peças" (≤ 2) e "esgotada", avisa a reposição em 50 peças e sai com erro se algo ficar negativo. Em 27/10/2026: 212 peças, nenhuma variante esgotada.

## Passo a passo

1. **Leia o Painel** com o Artifact tool (`action: read`, url do Painel, `path: data/state.json`) e rode `estoque.py`. Número negativo é pergunta para o Jorge, nunca ajuste.
2. **Produtos e variantes** como em `loja/arquitetura.md`: Camiseta Básica (3 cores × P–GG, SKU `MOD-CAM-<COR>-<TAM>`), Kit 2, Kit 3, Kit Essencial, e a linha **Estampada**: um produto por estampa aprovada em `estampas/estado.md` (SKU `MOD-EST-<NN>-<COR>-<TAM>`, só nas cores em que a arte foi aprovada). Preço da tabela da Central; a Estampada só entra depois que o Jorge fechar o preço dela lá.
3. **Fotos.** Só reais: frames dos vídeos do Keanu (`claude/mapa-takes-keanu.md`), golas com etiqueta, ecobag. Nunca `2_preta_vestida` nem `4_espelho_preta`. Com o conector Photoroom: fundo linho ou carvão liso, sombra suave, recorte; **nunca** trocar a peça, a cor ou o caimento (o Photoroom gasta créditos do Jorge: confirmar antes de rodar em muitas fotos). Ordem por variante: frente vestida, costas, gola de perto, tecido de perto, peça dobrada.
4. **Texto do produto,** no tom da marca:
   - abre pela sensação e pelo uso, não pela ficha técnica;
   - Básica: "lisa, sem logo; só o nome MODESTINO pequeno na nuca por dentro";
   - Estampada: nome e número da estampa, a história em uma ou duas frases (de `estampas/<código>/conceito.md`), técnica ("silk base d'água, toque macio"), posição e tamanho da arte em cm; foto real da peça estampada, nunca o mockup;
   - composição: "vem na etiqueta" (modal é um dos tecidos, não o da marca);
   - um básico para cada ocasião, nunca a mesma peça em sequência;
   - tabela P 51 · M 54 · G 57 · GG 60 cm (axila a axila), tórax 102 · 108 · 114 · 120, e como medir uma camiseta que ele já tem;
   - troca: 7 dias arrependimento, 30 dias tamanho e defeito.
   Revise com `loja-lancamento-modestino/vitrine.py` antes de publicar.
5. **Publicar.** Se a loja for Shopify, use o conector (busque o produto antes, nunca chute id; `create-product`/`update-product`, `set-inventory` com os números do `estoque.py`). Sem conector, entregue a planilha de importação da plataforma. Nada vai ao ar sem o ok do Jorge.
6. **Sincronizar.** A cada venda lançada pela `financeiro-modestino`, rode de novo e atualize a loja no mesmo dia. Peça vendida no Direct sai da loja também.

## Alertas que sempre vão na resposta

- variante com 0 ou ≤ 2 peças (tirar da vitrine ou marcar "últimas");
- total ≤ 50: pedir o lote novo ao Lucas (Filati 1 dia + corte 7 + costura 7 ≈ 20 dias); vendendo mais de 17/semana, antecipar;
- GG costuma acabar primeiro: lote 2 com mais GG e mais preto.

## Como responder

Curto: o que foi cadastrado/atualizado (tabela), estoque por cor e tamanho, alertas, e o que falta (foto, confirmação de preço).

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), as ferramentas citadas acima vêm dentro da própria pasta desta habilidade, ao lado deste SKILL.md: troque `.claude/skills/<pasta>/` pelo caminho desta pasta. Sem Python disponível, siga o método à mão; ele funciona igual.
