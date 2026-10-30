---
name: estampa-producao-modestino
description: "Use quando Jorge pedir para mandar a estampa para a gráfica, escolher entre silk, DTF ou bordado, fazer fotolito, ficha técnica, orçamento, amostra, piloto ou teste de lavagem de uma camiseta estampada da Modestino: prepara os arquivos finais e o pedido, e só libera a tiragem com a amostra aprovada."
---

# Produção da estampa (da tela para a camiseta)

Quarta etapa da linha Estampada. Entra a arte aprovada no mockup (`estampa-mockup-modestino`); sai a pasta `estampas/EST-NN-nome/producao/` pronta para a gráfica, a amostra e a liberação da tiragem. Regras da linha em `estampa-modestino`.

Ferramentas (na pasta `estampa-arte-modestino`):

```bash
python3 .claude/skills/estampa-arte-modestino/estampa.py arte.svg --tecnica silk --posicao costas
python3 .claude/skills/estampa-arte-modestino/separar.py arte.svg estampas/EST-NN-nome/producao/fotolitos [--base-branca] [--vazado "#1E1D1C"]
node    .claude/skills/estampa-arte-modestino/exportar.mjs arte.svg estampas/EST-NN-nome/producao/arte.pdf
node    .claude/skills/estampa-arte-modestino/exportar.mjs arte.svg estampas/EST-NN-nome/producao/arte-300dpi.png --dpi 300
```

`separar.py` faz um fotolito por tinta (preto = imprime, branco = não imprime, com marcas de registro e o nome da tinta), a base branca quando pedida e `separacoes.md` com a ordem.

## Qual técnica

| técnica | quando | cuidado |
| --- | --- | --- |
| **DTF** | tiragens pequenas (a partir de 1 peça), arte com detalhe fino como o traço do Cavalheiro, várias cores de camiseta. É a da Coleção 01 no guia. | toque de película; peça filme macio ("soft") e teste de lavagem |
| **Silk base d'água** | tiragem a partir de ~30 peças por arte, 1 a 2 tintas, toque quase zero (combina com "segunda pele") | tinta clara na preta e na mapple pede base branca (+1 tela) ou corrosão |
| **Silk corrosão (discharge)** | arte clara em camiseta escura com toque zero | só funciona em fibra que aceita (algodão, alguns modais); a gráfica testa no nosso tecido antes |
| **Bordado** | cartola na nuca, na manga ou no peito, peça mais cara | só formas simples; traço de 1 mm ou mais; a figura inteira não cabe |

Regra prática: **lançamento e teste em DTF** (pouca peça, sem risco de estoque parado); **a que vender bem passa para silk** na reposição.

## Passo a passo

1. **Arquivo final.** Rode `estampa.py` com a técnica escolhida até zero ERRO. Exporte PDF e PNG 300 dpi no tamanho real. Para silk, rode `separar.py` (com `--base-branca` se a checagem avisar).
2. **Ficha técnica** em `producao/ficha.md`, uma por estampa:

   ```
   EST-03 · Horizonte
   Técnica: DTF soft          Posição: peito, lado esquerdo de quem veste
   Tamanho: 9,0 × 5,4 cm (igual do P ao GG)
   Distância: topo da arte 8 cm abaixo da costura da gola; centro 10 cm do meio da peça
   Tintas: areia #CBBFAE (preta, mapple) | carvão #22201D (off-white)
   Camisetas e quantidades: preta P 2 M 4 G 4 GG 2 ...
   Arquivos: arte.pdf, arte-300dpi.png, fotolitos/ (silk)
   Amostra: 1 por cor antes da tiragem
   ```

   Nas costas, a distância conta da costura da gola de trás. Em peças de tamanhos diferentes, a arte é a mesma; só muda se a ficha disser.
3. **Orçamento.** Peça a 2 ou 3 gráficas de Fortaleza que o Jorge ou o Lucas indicarem (não invente nomes nem preços): preço por peça na tiragem, custo de tela ou de setup, prazo, se fazem amostra, se testam no nosso tecido. Monte uma tabela e recomende uma.
4. **Amostra.** Uma peça por cor, estampada no tecido da Modestino. Confira com régua: tamanho, distância da gola, cor da tinta ao lado da paleta impressa, nitidez do traço mais fino.
5. **Teste de lavagem.** 5 lavagens do avesso, água fria, sem secadora. Depois de cada uma: rachadura, descascado, desbotamento, toque. Foto da 1ª e da 5ª. Reprovou, troca a técnica ou a gráfica.
6. **Liberação.** Com a amostra aprovada e o ok do Jorge, a tiragem sai. Grave a decisão (técnica, gráfica, custo por peça) em `estampas/estado.md` e passe o custo para a `financeiro-modestino` (o preço de venda é do Jorge, na Central).
7. **Fotos reais.** A amostra aprovada vai para a foto de produto (`catalogo-modestino`); o lançamento vai para `criar-conteudo-modestino` (o processo do rascunho à camiseta é um bom carrossel).

## Os portões

- Nenhum pedido, pagamento ou contrato sem o ok do Jorge. Claude não fecha com gráfica.
- Nenhuma tiragem sem amostra aprovada e lavada.
- Etiqueta da peça estampada: mesma etiqueta obrigatória da básica (composição, cuidados, CNPJ; `administrativo-modestino`), com cuidado extra: "lavar do avesso, não passar ferro sobre a estampa".

## Como responder

A técnica recomendada com o porquê em uma linha, a lista de arquivos prontos, a ficha técnica e o que falta do Jorge (gráfica, quantidade, ok da amostra).

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), `estampa.py`, `separar.py` e `exportar.mjs` vêm dentro da pasta desta habilidade: troque `.claude/skills/estampa-arte-modestino/` pelo caminho desta pasta. Sem Python ou Node, mande o SVG e a ficha; a gráfica separa as cores.
