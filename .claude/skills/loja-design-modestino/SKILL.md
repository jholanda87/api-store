---
name: loja-design-modestino
description: "Use quando Jorge pedir o design, o tema, as cores, fontes ou componentes da loja virtual da Modestino: transforma a identidade oficial (O Cavalheiro) em tokens e especificações de componentes, com checagem de contraste."
---

# Design da loja (Replica adaptada)

Versão Modestino do `replica-design`. A diferença: a Replica reconstrói o sistema de design do app copiado; a Modestino **já tem identidade**. Aqui se mede a estrutura das referências (onde fica cada coisa, hierarquia, espaçamento) e se veste tudo com a marca. Leia `site-impecavel-modestino` (padrão de qualidade da landing aprovada) e `criar-conteudo-modestino` (regras visuais).

Ferramenta:

```bash
python3 .claude/skills/replica-design/contrast.py loja/design/tokens.json
```

## As regras

- **Herdar, não reinventar.** Linho #ECE7DE / #E4DDD0, carvão #22201D / #1E1D1C, mapple #5B3F30, areia #CBBFAE, grafite #6E675F (texto secundário sobre linho: #5F5850). Instrument Serif nos títulos (itálico na ênfase), Instrument Sans no texto e no nome MODESTINO espaçado, Geist Mono só em preço, medida e dado.
- **O Cavalheiro** só em cabeçalho/rodapé, favicon, e-mail e embalagem. Nunca na roupa nem estampado em foto de produto.
- **Nada das referências:** nem cor, nem ícone, nem foto, nem texto. Ícone de traço único de um pacote aberto (Lucide, Phosphor, Tabler).
- **Identidade antiga (terracota + Poppins) não entra na loja.**
- **Fotos reais,** nunca banco de imagem nem IA vendendo a peça.

## Passo 1: medir as referências (estrutura, não pixel)

Dos prints em `loja/screens/`: largura máxima, grade, altura do cabeçalho, tamanho da foto de produto, onde ficam preço, seletor de cor e tamanho, botão de compra, frete e troca na primeira dobra do celular. Isso vira layout; os valores visuais vêm da marca.

## Passo 2: tokens

`loja/design/tokens.json` já existe com os papéis da Replica e os valores da marca (13 de 13 pares passando AA em 27/10/2026). Ao mudar qualquer valor, rode o contraste: zero falha AA (4,5:1 texto, 3:1 texto grande, borda de input e anel de foco). Gere `tokens.css` (variáveis CSS) ou as configurações do tema da plataforma a partir dele. Nenhum hex solto em componente.

## Passo 3: componentes (um bloco por componente em `loja/design/componentes.md`)

```
Seletor de tamanho
  variantes  disponível, últimas peças, esgotado (riscado, "avise-me")
  tamanhos   44 px mínimo de toque
  estados    padrão, hover, foco visível (anel accent 2px), selecionado, desabilitado
  tokens     borda border-input, selecionado bg surface-dark texto text-on-dark
  a11y       grupo de radio com legenda "Tamanho", esgotado anunciado ao leitor de tela
  usado em   S03 produto, S05 carrinho
```

Mínimo: botão (comprar, secundário, fantasma), seletor de cor (troca foto e fundo), seletor de tamanho, guia/calculadora de tamanho, preço (Geist Mono, números tabulares), aviso de frete por CEP, selo de troca, card de produto, carrinho lateral, campo com erro, mensagem de vazio, faixa de anúncio, rodapé com CNPJ.

## Passo 4: primitivos

Monte os componentes isolados numa página de amostra (ou na área de seções do tema), renderize em 1440 e 390 px com Playwright e olhe uma vez. Essa é a checagem do sistema.

## Saída

`tokens.json` (e `tokens.css` ou configuração do tema), `componentes.md`, a página de amostra e o relatório de contraste sem falhas. Próxima: `catalogo-modestino`.

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), as ferramentas citadas acima vêm dentro da própria pasta desta habilidade, ao lado deste SKILL.md: troque `.claude/skills/<pasta>/` pelo caminho desta pasta. Sem Python disponível, siga o método à mão; ele funciona igual.
