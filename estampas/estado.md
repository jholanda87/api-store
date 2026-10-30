# Linha Estampada Modestino: estado

Decisão do Jorge em 30/10/2026: além da Básica (lisa), a Modestino tem a linha Estampada,
com arte autêntica, minimalista e autoral, e o Cavalheiro pode ir na roupa.
Regras e ordem em `.claude/skills/estampa-modestino/SKILL.md`.

- `marca/`: vetores oficiais do Cavalheiro (figura, busto, cartola), em carvão e linho,
  tirados do desenho original (`Modestino — O Cavalheiro.pdf`, Drive › logo oficial).
- `fotos-base/`: fotos das blusas lisas (fal.ai ou reais), frente e costas, e `fotos.json`
  com a gola e a largura de axila a axila de cada foto.
- `EST-NN-nome/`: conceito.md, arte.svg, mockups/, producao/.

| código | nome | posição | camisetas | técnica | etapa | próximo passo |
| --- | --- | --- | --- | --- | --- | --- |
| EST-01 | Busto (Coleção 01) | peito, 5 cm | preta e mapple (linho) | DTF | 🟡 mockup pronto | ok do Jorge |
| EST-02 | Figura | peito, 10 cm | off-white (grafite); preta e mapple (linho) | DTF | 🟢 peça real feita e aprovada (off-white) | levar para preta e mapple? |
| EST-03 | Cartola nas costas (Coleção 01) | nuca por fora, 2 cm, + MODESTINO | mapple (linho) | DTF ou bordado | 🟡 cartola pronta | foto de costas da mapple |
| EST-04 | Horizonte | peito, 9 cm | as 3 | DTF | ⚪ reserva (geométrico, fora da linguagem) | — |
| EST-05 | Aracati | peito, 9 cm | as 3 | DTF | ⚪ reserva (geométrico); a ideia pode voltar à mão | — |
| EST-06 | Jangada | peito, 8 cm | as 3 | DTF | ⚪ reserva (geométrico); a ideia pode voltar à mão | — |
| EST-07 | Postura | costas, 23,5 cm | as 3 | DTF | 🟡 mockup plano (30/10) | foto de costas; escolha do Jorge |
| EST-09 | Caju | peito, 9,2 cm | as 3 | DTF | 🟡 primeiro teste da linguagem (traço à mão + pontilhismo) | ok do Jorge na direção; afinar a castanha |
| EST-08 | Meio-dia | peito, 7 cm | as 3 | DTF | ⚪ reserva (geométrico); a ideia pode voltar à mão | — |

Linguagem (30/10): traço à mão, pontilhismo, hachura e xilogravura, como o Cavalheiro. Referências em `referencias/`.
Peito: padrão medido na primeira peça real (topo 10 cm abaixo da gola, centro 7 cm do meio).
Etiqueta da gola: fica a atual ("MODESTINO essencial. diário. real.", 95% modal / 5% elastano), decisão do Jorge em 30/10.
Artes EST-04 a 08 geradas por `gerar_autorais.py` (rode da raiz com as fontes instaladas).

Fotos-base: só frente por enquanto (preta, mapple, off-white e o trio, do fal.ai). Faltam as de costas.

EST-01 a 03 são a Coleção 01 do guia de identidade (página 2). Preço da Estampada: ⚪ Jorge decide na Central.
