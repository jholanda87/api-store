# Coleta de avaliações (etapa 2 — precisa do Jorge)

O Reclame Aqui, o Mercado Livre e o Reddit bloqueiam leitura automática a partir do ambiente do Claude (erro 403 em 27/10/2026). Pela regra do Empreendedor, não se força o bloqueio: a coleta é feita por uma pessoa, no navegador, e o Claude organiza.

## Como fazer (20 a 30 minutos, dá pelo celular)

1. Abra estas páginas (são públicas):
   - https://www.reclameaqui.com.br/empresa/insider-store/lista-reclamacoes/
   - https://www.reclameaqui.com.br/empresa/reserva/lista-reclamacoes/
   - https://www.reclameaqui.com.br/empresa/hering-loja-virtual/lista-reclamacoes/
   - https://www.reclameaqui.com.br/empresa/basico-com/lista-reclamacoes/
   - as perguntas e opiniões de 3 anúncios de "camiseta básica masculina lisa" no Mercado Livre
2. Em cada reclamação sobre **camiseta**, copie o link e o texto e mande para o Claude (print também serve: o Claude transcreve palavra por palavra).
3. Meta: 100 avaliações no total, de pelo menos 3 fontes, as mais recentes primeiro. Inclua as de 3 e 4 estrelas ("gostei, mas…").

Opção mais rápida: no Claude do computador, com a habilidade de navegador (Chrome) ligada, peça "colete as reclamações sobre camiseta destas páginas para o reviews.csv da Modestino". O navegador é o seu, em velocidade humana.

## O que já se sabe (números públicos, a conferir na página)

- Insider: reputação máxima (RA1000), principal problema citado "produto não recebido" — [Reclame Aqui](https://reclameaqui.com.br/empresa/insider-store/).
- Básico.com: reputação "Regular", nota 6,6 nos últimos 6 meses, tempo médio de resposta de mais de 6 dias — [Reclame Aqui](https://www.reclameaqui.com.br/empresa/basico-com/lista-reclamacoes).
- Hering Loja Virtual: nota 8,6, 92,8% resolvidas, resposta média de mais de 5 dias — [Reclame Aqui](https://www.reclameaqui.com.br/empresa/hering-loja-virtual/lista-reclamacoes/).
- Reserva: nota 8,1, 87,2% resolvidas — [Reclame Aqui](https://www.reclameaqui.com.br/empresa/reserva/).

Esses números vieram de resumos de busca, não da leitura da página; confira antes de usar. Já apontam um tema a testar: **tempo de resposta e troca** (a Modestino promete 10 minutos no WhatsApp e troca em mãos em Fortaleza).

Quando `reviews.csv` estiver preenchido, rode `/loja-empreendedor-modestino`.
