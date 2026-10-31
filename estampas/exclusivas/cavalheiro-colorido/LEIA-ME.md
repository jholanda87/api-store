# Exclusivas · O Cavalheiro colorido (31/10/2026)

O desenho oficial do Cavalheiro (figura inteira, do guia de identidade), sem redesenhar, nas costas com
35 cm de altura (12,4 cm de largura), topo 11 cm abaixo da gola, preenchido por áreas com a paleta de cada tecido:

| camiseta | traço | fraque (fria) | colete, rosto, mão (quente) | calça, cartola, sapatos |
| --- | --- | --- | --- | --- |
| preta | linho #ECE7DE | sálvia #8E9B7A | ocre #C9A25E | tecido (vazado) |
| mapple | linho #ECE7DE | azul-mar #9FB4B3 | areia dourada #D8B878 | tecido |
| off-white | carvão #22201D | oliva #6B7350 | mapple #5B3F30 | tecido |

3 tintas por camiseta (serigrafia, uma tela por tinta: `<g id="tinta-...">` no SVG) ou DTF.
Traço com mínimo de 0,8 mm. Gerado por `colorir.py` a partir da página 1 do guia (pdfimages).

Versão com volume (`--volume`, pedida em 31/10): luz de cima à esquerda em pontilhismo de 0,8 mm.
Na preta e na mapple a sombra é o tecido aparecendo e a luz são pontos de linho; na off-white a sombra
são pontos de carvão e a luz é o tecido. Continua com 3 tintas: `cavalheiro-colorido-volume-*.svg`.

## Versão 2 (31/10): traço limpo e cores vivas
Pedido do Jorge: "traços melhorados, como um desenho mas não feito à mão" e "cores mais vivas".
- Traço refeito pela linha central do desenho original (`--limpo`): espessura constante de 1,2 mm,
  rebarbas da caneta removidas, curvas suavizadas. Pose, proporções e detalhes no mesmo lugar.
- Paleta viva (`--vivo`): preta linho/ouro #E3A833/verde #5FA05A; mapple linho/amarelo-sol #F2C24E/
  azul-céu #7EC0D6; off-white carvão/castanho #8A4518/verde-mata #3F7A3A (contraste 4,2:1 ou mais).
- Volume em pontilhismo mantido. Arquivos: `cavalheiro-colorido-v2-volume-*.svg`, 3 tintas.
