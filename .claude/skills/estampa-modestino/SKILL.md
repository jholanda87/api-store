---
name: estampa-modestino
description: "Use quando Jorge falar de camiseta estampada, blusa estampada, estampa, arte para camiseta, coleção nova, drop, Cavalheiro na roupa ou \"em que pé estão as estampas\" da Modestino: dá as regras da linha Estampada, mostra a etapa de cada estampa e chama a próxima habilidade (conceito, arte, mockup, produção)."
---

# Linha Estampada da Modestino (o maestro)

Decisão do Jorge em 30/10/2026: as 3 cores lisas sozinhas dão poucas opções ao cliente. A Modestino passa a ter **duas linhas**:

- **Básica:** lisa, só o nome MODESTINO pequeno na nuca por dentro. Não muda.
- **Estampada:** camisetas com arte **autêntica, minimalista e autoral**. Aqui o **Cavalheiro pode ir na roupa**.

Registre a decisão na Central (seção 10), se ainda não estiver lá. As habilidades do Claude.ai que ainda dizem "nunca na roupa" (criar-conteudo, roteiro-reels, site-impecavel) têm a versão nova em `loja/instalar/atualizar-no-claude-ai/`.

## As regras da Estampada

1. **Autoral.** Toda arte nasce aqui: do desenho do Cavalheiro, de um desenho ou foto do Jorge, de geometria construída do zero ou de uma palavra nossa em curvas. Nunca decalcar, nunca "inspirado" em uma estampa que já existe, nunca clip-art, banco de imagem nem fonte sem licença comercial. Imagem de IA não vira arte de estampa.
2. **Minimalista.** Uma ideia, um gesto. No máximo 2 tintas (o tecido conta como a terceira cor). Sem degradê, sombra ou contorno decorativo. Se dá para tirar um elemento e a ideia continua de pé, tire.
3. **Autêntica.** Tem que ser da Modestino: postura, Fortaleza, o cotidiano de quem usa básico. Sem frase motivacional genérica, sem inglês de enfeite, sem tendência copiada.
4. **Pequeno no peito, grande na caixa** (guia de identidade). A marca aparece pouco. Arte grande só nas costas, e só quando a ideia pede.
5. **Cores da casa.** Camisetas: preto, mapple, off-white. Tintas da paleta: linho #ECE7DE, areia #CBBFAE, carvão #22201D, mapple #5B3F30, grafite #6E675F.
6. **Nada de outra marca** (`loja/marca.json`), nem a identidade antiga (terracota, Poppins).

## O Cavalheiro na roupa

Vetores oficiais em `estampas/marca/` (tirados do desenho original no guia `Modestino — O Cavalheiro.pdf`, no Drive, em "logo oficial"), em carvão e em linho:

| versão | arquivo | onde | tamanho |
| --- | --- | --- | --- |
| figura inteira | `cavalheiro-figura-*.svg` | frente (com o nome embaixo), costas | 7 cm ou mais de altura |
| busto | `cavalheiro-busto-*.svg` | peito | 4 a 6 cm de altura |
| cartola | `cavalheiro-cartola-*.svg` | nuca por fora, gola, manga, bordado | a partir de 1 cm |
| nome | MODESTINO em Instrument Sans 600, espaçado 0.32 (`curvas.py`) | com a figura ou embaixo da cartola nas costas | — |

Não se redesenha, não se distorce, não se espelha, não se troca o traço. Pode mudar a tinta (carvão ou linho, conforme a camiseta) e o tamanho. Ele pode ser **parte** de uma arte autoral (o Cavalheiro numa cena de Fortaleza, por exemplo), desde que continue inteiro e reconhecível.

**Coleção 01** (já desenhada no guia de identidade, página 2):

| camiseta | estampa | técnica e tamanho |
| --- | --- | --- |
| Preto | busto no peito | DTF linho, 5 cm de altura |
| Off White | figura e nome na frente | DTF carvão, 7 cm de altura |
| Mapple Brown | cartola + MODESTINO nas costas, junto da gola | cartola 2 cm |

## Frente e costas

Toda estampa diz o lugar: `peito`, `frente`, `costas` ou `nuca`. Combinações que funcionam: peito pequeno + costas grande (a costas conta a história e o peito assina); só nuca (a mais discreta); só frente. Nas fotos e mockups, mostre sempre os dois lados quando houver arte nas costas.

## A ordem

```
conceito → arte → mockup (fotos das blusas) → aprovação do Jorge → produção (amostra) → catálogo e conteúdo
```

| etapa | habilidade | sai |
| --- | --- | --- |
| 1 | estampa-conceito-modestino | `estampas/EST-NN-nome/conceito.md` com até 3 direções |
| 2 | estampa-arte-modestino | `arte.svg` (vetor, tamanho real) com a checagem limpa |
| 3 | estampa-mockup-modestino | a estampa aplicada nas fotos das blusas (frente e costas) e o mockup plano |
| 4 | estampa-producao-modestino | fotolitos, ficha técnica, pedido de amostra, teste de lavagem |
| 5 | catalogo-modestino + criar-conteudo-modestino | produto `MOD-EST-NN-<COR>-<TAM>` e o lançamento |

Cada estampa tem uma pasta `estampas/EST-NN-nome/` e uma linha em `estampas/estado.md` (código, nome, posição, cores, etapa, próximo passo). Atualize ao fim de cada etapa.

## Os portões

- **Nada vai para a gráfica sem o ok do Jorge no mockup,** e nada vai para a vitrine sem a amostra física aprovada e lavada.
- **Vitrine com foto real da peça estampada.** As fotos de blusa feitas no fal.ai e os mockups servem para aprovar a arte, testar interesse (enquete, story, pré-venda) e briefar o fotógrafo, sempre como "prévia". Não vendem a peça como se fossem foto dela.
- **Preço da Estampada:** só o Jorge decide, na Central. Até lá, catálogo e anúncio ficam em espera.
- **No máximo 3 opções por decisão,** com uma recomendada.

## Como responder

Curto, em português, tom de diretor de arte. Diga em que etapa cada estampa está, o que a próxima entrega e o que falta do Jorge (no máximo 3 itens).

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), os vetores do Cavalheiro vêm na pasta `marca/`, ao lado deste SKILL.md: troque `estampas/marca/` por ela. O estado das estampas fica num doc do Drive (pasta MODESTINO) com a mesma tabela.
