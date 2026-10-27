---
name: loja-recon-modestino
description: "Use quando Jorge pedir para estudar, mapear ou \"clonar\" a loja virtual de uma marca de referência (Insider, Reserva, Hering, Básico.com ou outra), ou para saber que telas e recursos a loja da Modestino precisa ter: gera o mapa de telas, fluxos de compra e a matriz de recursos."
---

# Recon da loja (Replica adaptada à Modestino)

Versão Modestino do `replica-recon`. Tudo que vem depois nasce daqui: um mapa ruim dá uma loja ruim. Leia antes `.claude/skills/replica-recon/SKILL.md` (o método original) e `loja/features.csv` (a matriz que já existe).

## As regras, antes de tudo

- **Só fonte pública** (site, central de ajuda, política de troca, perfil no Instagram, avaliações públicas) e a conta do próprio Jorge, se ele comprar numa referência. Nunca login de outra pessoa, nunca passar de paywall.
- **Ler como gente, não raspar.** Sem robô, sem download em massa. Navegador em velocidade humana.
- **Sem código, sem API privada.** Não salvar JavaScript, não copiar chamadas de rede.
- **Print é referência.** Fica em `loja/screens/`, serve para comparar estrutura e nunca vai para a loja.
- **O que a Modestino copia é o fluxo**, não o texto, a foto, a cor nem o nome.

## Passo 1: escopo (proponha e peça um sim)

1. **Quais referências.** Padrão: as estéticas da Central (Insider, Ricardo Almeida, Mirante) + 1 grande de básico (Hering ou Reserva) + 1 marca local de Fortaleza que venda online.
2. **Qual fatia.** Padrão: o laço central — descobrir a peça → escolher cor e tamanho → pagar → receber → trocar se precisar.
3. **Para quem.** O cliente da Central: homem de 22 a 40, Fortaleza, compra rápido pelo Instagram e WhatsApp, paga R$ 90 a R$ 250 numa peça.

## Passo 2: fontes, com link em cada linha

Página de produto, tabela de medidas, política de troca, FAQ/central de ajuda, página de frete, checkout até antes de pagar, e-mails de pedido (se Jorge comprou), perfil do Instagram e catálogo do WhatsApp.

## Passo 3: telas (IDs estáveis S01, S02…)

`ID | tela | como chega | para quê | componentes | estados vistos`. Estados contam: esgotado, sem estoque no tamanho, CEP inválido, cupom inválido, carrinho vazio, erro de pagamento, celular.

Telas mínimas de uma loja de básico: início, coleção, produto, guia de tamanho, carrinho, checkout (dados, entrega, pagamento), pedido confirmado, rastreio, troca/devolução, FAQ, contato, políticas.

## Passo 4: fluxos (F01, F02…) com cliques contados

```
F01 Cliente compra 1 camiseta pelo celular
    S03 produto -> S04 guia de tamanho -> S05 carrinho -> S06 checkout -> S07 confirmado
    borda: tamanho esgotado, CEP fora de Fortaleza, Pix expira, cupom de embaixador no kit
```

Fluxos obrigatórios: compra avulsa, compra de kit, compra com cupom de embaixador, troca de tamanho, cliente vindo do Instagram (link na bio ou post), cliente vindo do WhatsApp. O número de cliques do caminho feliz vira a meta a bater.

## Passo 5: componentes e dados

Componentes repetidos (seletor de cor, de tamanho, botão de compra, aviso de frete, selo de troca) e o modelo de dados inferido (produto, variante cor × tamanho, kit, pedido, cupom, cliente), cada um com evidência e confiança.

## Passo 6: matriz de recursos

Atualize `loja/features.csv` (colunas: feature, area, priority, original, clone, notes). `original = yes` quando as referências têm; `no` para os diferenciais da Modestino (calculadora de tamanho, troca em mãos). `clone` começa em `no`. Marque `skip` com motivo o que não se copia (marketplace de outras marcas, programa de pontos cedo demais).

## Passo 7: tamanho do projeto

Telas, fluxos, partes difíceis (frete, Pix, estoque sincronizado com o Painel) e um tamanho honesto: P (um fim de semana numa plataforma pronta), M (algumas semanas), G (loja própria em código).

## Saída

`loja/recon.md`, `loja/features.csv` atualizado, prints em `loja/screens/` e um resumo de 5 linhas: o laço central, número de telas e fluxos, as 3 partes mais difíceis, o que ficou fora e a próxima etapa: `loja-empreendedor-modestino`. Atualize `loja/estado.md`.
