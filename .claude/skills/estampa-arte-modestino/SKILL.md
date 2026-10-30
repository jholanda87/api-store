---
name: estampa-arte-modestino
description: "Use quando Jorge pedir para desenhar, criar, vetorizar ou ajustar a arte de uma estampa da Modestino, colocar o Cavalheiro numa estampa, transformar um rabisco ou foto em vetor, ou conferir se um arquivo de estampa está pronto: desenha em SVG vetorial no tamanho real e checa tintas, traço mínimo e contraste nas 3 camisetas."
---

# Arte da estampa (vetor, tamanho real, pronta para a gráfica)

Segunda etapa da linha Estampada. Entra o `conceito.md` aprovado (`estampa-conceito-modestino`); sai `estampas/EST-NN-nome/arte.svg`. Regras da linha em `estampa-modestino`.

Ferramentas (pasta desta habilidade):

```bash
python3 .claude/skills/estampa-arte-modestino/estampa.py arte.svg --posicao peito --tecnica dtf --marca loja/marca.json
python3 .claude/skills/estampa-arte-modestino/curvas.py fonte.woff "MODESTINO" --altura-mm 4 --espaco 0.32 > nome.svg
python3 .claude/skills/estampa-arte-modestino/vetorizar.py rabisco.jpg traco.svg --altura-mm 60 [--corte x0,y0,x1,y1]
python3 .claude/skills/estampa-arte-modestino/textura.py foto.jpg arte.svg --largura-mm 80 [--modo hachura] [--inverter]
node    .claude/skills/estampa-arte-modestino/exportar.mjs arte.svg arte.png --dpi 300   # ou arte.pdf
```

- `estampa.py` lê o tamanho real, conta as tintas, mede o traço mais fino em mm, acusa degradê, transparência, bitmap, texto que não virou curva e nome de outra marca, e dá o contraste de cada tinta no preto, no mapple e no off-white (avisa quando precisa de base branca). Sai com erro se algo impede a impressão.
- `curvas.py` transforma palavra em vetor com as fontes da marca (OFL, uso comercial livre): `npm i @fontsource/instrument-serif @fontsource/instrument-sans @fontsource/geist-mono` e `pip install fonttools brotli`.
- `vetorizar.py` passa o traço à mão (Cavalheiro, rabisco do Jorge) para vetor sem redesenhar: `pip install pillow potracer`. Sem Python, o conector Adobe (`image_vectorize`) faz o mesmo.
- `textura.py` faz **pontilhismo** (pontos do mesmo tamanho, mais juntos na sombra) ou **hachura** (traços cruzados com tremor de mão) a partir de uma imagem com luz e sombra. Desenho só de linha não serve: vira pontos soltos. `--inverter` para tinta clara em camiseta escura (os pontos vão na luz, não na sombra). Ponto de 0,6 mm (DTF) a 0,8 mm (silk).
- `exportar.mjs` gera PNG 300 dpi ou PDF no tamanho real (Node + Playwright).

## As técnicas da casa (comece por aqui)

Leia "A linguagem da Modestino" em `estampa-modestino`. A ordem de preferência da fonte:

1. **Desenho do Jorge no papel** (caneta nanquim, lápis, linogravura carimbada): foto de cima, com luz uniforme, e `vetorizar.py`. É a mais autoral; o tremor da mão fica.
2. **Foto do Jorge** (um caju da feira, a jangada na Beira-Mar, um mandacaru): recorte o assunto, fundo liso, e `textura.py` (pontilhismo ou hachura). Junte um contorno se a silhueta se perder.
3. **Desenho construído aqui** (como `estampas/EST-09-caju/gerar.py`): a forma em pontos de controle, o volume em degradê só para gerar os tons, o `textura.py` vira pontos, e o contorno ganha tremor de caneta. Bom para testar a ideia; o desenho final, se possível, volta para a mão.

Em todas: um assunto, 1 tinta, versão clara (pontos na luz) e versão escura (pontos na sombra), e o tecido aparecendo.

## Como desenhar

1. **Comece pelo tamanho físico.** Raiz do SVG com `width`/`height` em mm e `viewBox` em mm (1 unidade = 1 mm). Maior lado: peito 40 a 120 mm (o busto do guia tem 50 de altura; a figura aprovada, 100), frente 70 a 280, costas 100 a 320, nuca 10 a 80.
2. **Grade.** Monte sobre uma grade de 1 mm e um módulo (por exemplo 6 mm). Alinhe as formas ao módulo; meça espaços em múltiplos dele. Isso é o que faz o mínimo parecer pensado, e não vazio.
3. **Formas, não efeitos.** `path`, `rect`, `circle`, `line` com `fill`/`stroke` direto no elemento (#RRGGBB). Nada de `filter`, gradiente, `opacity`, imagem embutida ou classe CSS.
4. **Traço mínimo:** silk 0,5 mm, DTF 0,3 mm, bordado 1 mm. Detalhes (pontos, vãos) a partir de 0,8 mm no silk. Traço uniforme combina com o desenho do Cavalheiro.
5. **No máximo 2 tintas.** O tecido é a terceira cor: um vazado que deixa a camiseta aparecer conta como cor e não custa tela (`--vazado` na checagem).
6. **Texto sempre em curvas** (`curvas.py`) e em português. Nome MODESTINO: Instrument Sans 600, espaçamento 0.32. Frase: Instrument Serif, itálico na ênfase.
7. **Cavalheiro:** importe o vetor oficial de `estampas/marca/` (carvão para off-white, linho para preto e mapple) como `<g>` com `transform` de escala e posição. Escala proporcional, sem girar nem espelhar, sem editar os nós.
8. **Uma versão por camiseta, se precisar:** a mesma arte em areia/linho para preto e mapple e em carvão para off-white (`arte-off-white.svg`).

Esqueleto:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="90mm" height="54mm" viewBox="0 0 90 54">
  <title>EST-03 Horizonte · peito · DTF areia</title>
  <path fill="#CBBFAE" d="M23 30 A22 22 0 0 1 67 30 Z"/>
  <g fill="none" stroke="#CBBFAE" stroke-width="2"><path d="M0 35 H90"/></g>
</svg>
```

O arquivo `exemplo.svg` desta pasta é esse exemplo completo (e `exemplo-off-white.svg`, a versão em carvão).

## Passo a passo

1. Leia o `conceito.md`. Desenhe 3 variações de peso (mais leve, a do conceito, mais forte), lado a lado.
2. Rode `estampa.py` em cada uma até zero ERRO. Leia os AVISOS: "tom sobre tom" pode ser a ideia; "base branca" vai para a produção.
3. Renderize e olhe uma vez **no tamanho real** (`exportar.mjs` a 300 dpi, ver a 100%) e de longe (miniatura de 200 px): a ideia tem que ler nos dois.
4. Mande para o mockup (`estampa-mockup-modestino`) e só depois para o Jorge escolher.
5. Grave a escolhida como `estampas/EST-NN-nome/arte.svg` (+ `arte-off-white.svg` se tiver) e atualize `estampas/estado.md` (etapa "arte").

## Como responder

As 3 variações numa imagem só, a saída do `estampa.py` da recomendada (tamanho, tintas, onde funciona) em 3 linhas, e a pergunta de qual vai para o mockup.

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), as ferramentas citadas acima vêm dentro da própria pasta desta habilidade, ao lado deste SKILL.md: troque `.claude/skills/<pasta>/` pelo caminho desta pasta. Os vetores do Cavalheiro também vêm junto, na pasta `marca/`. Sem Python ou Node, siga o método à mão; ele funciona igual.
