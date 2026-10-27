---
name: loja-paridade-modestino
description: "Use quando Jorge perguntar se a loja virtual da Modestino está pronta, o quanto ela está perto das lojas de referência, o que falta construir, ou pedir uma nota da loja: calcula a paridade de recursos, compara a estrutura das telas e dá o veredito."
---

# Paridade da loja (Replica adaptada)

Versão Modestino do `replica-diff`. Duas ferramentas da Replica, sem instalar nada:

```bash
python3 .claude/skills/replica-diff/parity.py loja/features.csv
python3 .claude/skills/replica-diff/imgdiff.py loja/screens/S03.png loja/clone-screens/S03.png --out loja/diffs/S03.png
python3 .claude/skills/replica-diff/imgdiff.py a.png b.png --json > loja/diffs/S03.json
python3 .claude/skills/replica-diff/parity.py loja/features.csv --visual loja/diffs/*.json --markdown > loja/paridade.md
```

## O que paridade quer dizer aqui

**Fazer o mesmo trabalho, não ter a mesma cara.** A nota de recursos é a que importa: o cliente consegue fazer tudo que faria numa loja grande? A nota de estrutura vê se a informação está nos lugares que o cliente espera (preço, tamanho, frete, troca na primeira dobra) e ignora cor de propósito, porque a cor é da Modestino. Não persiga o pixel das referências: o visual delas é delas.

## Passo 1: recursos

`features.csv` em dia: cada linha com `clone` = `yes`, `partial` (com nota), `no` ou `skip` (com motivo). Rode `parity.py`. Peso: must 3, should 2, could 1; partial vale metade; `skip` e os diferenciais (`original = no`) ficam fora da nota. Faltando `must`, não está pronta. Em 27/10/2026: 0 de 21 obrigatórios.

## Passo 2: estrutura

Prints no mesmo tamanho (1440×900 e 390×844) e no mesmo estado (mesmo produto, mesmo passo). `imgdiff.py` compara onde as coisas estão (90+ igual, 75+ perto, 50+ em parte) e aponta as regiões diferentes.

## Passo 3: comportamento

Ande cada fluxo nas duas lojas e compare: cliques até pagar, o que acontece no erro, o que chega por e-mail/WhatsApp, prazo de entrega em Fortaleza, como pedir troca. Menos cliques que a referência é vitória. Formato: fluxo, referência faz, Modestino faz, corrigir ou manter.

## Passo 4: veredito em `loja/paridade.md`

- **não está pronta:** falta `must` ou há S1 aberto;
- **pronta:** todos os `must`, nota de recursos 80+, sem S1/S2 aberto;
- **melhor que as referências:** pronta + as correções de `correcoes.md` no ar. Esta é a meta. Cópia pura não tem motivo para existir.

Números honestos: 62% é 62%.

## Saída

`loja/paridade.md`, as imagens de diferença e as 5 próximas coisas a construir. Depois, `loja-build-modestino` para as lacunas ou `loja-marca-modestino` se a paridade chegou.

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), as ferramentas citadas acima vêm dentro da própria pasta desta habilidade, ao lado deste SKILL.md: troque `.claude/skills/<pasta>/` pelo caminho desta pasta. Sem Python disponível, siga o método à mão; ele funciona igual.
