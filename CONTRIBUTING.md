# Contribuindo com o Dataset fipeX

Este repositório é, primariamente, um **canal de distribuição** dos dados extraídos pelo projeto [fipeX](https://fipex.com.br). Os dados em si são gerados automaticamente a partir do banco de produção — você não vai abrir PR adicionando linhas ao CSV.

Mesmo assim, há vários tipos de contribuição muito bem-vindos.

## Tipos de Contribuição

### 1. Scripts de exemplo

Adicionar exemplos em outras linguagens/ferramentas é a contribuição mais fácil e útil:

- `examples/python.py` — já existe (Polars + Pandas)
- `examples/duckdb.sql` — já existe
- `examples/r.R` — ainda não existe, PR aberto
- `examples/julia.jl` — ainda não existe
- `examples/spark.py` — ainda não existe

Mantenha cada exemplo **curto** (50–100 linhas), com comentários explicativos em pt-BR.

### 2. Documentação

- Melhorias na descrição das colunas
- Explicação de casos extremos (ex: por que `valor_centavos` em vez de `valor_reais`)
- Tradução do README para outros idiomas (em arquivos separados como `README.en.md`)
- Notebooks de exploração (em `notebooks/`, formato `.ipynb`)

### 3. Problemas nos dados

Se você encontrar um erro grosseiro nos dados:

- Abra uma [issue](https://github.com/fipex-labs/dataset/issues/new/choose) descrevendo o caso (`codigo_fipe`, período, valor problemático)
- Lembre-se: o dataset reflete o que a FIPE publicou. Se o erro veio da fonte, não dá para corrigir aqui — mas vale documentar como nota de release.

### 4. Pipeline de geração

O pipeline que gera os dumps mensais não é público. Sugestões sobre ele (novas colunas, validações, formatos adicionais) são bem-vindas como [issue](https://github.com/fipex-labs/dataset/issues/new/choose) neste repositório.

## Fluxo

1. Fork → branch → PR.
2. **Commits assinados** (`git config commit.gpgsign true`).
3. **Conventional Commits**: `feat(examples): add R example`, `docs(schema): clarify zero_km semantics`.
4. PRs pequenos. Para mudanças maiores, abra uma issue antes.

## Setup local

Para rodar os exemplos:

```bash
git clone https://github.com/fipex-labs/dataset.git
cd dataset

# Os arquivos grandes ficam em LFS (hospedado no Hugging Face) — o caminho
# mais simples é baixar do release mais recente:
gh release download --pattern '*.parquet'

# Ou:
curl -L -o fipex-prices-latest.parquet \
  https://github.com/fipex-labs/dataset/releases/latest/download/fipex-prices-latest.parquet

# Python
python -m venv .venv && source .venv/bin/activate
pip install polars pandas
python examples/python.py
```

## Código de Conduta

Veja [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Aplica-se a todas as interações no repositório.

## Segurança

Veja [SECURITY.md](SECURITY.md) para reports.
