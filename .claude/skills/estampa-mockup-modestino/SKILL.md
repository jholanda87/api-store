---
name: estampa-mockup-modestino
description: "Use quando Jorge pedir para ver a estampa na camiseta, aplicar ou anexar a estampa nas fotos das blusas (as feitas no fal.ai ou fotos reais), mostrar frente e costas, montar mockup ou prévia para aprovar, enquete ou pré-venda da Modestino: aplica a arte em escala real nas fotos, no peito, na frente, nas costas ou na nuca."
---

# Mockup: a estampa nas blusas (frente e costas)

Terceira etapa da linha Estampada. Entra `estampas/EST-NN-nome/arte.svg` (já sem ERRO no `estampa.py`); sai a estampa aplicada nas fotos das blusas para o Jorge aprovar. Regras da linha em `estampa-modestino`.

Ferramentas (na pasta `estampa-arte-modestino`):

```bash
# na foto da blusa (fal.ai ou real), em escala real
node .claude/skills/estampa-arte-modestino/aplicar.mjs estampas/fotos-base/preta-frente.png arte.svg saida.png --posicao peito
node .claude/skills/estampa-arte-modestino/aplicar.mjs estampas/fotos-base/preta-costas.png arte.svg saida.png --posicao costas
# mockup plano nas 3 cores, sem foto
python3 .claude/skills/estampa-arte-modestino/mockup.py arte.svg mockup.svg --posicao peito --arte-off-white arte-off-white.svg --png mockup.png
```

## As fotos-base (as blusas do fal.ai)

Ficam em `estampas/fotos-base/`, uma por cor e lado: `preta-frente.png`, `preta-costas.png`, `mapple-frente.png`, `mapple-costas.png`, `offwhite-frente.png`, `offwhite-costas.png` (e variações de pose, se houver). Se não estiverem lá, procure no Google Drive (pasta MODESTINO) ou peça ao Jorge que mande no chat. A melhor foto-base é a da blusa **lisa**, de frente ou de costas, sem cruzar os braços na frente do peito.

**Meça cada foto uma vez** e registre em `estampas/fotos-base/fotos.json`:

```json
{
  "preta-frente.png":  {"gola": [512, 236], "axilas": 640, "lado": "frente", "cor": "preto"},
  "preta-costas.png":  {"gola": [508, 190], "axilas": 652, "lado": "costas", "cor": "preto"}
}
```

- `gola`: o ponto central de baixo da gola, em pixels (na foto de costas, a gola de trás);
- `axilas`: a largura da blusa de uma axila à outra, em pixels. Com isso a escala sai real (tamanho M, 54 cm).

Para medir: abra a foto, ache os dois pontos e confira desenhando uma marca na foto com Pillow; olhe uma vez. Com o `fotos.json` preenchido, o `aplicar.mjs` só precisa da foto, da arte e da posição.

## Posições

| posição | onde fica | uso |
| --- | --- | --- |
| `peito` | topo 8 cm abaixo da gola, 10 cm para o lado esquerdo de quem veste (à direita na foto de frente) | busto do Cavalheiro, assinatura |
| `frente` | centro, topo 8 cm abaixo da gola | figura e nome, arte média |
| `costas` | centro, topo 7 cm abaixo da gola de trás | a arte grande, a história |
| `nuca` | centro, 2,5 cm abaixo da gola de trás | cartola, nome pequeno |

Ajustes: `--lado-peito esquerda` se a foto estiver espelhada; `--giro 3` se a blusa estiver inclinada na foto; `--dobras 0.5` (menos) a `1` (mais) para quanto as dobras do tecido passam por cima da tinta; `--caixa X,Y,LARGURA` para posicionar à mão.

## Passo a passo

1. Confira se a arte tem versão por cor (linho/areia na preta e na mapple, carvão na off-white).
2. Para cada cor aprovada no conceito, aplique na foto de frente e, se a arte for de costas ou tiver costas, na de costas. Peito + costas: rode duas vezes (uma por foto).
3. Monte **uma folha** com tudo (Pillow): frente e costas lado a lado, uma linha por cor, com o rótulo "EST-NN · nome · posição · tamanho em cm". Olhe uma vez, a 100% e de longe.
4. Confira no olho: a escala parece real (5 cm de busto não pode ocupar o peito todo), a arte acompanha a inclinação da blusa, nada encosta na costura da gola ou da manga.
5. Mande a folha para o Jorge escolher. Se aprovada, grave em `estampas/EST-NN-nome/mockups/` e atualize `estampas/estado.md` (etapa "aprovada no mockup").

## Usos e limites

- **Pode:** aprovar a arte, testar interesse (enquete nos stories, "qual cor?"), pré-venda marcada como prévia, briefing do fotógrafo e da gráfica.
- **Não pode:** ir para a vitrine ou anúncio como se fosse foto da peça. A vitrine usa a foto real da amostra estampada (`catalogo-modestino`).
- O Photoroom (virtual try-on) só com o ok do Jorge: gasta créditos.

## Como responder

A folha de mockups e, em uma linha por cor, se a estampa funciona naquela blusa. Pergunte qual vai para a produção. Próxima: `estampa-producao-modestino`.

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), `aplicar.mjs`, `mockup.py`, `estampa.py` e `exportar.mjs` vêm dentro da pasta desta habilidade: troque `.claude/skills/estampa-arte-modestino/` pelo caminho desta pasta. Precisa de Node com Playwright para a foto; sem isso, posicione a arte à mão no Canva ou no Adobe Express com as mesmas medidas da tabela.
