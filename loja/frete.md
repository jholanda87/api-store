# Frete da loja — Fortaleza e fora

Decidido pelo Jorge em 27/10/2026. **Os endereços de partida dos sócios não aparecem aqui nem em lugar público nenhum.** Eles ficam só no cadastro de locais da plataforma (área de administrador, que o cliente não vê), como "Ponto J" e "Ponto L".

## Regra

**Atualização de 27/10 (tarde):** por enquanto só o **Ponto J** despacha. Ele já está cadastrado como local na Shopify (endereço só lá) e todo o estoque está nele. O Ponto L entra depois.


- **Fortaleza:** entrega própria ou Uber Flash, saindo do ponto (J ou L) **mais perto do cliente** que tenha a peça. O frete só cobre o custo (gasolina ou Uber Flash), sem lucro e sem prejuízo.
- **Quem despacha:** o dono do ponto escolhido. Se só um tem a cor/tamanho, sai dele.
- **Troca de tamanho em mãos:** mesma tabela, ou grátis quando junto com uma nova compra.
- **Fora de Fortaleza:** Correios ou transportadora, calculado pelo app de cotação no checkout.

**Atualização 28/10:** todas as peças estão com o Jorge, então por enquanto tudo sai do Ponto J. O Ponto L entra quando o Lucas tiver estoque.

## Valor decidido (28/10, Jorge)

**Fortaleza: R$ 10 fixo**, entrega de carro pelo Jorge.

Conta de referência: carro a 10 km/L e gasolina a R$ 7/L = **R$ 0,70 por km rodado**. Os R$ 10 cobrem até ~14 km rodados (ida e volta), ou seja, clientes a até **~7 km** do Ponto J. Mais longe que isso, a entrega custa mais do que cobra (ex.: 12 km de distância = 24 km rodados = R$ 16,80). Acompanhar no Painel: se muitos pedidos forem longe, rever (faixa extra ou mínimo para frete).

**Decisão do Jorge (27/10, noite):** R$ 10 para Fortaleza inteira, de propósito abaixo do custo nas entregas longe do Ponto J: valor acessível para gerar fluxo. A diferença nas entregas longas entra como custo de aquisição. Configurado pelo Jorge no admin como Entrega local por CEP (60, 610–615); a API não mostra a entrega local, conferir no checkout com um CEP de Fortaleza e um de fora.

## Como fica na Shopify (plano original por distância)

1. Configurações → Locais: criar "Ponto J" e "Ponto L" com o endereço de cada um (só o administrador vê).
2. Configurações → Frete e entrega → Entrega local: ativar no Ponto J, **taxa fixa de R$ 10** para os CEPs de Fortaleza (60000-000 a 61599-999, a confirmar).
3. Desligar "Retirada no local" (mostraria o endereço ao cliente).
4. Estoque por local: cada peça fica no ponto onde está de verdade (o Painel passa a anotar onde está cada peça).

## Falta

- **Bairro do Ponto L** (o nome da rua sozinho não basta: há várias ruas com o mesmo nome em Fortaleza). Passar ao Claude só na conversa, nunca em arquivo.
- As 3 cotações de Uber Flash por ponto.
- Decidir se o Painel registra o estoque por ponto (recomendado para a loja saber de onde despachar).

## Peso para Correios (estimativa, 28/10/2026)

Não há peso padrão publicado para camiseta GG; as fontes dão só a gramatura do tecido (160–170 g/m² em fichas técnicas) e uma média geral de ~200 g por camiseta de algodão. Conta para a GG da Modestino (largura 60 cm, ~1 m² de malha na peça pronta): **~170 a 200 g**. Usamos o teto, para não faltar frete.

| envio | peso cadastrado | conta |
| --- | --- | --- |
| 1 camiseta | **250 g** | 200 g (GG) + saco/etiqueta |
| Kit 2 | **500 g** | 2 × 200 g + ecobag ~100 g |
| Kit 3 / Kit Essencial | **750 g** | 3 × 200 g + ecobag ~100 g + folga |

Caixa ou envelope de referência: 30 × 25 × 5 cm. Quando der, pesar uma GG e um kit 3 numa balança de cozinha e ajustar aqui. Fontes: [ficha de licitação de Pelotas, 160 g/m²](https://saiserver.pelotas.com.br/anexos_licitacao/arq_objeto/2016-05-05_11-30-34_objeto_AnexoIVEspecificacoestecnicas.pdf), [fichas do SENAC-PR](https://www.pr.senac.br/licitacoes/Arquivos/Documentos_Editais/PP012018/PP_01_2018_Fichas_Referenciais.pdf), [média de ~200 g](https://www.auditorioibirapuera.com.br/qual-o-peso-de-uma-camiseta-100-algodao/).
