---
name: loja-build-modestino
description: "Use quando Jorge pedir para construir, montar ou ajustar uma página da loja virtual da Modestino (início, produto, carrinho, checkout, guia de tamanho, FAQ, políticas): constrói tela a tela a partir do recon, dos tokens e da landing aprovada, com todos os estados."
---

# Construção da loja (Replica adaptada)

Versão Modestino do `replica-build`. Lê `loja/recon.md`, `loja/arquitetura.md`, `loja/design/` e `loja/correcoes.md`. Atualiza a coluna `clone` de `loja/features.csv` e mantém `loja/build-log.md`. O padrão de acabamento é o de `site-impecavel-modestino` (Impeccable): leia e siga as seções "Modo e estrutura", "Proibido" e "Piso de qualidade".

## As regras

- **Sala limpa.** Toda linha é escrita aqui. Nunca colar HTML, CSS, JS, SVG ou foto de referência; nunca carregar nada do domínio delas.
- **Nossas palavras.** Fazer o que o botão deles faz é paridade; repetir a frase deles é cópia.
- **Só tokens.** Nenhum hex ou px solto; faltou valor, entra no `tokens.json`.
- **Fatos só confirmados** (preço, grade, medidas, prazos). O resto vira [PLACEHOLDER] e pergunta ao Jorge.

## Passo 1: a casca

Tema da plataforma (ou rotas, se for código próprio) com todas as telas do recon, cabeçalho com o Cavalheiro + MODESTINO, rodapé com políticas e CNPJ, tokens ligados, produtos de verdade do `catalogo-modestino`.

## Passo 2: a fatia vertical

Do post do Instagram ao pedido confirmado, no celular: produto → cor → tamanho → carrinho → Pix → confirmado. Antes de qualquer outra tela.

## Passo 3: tela a tela

Na ordem de `arquitetura.md`. Para cada tela:

1. Leia a linha dela no recon (para quê, componentes, estados, fluxos).
2. Olhe o print da referência pela hierarquia, não pelo pixel.
3. Construa com os componentes de `componentes.md`.
4. **Todos os estados:** vazio, carregando, cheio, erro, esgotado, cupom inválido, CEP fora da área, texto longo, 390 px.
5. Básico sempre: HTML semântico, rótulo em todo campo, teclado alcança tudo, foco visível, `alt` em toda foto.
6. Marque `yes` ou `partial` (com nota) em `features.csv`.
7. Print em `loja/clone-screens/S03.png` no mesmo tamanho do print da referência.
8. Um commit por tela: `loja: S03 página de produto`.

## Telas com regra própria da Modestino

- **Início:** a primeira tela é uma tese (a oferta, o desejo, a ação, uma prova), com o ângulo escolhido em `correcoes.md`.
- **Produto:** seletor de cor troca foto e fundo; calculadora de tamanho pela largura da camiseta que a pessoa já tem (com `aria-live` e erro para medida fora da tabela); frete e troca visíveis antes do botão.
- **Kit:** escolher cor e tamanho de cada peça; mostrar o preço por peça (R$ 75 no kit 3).
- **Checkout:** compra sem conta; Pix em destaque; cupom de embaixador recusado no kit com explicação gentil.
- **Políticas e FAQ:** texto de `administrativo-modestino`.

## Feito, por tela

- [ ] todos os estados do recon + vazio, erro, carregando
- [ ] funciona em 390 e 1440 px
- [ ] só teclado completa o fluxo
- [ ] sem erro no console
- [ ] nenhum texto copiado de referência; `vitrine.py` sem erro nos textos de produto
- [ ] `features.csv` atualizado e print salvo

## Saída

Telas prontas, matriz atualizada, prints salvos e resumo: telas feitas de quantas, `must` feitos de quantos, o que vem depois (`loja-backend-modestino` ou `loja-teste-modestino`). Quando algo for maior que parecia, diga no log e na conversa; não entregue metade calado.
