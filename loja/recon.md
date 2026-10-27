# Recon da loja — referências e mapa da loja Modestino

Feito em 27/10/2026 com `loja-recon-modestino`. Só páginas públicas, lidas uma vez cada. Nada de texto, foto ou cor das referências vai para a loja: aqui está só **o que elas fazem**.

## Fontes

| referência | página | o que deu | lida em |
| --- | --- | --- | --- |
| Insider | [insiderstore.com.br](https://www.insiderstore.com.br/) | estrutura da página inicial, menu, faixa de confiança, cards | 27/10/2026 |
| Insider | [página da Tech T-Shirt](https://www.insiderstore.com.br/products/tech-t-shirt) | só o topo (galeria, cores); o resto veio truncado | 27/10/2026 |
| Hering | [hering.com.br](https://www.hering.com.br/) | faixa de benefícios, menu de ajuda, rodapé | 27/10/2026 |
| Reserva | [usereserva.com](https://www.usereserva.com/) | só cabeçalho e carrossel (resto truncado) | 27/10/2026 |
| Básico (Malwee) | [malwee.com.br/home-marca-basico](https://www.malwee.com.br/home-marca-basico/) | estrutura, frete, rodapé com atendimento | 27/10/2026 |
| Reclame Aqui | páginas das empresas | **bloqueado para leitura automática (403)** — ver `loja/coleta-avaliacoes.md` | 27/10/2026 |

Ainda falta (precisa do navegador do Jorge): página de produto completa de uma referência (tamanho, frete, troca perto do botão, avaliações), checkout até antes de pagar, e-mails de pedido.

## O que as referências fazem (padrões, não cópia)

1. **Faixa de confiança no topo e logo abaixo da primeira tela:** frete (grátis acima de um valor: Hering R$ 349,99, Básico R$ 299; Insider grátis em tudo), troca/devolução grátis (Hering: 15 dias), parcelamento (Hering: 6x sem juros) e vantagem no Pix (Insider). É o padrão mais repetido entre as quatro.
2. **Primeira tela = campanha** (carrossel com "comprar"), não uma tese. Oportunidade para a Modestino: a landing aprovada já abre com tese + prova.
3. **Menu com atalho para kits / "leve mais"** (Insider "Kits", Básico "Combos") e para o produto-estrela (Insider tem item de menu só para a camiseta principal).
4. **Card de produto** com bolinhas de cor, nota em estrelas e número de avaliações, selo (best-seller, últimas peças) e compra rápida.
5. **Galeria grande** por cor: frente, costas, detalhe, corpo inteiro e vídeo no fim.
6. **Ajuda organizada:** status do pedido, devoluções, entrega, pagamento, central de atendimento com horário e WhatsApp, CNPJ e endereço no rodapé.
7. **Urgência e desconto o tempo todo** (contador regressivo, "% OFF", brinde por valor). **A Modestino não copia isso:** a Central proíbe preço menor na avulsa e manda educar antes de vender.
8. **Garantia contra desbotamento** anunciada (Insider). A Modestino só pode prometer o que testou: fica como teste a fazer (10 lavagens), não como promessa.

## Telas da loja Modestino

| ID | tela | como chega | para quê | componentes | estados |
| --- | --- | --- | --- | --- | --- |
| S01 | início | link da bio, anúncio | tese + oferta + prova + ação | hero com troca de cor, faixa de confiança, kits, prova real, fechamento | celular, sem estoque numa cor |
| S02 | coleção (camisetas e kits) | menu | ver tudo | card de produto | vazio (no futuro) |
| S03 | produto: Camiseta Básica | S01, post, catálogo | escolher cor e tamanho | galeria, seletor de cor, seletor de tamanho, calculadora, preço, frete por CEP, troca | esgotado, últimas peças, CEP inválido |
| S04 | guia/calculadora de tamanho | S03 | acertar o tamanho | campo de medida, resultado com `aria-live` | medida fora da tabela |
| S05 | produto: Kit 2 / Kit 3 / Essencial | S01, S03 | levar mais com ecobag | escolha cor e tamanho por peça, preço por peça | uma das escolhas esgotada |
| S06 | carrinho | botão comprar | revisar | linhas, cupom, frete, total | vazio, cupom inválido, cupom no kit |
| S07 | checkout: dados e entrega | S06 | endereço | formulário, opção "entrega em Fortaleza" | CEP fora da área |
| S08 | checkout: pagamento | S07 | pagar | Pix (QR + copia e cola), cartão até 3x | Pix expirado, cartão recusado |
| S09 | pedido confirmado | S08 | tranquilizar | resumo, prazo, WhatsApp | Pix pendente |
| S10 | acompanhar pedido | e-mail/WhatsApp | ver status | status, rastreio | não encontrado |
| S11 | trocas e devoluções | rodapé, S03 | pedir troca | texto + botão WhatsApp | — |
| S12 | perguntas frequentes | rodapé | tirar dúvida | lista aberta/fechada | — |
| S13 | privacidade / termos | rodapé | LGPD | texto | — |
| S14 | sobre a Modestino | menu | história (família de confecção, Fortaleza) | texto + fotos reais | — |

## Fluxos

```
F01 Compra avulsa pelo celular (meta: 5 toques até o Pix)
    S03 -> (S04) -> S06 -> S07 -> S08 -> S09
    borda: tamanho esgota no meio, CEP fora de Fortaleza, Pix expira
F02 Compra de kit
    S05 -> S06 -> S07 -> S08 -> S09
    borda: uma cor esgotada no kit
F03 Compra com cupom de embaixador
    S03 -> S06 (cupom) -> S07 -> S08 -> S09
    borda: cupom no kit é recusado com explicação; cupom inexistente
F04 Troca de tamanho
    S11 -> WhatsApp -> troca em mãos (Fortaleza) ou envio
F05 Vindo do Instagram (bio/post/catálogo) — chega direto em S03 ou S05 com UTM
F06 Vindo do WhatsApp (catálogo) — link do produto ou pedido fechado no próprio chat
```

## Dados

- **Produto** Camiseta Básica; **variante** cor (preta, marrom, off) × tamanho (P–GG); SKU `MOD-CAM-<COR>-<TAM>`. Evidência: Painel `stock.lots`. Confiança alta.
- **Kit** (2, 3, Essencial) que baixa o estoque das variantes. Evidência: Central seção 3. Alta.
- **Cupom** por embaixador, 10% só na avulsa. Evidência: Central seções 3 e 7. Alta.
- **Pedido** com origem (UTM/cupom) e quem despacha (Jorge ou Lucas, estoque dividido). Evidência: Central seção 8. Média (como dividir o despacho é decisão em aberto).

## O que não se copia

Contador de urgência e desconto permanente; brinde por valor de compra (até decidir margem); app próprio; programa de pontos; garantia de desbotamento sem teste.

## Tamanho

14 telas, 6 fluxos, 4 entidades. Partes difíceis: estoque dividido em duas casas sincronizado com o Painel; kit que baixa variantes; frete local de Fortaleza. Em plataforma pronta (Shopify): **M — algumas semanas** no ritmo de 3 a 4 h/dia, sendo a fatia vertical (F01) um fim de semana.

Próxima etapa: `loja-empreendedor-modestino` (depende da coleta de avaliações — `loja/coleta-avaliacoes.md`).
