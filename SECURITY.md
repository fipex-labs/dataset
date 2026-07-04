# Política de Segurança — Dataset fipeX

Este repositório distribui dados públicos da Tabela FIPE em formatos abertos (CSV, Parquet). Como os dados são de domínio público (CC0) e não contêm informações pessoais identificáveis, o escopo de segurança é limitado.

## Reportando problemas

**Dentro do escopo:**

- Erro grosseiro nos dados que possa induzir terceiros ao erro (ex: preço claramente incorreto que se propagou amplamente)
- Vazamento acidental de qualquer informação pessoal identificável (não deveria haver, mas reporte se encontrar)
- Scripts de exemplo (`examples/`) com vulnerabilidades (injeção, eval inseguro, etc.)
- Problema no processo de release que afete a integridade dos snapshots distribuídos

**Fora do escopo:**

- A precisão dos dados em si — eles refletem o que a FIPE publicou
- Bugs em ferramentas de terceiros usadas para ler o dataset (Polars, DuckDB, Pandas)

## Como reportar

Envie um e-mail para **contato@fipex.com.br** com descrição do problema, arquivos/linhas afetados e contexto. Vulnerabilidades de segurança em scripts seguem estes prazos:

- Confirmação em 5 dias úteis
- Avaliação inicial em 14 dias
- Janela de embargo até 90 dias ou até a correção, o que vier primeiro
