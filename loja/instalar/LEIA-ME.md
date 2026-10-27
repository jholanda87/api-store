# Como instalar as habilidades da máquina de vendas

São 16 habilidades da Modestino + as 11 originais da Replica (MIT, de Jake Schincariol).

## 1. Claude Code (este repositório): já instaladas

Estão em `.claude/skills/`. Qualquer sessão do Claude Code aberta neste repositório já enxerga:
`/maquina-vendas-modestino`, `/loja-recon-modestino`, ... e as originais `/replica-recon`, `/replica-entrepreneur`, ...

Para ter as originais em todos os seus projetos no computador, rode no Claude Code do seu PC (os comandos do vídeo):

```
/plugin marketplace add Jakeschincariol/replica-skill
/plugin install replica-skill@replica-skill
```

## 2. Claude.ai e app do celular (onde ficam as outras habilidades da Modestino)

As habilidades que você já usa (criar-conteudo, agendar-post, financeiro…) ficam na sua conta do Claude.ai. Para as novas aparecerem lá também:

1. Baixe os arquivos `.zip` desta pasta (um por habilidade).
2. No Claude.ai: **Configurações → Recursos (Capabilities) → Habilidades (Skills) → Enviar habilidade (Upload skill)**.
3. Envie um `.zip` por vez. Comece por `maquina-vendas-modestino.zip` e `loja-empreendedor-modestino.zip`.
4. Confira se a chave de cada uma ficou ligada.

As habilidades que usam ferramenta Python já levam a ferramenta dentro do próprio `.zip`.

## 3. Conectores que a máquina usa

| conector | para quê | situação em 27/10 |
| --- | --- | --- |
| Shopify | cadastrar produto, estoque, pedidos | **precisa entrar de novo** (Configurações → Conectores) |
| Metricool | métricas e agendamento | ok |
| Google Drive | fotos e artes | ok |
| Photoroom | fundo e sombra das fotos de produto | ok (gasta créditos) |
| Canva / Adobe | artes e vetorizar o Cavalheiro | ok |
