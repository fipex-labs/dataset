---
license: cc0-1.0
task_categories:
- tabular-regression
- time-series-forecasting
language:
- pt
tags:
- fipe
- veiculos
- brasil
- carros
- precos
pretty_name: fipeX - Dados de Veículos da Tabela FIPE
size_categories:
- 1M<n<10M
---

# fipeX: Dataset Completo da Tabela FIPE

Este dataset contém preços históricos e atuais de veículos comercializados no Brasil, baseados na Tabela FIPE (Fundação Instituto de Pesquisas Econômicas).

Os dados são extraídos e organizados pelo projeto [fipeX](https://fipex.com.br) — uma iniciativa independente para facilitar o acesso a dados automotivos públicos, com [API pública gratuita](https://fipex.com.br/dados-e-api) e este dataset em domínio público.

**Licença:** [CC0-1.0](LICENSE) — domínio público. Use livremente, inclusive comercialmente, sem necessidade de atribuição (atribuição é bem-vinda, claro).

## Sobre o Dataset

Este conjunto de dados é ideal para:
- Análise de depreciação de veículos
- Previsão de preços (Machine Learning)
- Estudos econômicos sobre o mercado automotivo brasileiro
- Criação de aplicações de consulta e análise

## Como Obter os Dados

O dataset é distribuído em três canais:

### 1. GitHub Releases (recomendado para download direto)

As snapshots completas (~1 GB CSV / ~120 MB Parquet) são publicadas como **release assets** em [github.com/fipex-labs/dataset/releases](https://github.com/fipex-labs/dataset/releases). Cada tag (`v2026.05.0`, `v2026.04.0`, etc.) corresponde a uma referência mensal da FIPE.

```bash
# Download direto do release mais recente
curl -L -o fipex-prices-latest-merged.parquet \
  https://github.com/fipex-labs/dataset/releases/latest/download/fipex-prices-latest-merged.parquet

# Ou via gh CLI
gh release download --pattern '*.parquet' -R fipex-labs/dataset
```

### 2. Hugging Face Datasets

Mirror oficial em [huggingface.co/datasets/alanwgt/fipex-veiculos-brasil](https://huggingface.co/datasets/alanwgt/fipex-veiculos-brasil) — ideal para integração com a stack ML (`datasets`, `polars`, etc.).

### 3. Dumps mensais individuais (no git)

Dumps por período de referência (`2026/01/`, `2026/02/`, …) ficam **dentro deste repositório**. São arquivos menores, versionáveis, e úteis para análises pontuais sem precisar baixar o histórico completo.

## Arquivos Disponíveis

### Histórico Completo (via GitHub Releases)

4 arquivos por release, combinando duas versões dos dados e dois formatos:

| Arquivo                              | Versão      | Formato | Descrição                                       |
|--------------------------------------|-------------|---------|-------------------------------------------------|
| `fipex-prices-latest.csv`            | Original    | CSV     | Dados históricos como publicados pela FIPE      |
| `fipex-prices-latest-merged.csv`     | Consolidada | CSV     | Visão consolidada com nomes de modelos atuais   |
| `fipex-prices-latest.parquet`        | Original    | Parquet | Versão original em formato colunar otimizado    |
| `fipex-prices-latest-merged.parquet` | Consolidada | Parquet | Versão consolidada em formato colunar otimizado |

### Por Período de Referência (`YYYY/MM/`)

Dumps individuais por período de referência FIPE, disponíveis apenas na versão **original**:

| Arquivo                            | Formato | Descrição                                         |
|------------------------------------|---------|---------------------------------------------------|
| `YYYY/MM/fipex-prices.csv`        | CSV     | Preços do período como publicados pela FIPE       |
| `YYYY/MM/fipex-prices.parquet`    | Parquet | Mesmos dados em formato colunar otimizado         |

> **Por que apenas versão original nos dumps por período?**
> A versão consolidada (merged) reflete o estado *atual* das fusões de modelos, que muda ao longo do tempo conforme a FIPE renomeia veículos. Um dump merged feito hoje seria diferente de um feito daqui a 6 meses. Para dados por período, a versão original é a única que permanece imutável e reproduzível.

### Qual versão usar?

Ambas as versões do histórico completo contêm **o mesmo número de registros de preços**. A diferença está na atribuição dos nomes de modelos:

**Versão Original** (`fipex-prices-latest.csv` / `.parquet`):
- Usa os nomes de modelos exatamente como foram publicados pela FIPE em cada período
- Se a FIPE renomeou um modelo (ex: "Gol 1.0 Mi" → "Gol 1.0 12V"), os preços antigos mantêm o nome original
- Ideal para análises históricas que precisam rastrear renomeações ao longo do tempo

**Versão Consolidada/Merged** (`fipex-prices-latest-merged.csv` / `.parquet`):
- Unifica modelos renomeados sob o nome atual em **todos os períodos**
- Se um modelo foi renomeado, os preços históricos também aparecem com o nome novo
- Ideal para consultas e análises onde se quer acompanhar a evolução de preço de um veículo sem se preocupar com mudanças de nomenclatura

**Formato CSV** (`.csv`):
- Separado por tabulação (`\t`) - TSV format
- Compatível com Excel, Google Sheets, e qualquer ferramenta de análise de dados
- Fácil de ler e inspecionar visualmente
- Tamanho maior que Parquet

**Formato Parquet** (`.parquet`):
- Formato colunar binário otimizado para análise
- Compressão eficiente (~70% menor que CSV)
- Leitura 3-5x mais rápida que CSV
- Ideal para processamento em Python/Pandas, Spark, DuckDB
- Preserva tipos de dados nativamente

## Estrutura dos Dados

Todos os arquivos compartilham a mesma estrutura de 12 colunas:

| Coluna               | Tipo   | Descrição                                                     |
|----------------------|--------|---------------------------------------------------------------|
| `tipo_veiculo`       | string | Categoria do veículo (carro, moto, caminhão)                  |
| `codigo_fipe`        | string | Código único do veículo na FIPE                               |
| `nome_modelo`        | string | Nome do modelo (ex: Palio 1.0, Corolla XEi)                   |
| `nome_marca`         | string | Fabricante do veículo (ex: Fiat, Toyota)                      |
| `nome_combustivel`   | string | Tipo de combustível (Gasolina, Diesel, Flex, etc)             |
| `sigla_combustivel`  | string | Sigla do combustível (g, e, d, l, f, h, n)                    |
| `ano_modelo`         | int    | Ano de fabricação do modelo                                   |
| `zero_km`            | bool   | Se o veículo é zero quilômetro (true/false)                   |
| `valor_centavos`     | int    | Valor do veículo em centavos (evita erros de ponto flutuante) |
| `valor_formatado`    | string | Valor do veículo em Reais (R$) para facilidade de leitura     |
| `mes_referencia`     | int    | Mês de referência da tabela FIPE (1-12)                       |
| `ano_referencia`     | int    | Ano de referência da tabela FIPE                              |

## Exemplos de Uso

### Python - Polars

```python
import polars as pl

# Carregar CSV (note o separador tab)
df = pl.read_csv("fipex-prices-latest-merged.csv", separator="\t")

# Carregar Parquet (mais rápido!)
df = pl.read_parquet("fipex-prices-latest-merged.parquet")

# Estatísticas básicas
print(f"Total de registros: {df.height:,}")
print(f"Total de marcas: {df['nome_marca'].n_unique():,}")

# Top 10 marcas
print(df.group_by("nome_marca").len().sort("len", descending=True).head(10))
```

Para mais exemplos completos, veja [`examples/python.py`](examples/python.py).

### SQL - DuckDB

```sql
-- Carregar Parquet diretamente
SELECT nome_marca, COUNT(*) as total
FROM 'fipex-prices-latest-merged.parquet'
GROUP BY nome_marca
ORDER BY total DESC
LIMIT 10;
```

Mais consultas prontas em [`examples/duckdb.sql`](examples/duckdb.sql).

## Aviso Legal

Este dataset é derivado de informações públicas disponibilizadas pela FIPE. O fipeX é um projeto independente e **não possui afiliação** com a Fundação Instituto de Pesquisas Econômicas (FIPE).

Os dados são fornecidos "como estão", sem garantias de precisão absoluta. Recomenda-se utilizar com cautela para decisões financeiras críticas.

## Atualização

Os dados são extraídos do banco de dados do FipeX. A intenção é manter este dataset atualizado mensalmente conforme a FIPE libera novas tabelas.

## Como contribuir

Veja [CONTRIBUTING.md](CONTRIBUTING.md). Scripts de exemplo em outras linguagens (R, Julia, Spark, etc.) são especialmente bem-vindos.

## Projetos relacionados

| Recurso                                                      | Conteúdo                                              |
|--------------------------------------------------------------|-------------------------------------------------------|
| [fipex-labs/dataset](https://github.com/fipex-labs/dataset) | Este repositório — dataset (CC0)                      |
| [fipex.com.br](https://fipex.com.br)                        | Consulta da Tabela FIPE, gratuita e sem cadastro      |
| [API pública](https://fipex.com.br/dados-e-api)             | API REST gratuita, sem chave, 10 req/s por IP         |
