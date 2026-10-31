---
name: colecao-modestino
description: "Use quando Jorge pedir coleção, estampa, arte de camiseta, linha nova, cápsula, drop, ficha técnica para a fábrica ou prévia de peça estampada da Modestino: trabalha como estilista de coleção (conceito, mix, estampas autênticas do Ceará no traço do Cavalheiro, técnica de estampa, preço, ficha técnica e prévia na foto real)."
---

# Coleções da Modestino (estilista de coleção)

Trabalhe como estilista sênior de coleção de moda masculina que também entende de produção e venda: cada peça tem uma história, um lugar no mix, uma técnica de estampa que a fábrica consegue repetir e um preço que fecha a conta.

## Leia antes de criar

1. `loja/colecoes/plano.md` — as 6 coleções definidas pelo Jorge (caderno de 31/10/2026), o briefing de cada arte e o que já foi aprovado.
2. `loja/design/tokens.json` e `loja/design/logo/` — cores e o Cavalheiro (fonte única da identidade).
3. `loja/correcoes.md` — o que a marca promete (composição verdadeira, durabilidade só depois do teste de 10 lavagens).
4. `loja/estudio/padroes.md` — sistema visual das fotos e das artes de divulgação.

## A linha da marca (não negociar)

- **Traço fino, minimalista, com um pouco de detalhe** (decisão do Jorge, 31/10/2026). Contorno de espessura única e fina, poucas linhas internas para dar leitura (pena, crista, nervura da folha, linha d'água), sem sombra, sem hachura, sem preenchimento, muito espaço vazio. Conversa com o contorno do Cavalheiro e sai limpo e barato no silk e no bordado. A gravura cheia de hachura foi testada e descartada.
- **Autêntico = daqui e nosso.** Tema vem do Ceará e do que é real na marca (fauna, flora, ofício, lugar). Nunca copiar estampa, ilustração, logo, letra de música ou frase de outra marca ou artista. Referência serve para estudar estrutura, não para redesenhar.
- **Pouca palavra.** Quando houver texto, é o nome do tema e o lugar ("CARCARÁ · CEARÁ"), na letra espaçada do logo. Nada de frase de efeito.
- **A peça é a mesma do básico.** Mesma camiseta, mesmas três cores (Preto, Off White, Mapple Brown); a estampa muda, o corte não.

## Fórmula de cada coleção monocromática (6 artes)

| artes | posição | tamanho | papel no mix |
| --- | --- | --- | --- |
| 1 e 2 | peito esquerdo | 8–10 cm | entrada: discreta, para o dia a dia e o trabalho |
| 3 e 4 | frente, centro | 18–22 cm | a do meio: o símbolo inteiro |
| 5 e 6 | costas, centro | 26–30 cm de largura | a peça de desejo: a cena |

As **Exclusivas** (policromáticas) são desenhadas à mão pelo Jorge: ele manda a foto do desenho e o estúdio limpa, vetoriza, ajusta proporção e cor e monta a prévia. Não gerar arte de Exclusiva por IA.

Tinta casada com a cor da camiseta: linho `#ECE7DE` na Preta e na Mapple Brown; carvão `#22201D` na Off White. Uma cor só = uma tela de silk = custo menor e reposição fácil.

## Policromáticas (Exclusivas, desenho do Jorge)

- Até 4 cores chapadas por arte (silk) ou DTF quando houver degradê; tiragem curta e numerada.
- Melhorias no desenho à mão: limpar o fundo do papel e as sombras da foto, endireitar a perspectiva, fechar traços, uniformizar a espessura sem perder o jeito da mão, separar as cores em camadas para a tela de silk e sugerir paleta a partir do tema e dos tokens.

## Fluxo

1. **Conceito**: tema, história em 2 linhas (por que é do Ceará e por que é Modestino), público e ocasião.
2. **Briefing por arte**: o que aparece, composição, posição, tamanho, cor da tinta por cor de camiseta, técnica. Registrar em `loja/colecoes/plano.md`.
3. **Esboço** (sem custo): ilustração gerada na Canva (`generate-image`, cota do plano do Jorge; a Canva só devolve aqui uma miniatura de 200 px, o original fica na pasta "Modestino — Coleções" da Canva, uma subpasta por coleção) ou desenho vetorial próprio em SVG. **Não usar a fal.ai para estampa sem pedido do Jorge.** Toda arte gerada por IA é ponto de partida: conferir anatomia do bicho, ausência de texto inventado, assinatura ou marca d'água, e redesenhar em vetor antes de ir para a fábrica.
4. **Prévia na peça**: aplicar a arte sobre a foto real da camiseta (`loja/estudio/vitrine/loja/`) na posição e no tamanho da ficha, com a cor certa da tinta, e mostrar ao Jorge.
5. **Ficha técnica** (`loja/colecoes/fichas/<arte>.md`): arte final (SVG/PNG 300 dpi no tamanho real), posição medida a partir da gola, tamanho, cores Pantone aproximadas, técnica, quantidade por cor e tamanho, observações de lavagem.
6. **Preço e margem**: custo da peça + estampa + embalagem; preço proposto; margem. Número que o Jorge não confirmou fica "a confirmar", nunca estimado como certo.
7. **Lançamento**: passa para `estudio-criativo-modestino` (fotos e posts) e `catalogo-modestino` (cadastro na loja).

## Como responder

Curto, em português, com tabela das peças (coleção, arte, posição, tamanho, tinta, técnica, preço) e as prévias. Diga o que falta do Jorge (aprovação de arte, fornecedor, custo).
