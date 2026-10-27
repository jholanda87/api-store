# O que os clientes odeiam e o que a Modestino faz diferente

Etapa 2 (`loja-empreendedor-modestino`), 28/10/2026. Base: 114 reclamações de camiseta no Reclame Aqui, de 4 marcas (Insider 24, Reserva 30, Hering 30, Básico 30), coletadas pelo Jorge no Chrome. Detalhe e links em `feedback.md`; linhas em `reviews.csv`. Os textos são resumos, não citações; nenhuma frase de cliente dos outros vai para a loja.

## 1. O que odeiam

| # | problema | reclamações | marcas | exemplo |
| --- | --- | --- | --- | --- |
| 1 | **Pedido errado, incompleto ou cancelado** (comprou 3 e chegou 1, cor/tamanho trocado, item removido, pedido cancelado depois de pago, cupom não honrado) | 53 (46%) | 4 | [Reserva: recebeu 1 de 3](https://www.reclameaqui.com.br/reserva/recebi-apenas-1-camiseta-de-3-que-comprei-e-a-reserva-nao-resolve_tobJwDuHRQYktiQb/) · [Hering: cinza em vez de azul-marinho](https://www.reclameaqui.com.br/hering-loja-virtual/recebi-camiseta-cinza-em-vez-de-azul-marinho-e-nao-consigo-usar-bonus_LQjgsQXgTZEYOtWE/) |
| 2 | **Troca e estorno difíceis** (devolução recusada, estorno que não cai ou vem menor, vale-troca no lugar do dinheiro) | 37 (32%) | 4 | [Hering: vale-troca menor e prazo curto](https://www.reclameaqui.com.br/hering-loja-virtual/recebi-vale-troca-com-valor-inferior-ao-da-devolucao-e-prazo-curto_VRO1ws0s6Ti4xC28/) |
| 3 | **Camiseta que estraga cedo** (costura abre, gola, bolinha, desbota, alarga ou encolhe em 1 a 3 lavagens) | 30 (26%) | 4 | [Insider: descosturou na primeira lavagem](https://www.reclameaqui.com.br/insider-store/minha-camiseta-insider-descosturou-na-primeira-lavagem_Myjl4aDKqYzqA9On/) |
| 4 | Preço, frete e cupom (promoção que não aplica, frete que muda no fim, "leve 3 pague 2" confuso) | 18 (16%) | 4 | [Reserva: leve 3 pague 2 e frete](https://www.reclameaqui.com.br/reserva/fui-enganado-com-propaganda-leve-3-pague-2-e-frete-abusivo_idT-9JO_JJ-5zmEf/) |
| 5 | Atendimento que não responde ou não tem pessoa | 18 (16%) | 4 | [Hering: ninguém respondeu](https://www.reclameaqui.com.br/hering-loja-virtual/nao-recebi-minha-camiseta-comprada-online-e-ninguem-respondeu_zW5HyOCy60JEm0ap/) |
| 6 | Atraso e rastreio parado | 13 (11%) | 3 | [Básico: um mês e rastreio com erro](https://www.reclameaqui.com.br/basico-com/pedido-de-camiseta-de-manga-longa-nao-recebido-apos-um-mes-e-link-de-rastreamento-com-erro_HipHQtTqaPyOehuG/) |

## 2. O que falta (pedem pelo nome)

- **Tecido igual ao anunciado** — 10 reclamações, 3 marcas (composição diferente, "Pima que não é Pima", cheiro, marca de suor). [Básico](https://www.reclameaqui.com.br/basico-com/vendem-camiseta-algodao-comum-como-se-fosse-algodao-pima_nbL53qD4abph2mdT/)
- **Tamanho que segue a tabela** — 8 reclamações, 3 marcas (veio maior, menor ou diferente do padrão). [Básico](https://www.reclameaqui.com.br/basico-com/divergencia-de-tamanho-em-camiseta-cor-mirtilo-e-solicitacao-de-troca_FfTm5E_DWUOLhYV2/)
- Embalagem de presente inteira (poucas, fraco).

## 3. O que ninguém resolve

**Comprar camiseta online sem medo.** Em 4 marcas grandes, o que mais pesa não é o tecido: é o cliente não confiar que vai chegar o que pediu e que a troca vai funcionar (temas 1, 2, 5 e 6 juntos aparecem em quase todas as reclamações). Nenhuma delas tem alguém com nome respondendo e resolvendo. É exatamente o tamanho e o jeito da Modestino.

## 4. Plano de correções (entram em `features.csv` com `original = no`)

| # | o que a Modestino faz | tamanho | quem faz | evidência |
| --- | --- | --- | --- | --- |
| 1 | **Pedido conferido por um dos sócios**, com foto das peças (cor e tamanho) no WhatsApp antes de sair | P | pos-venda-modestino | tema 1, 53 |
| 2 | **Entrega em Fortaleza por um dos sócios ou Uber Flash**, com aviso de quem leva e quando; fora, rastreio enviado no mesmo dia | P | loja-backend-modestino | temas 1 e 6 |
| 3 | **Troca sem burocracia**: em mãos em Fortaleza; estorno por Pix em até 2 dias úteis; nunca vale-troca obrigatório | P | administrativo-modestino | tema 2, 37 |
| 4 | **Preço fechado e cupom que funciona**: kit com preço final (R$ 160 / R$ 225), cupom testado antes de divulgar, pedido pago nunca cancelado por erro nosso | P | loja-teste-modestino | tema 4, 18 |
| 5 | **Atendimento com nome**: Jorge ou Lucas no WhatsApp, resposta em até 10 min no horário | P | atendimento-modestino | tema 5, 18 |
| 6 | **Teste público de 10 lavagens** (antes e depois, por cor) antes de qualquer promessa de durabilidade | M | criar-conteudo-modestino | tema 3, 30 |
| 7 | **Tamanho pela camiseta que você já tem**: calculadora e medidas reais de cada tamanho | P (já no design) | loja-build-modestino | falta, 8 |
| 8 | **Composição verdadeira** na etiqueta e na página, por peça | P | catalogo-modestino | falta, 10 |

## 5. Posicionamento — três opções

**A. Confiança (recomendada)**
> Para quem já recebeu camiseta errada, pedido pela metade ou ficou preso numa troca, a Modestino é o básico que os próprios donos separam, conferem e entregam em Fortaleza — e trocam em mãos.

Evidência: pedido errado/incompleto (53) + troca e estorno (37) + atendimento (18), nas 4 marcas. Já é verdade hoje, não depende de teste.

**B. Durabilidade**
> Para quem já viu camiseta perder a forma em duas lavagens, a Modestino é o básico testado lavagem por lavagem antes de chegar até você.

Evidência: 30 reclamações, 4 marcas. **Só depois do teste de 10 lavagens** (regra: só prometer o que foi testado).

**C. Atendimento**
> Camiseta básica com gente de verdade do outro lado: quem te vende é quem resolve.

Evidência: 18 reclamações, 4 marcas. Mais fraca sozinha; entra como apoio da A.

**Recomendação:** lançar com a **A**, que é verdade desde o primeiro pedido, e somar a **B** quando o teste de 10 lavagens estiver gravado. A frase da A vira o título da primeira tela da loja e a base dos anúncios. Nenhuma das três cita outra marca.
