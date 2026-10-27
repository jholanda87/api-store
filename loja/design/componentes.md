# Componentes da loja Modestino

Etapa 4 (`loja-design-modestino`), 27/10/2026. Valores só de `tokens.json` (via `tokens.css`). Amostra viva: `design/amostra.html`; prints em `design/prints/` (1440 e 390 px, sem rolagem lateral, sem erro no console).

```
Faixa de confiança
  conteúdo   entrega rápida em Fortaleza · troca em até 30 dias, em mãos · Pix ou cartão em até 3x
  tokens     bg surface-dark, texto text-on-dark, ícone text-muted-on-dark, texto sm
  a11y       região com rótulo "Vantagens"; ícones aria-hidden
  usado em   todas as telas (topo)

Cabeçalho
  conteúdo   O Cavalheiro (busto, 32×40) + MODESTINO (Instrument Sans 600, 0,32em) · menu · carrinho com contagem
  celular    menu some abaixo de 860 px (vira gaveta na construção)
  pendente   arquivo do Cavalheiro em SVG (hoje um espaço reservado)

Galeria
  fotos      só reais: frente vestida (principal), gola de perto, costas; tecido e dobrada na construção
  troca cor  o fundo e as fotos acompanham a cor escolhida (movimento único: 320ms, ease-out)

Seletor de cor
  tamanho    44 px, círculo; selecionado com anel carvão 2px
  a11y       radio com legenda "Cor: <nome>"

Seletor de tamanho
  variantes  disponível · últimas peças (≤ 2, aviso embaixo) · esgotado (riscado, borda tracejada, desabilitado + "Avise-me")
  tamanho    56×44 mínimo; medida embaixo em Geist Mono
  estados    padrão, hover surface, foco anel accent, selecionado surface-dark/text-on-dark
  a11y       grupo de radio com legenda

Calculadora de tamanho
  entrada    largura de axila a axila de uma camiseta do cliente
  resultado  tamanho mais próximo da tabela (P 51 · M 54 · G 57 · GG 60) e seleciona sozinho
  erro       fora de 45–66 cm: "Meça deitada, de axila a axila. A tabela vai de 51 a 60 cm."
  a11y       aria-live, aria-invalid no erro

Botão
  primário   carvão, texto linho, hover mapple, 48 px, largura total na página de produto
  secundário contorno carvão; fantasma sublinhado
  desabil.   "Escolha o tamanho" até escolher (aria-disabled, leva o foco para o tamanho)

Frete por CEP
  regra      8 números; faixa de Fortaleza 60000–61599 A CONFIRMAR com a tabela dos Correios
  valores    [PLACEHOLDER] até definir a taxa local (arquitetura, item 4)

Preço
  fonte      Geist Mono, números tabulares; parcelamento menor ao lado

Card de kit
  conteúdo   nome · cores · preço · preço por peça · ação
  destaque   Kit 3 em carvão (é o kit das promoções, Central seção 3)

Mensagens de estado
  cupom no kit   "O cupom de embaixador vale na peça avulsa. No kit você já paga menos por peça."
  carrinho vazio "Seu carrinho está vazio. Comece pela cor."
  esgotado       "Avise-me quando voltar"

Rodapé
  conteúdo   MODESTINO · políticas · razão social e CNPJ [PLACEHOLDER até o MEI]
  tokens     surface-deep, text-on-dark
```

Contraste: 13 de 13 pares AA (`contrast.py`). Fontes: Instrument Serif, Instrument Sans e Geist Mono, licença OFL (em `design/fonts/`).
