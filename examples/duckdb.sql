-- Exemplos de consulta ao dataset fipeX usando DuckDB.
--
-- Como rodar:
--   1. Baixe o parquet mais recente:
--      curl -L -o fipex-prices-latest-merged.parquet \
--        https://github.com/fipex-labs/dataset/releases/latest/download/fipex-prices-latest-merged.parquet
--   2. Abra o duckdb na mesma pasta:
--      duckdb
--   3. Execute as queries abaixo (cole uma de cada vez).

-- 1) Visão geral: total de registros, marcas únicas, intervalo de períodos.
SELECT
  COUNT(*) AS total_registros,
  COUNT(DISTINCT nome_marca) AS marcas_unicas,
  COUNT(DISTINCT codigo_fipe) AS veiculos_unicos,
  MIN(ano_referencia || '-' || LPAD(mes_referencia::VARCHAR, 2, '0')) AS primeiro_periodo,
  MAX(ano_referencia || '-' || LPAD(mes_referencia::VARCHAR, 2, '0')) AS ultimo_periodo
FROM 'fipex-prices-latest-merged.parquet';

-- 2) Top 10 marcas com mais modelos catalogados.
SELECT
  nome_marca,
  COUNT(DISTINCT codigo_fipe) AS total_modelos
FROM 'fipex-prices-latest-merged.parquet'
GROUP BY nome_marca
ORDER BY total_modelos DESC
LIMIT 10;

-- 3) Histórico de preço de um modelo específico (Honda Civic 2020 gasolina).
--    Ajuste o filtro `nome_marca` / `nome_modelo` / `ano_modelo` para o veículo desejado.
SELECT
  ano_referencia,
  mes_referencia,
  valor_centavos / 100.0 AS valor_reais,
  valor_formatado
FROM 'fipex-prices-latest-merged.parquet'
WHERE nome_marca ILIKE '%Honda%'
  AND nome_modelo ILIKE '%Civic%'
  AND ano_modelo = 2020
  AND nome_combustivel ILIKE '%Gasolina%'
ORDER BY ano_referencia, mes_referencia;

-- 4) Depreciação anual média por marca (somente carros, últimos 5 anos de referência).
WITH latest_year AS (
  SELECT MAX(ano_referencia) AS max_ref FROM 'fipex-prices-latest-merged.parquet'
)
SELECT
  nome_marca,
  ROUND(AVG(valor_centavos / 100.0), 2) AS preco_medio_reais,
  COUNT(*) AS amostras
FROM 'fipex-prices-latest-merged.parquet', latest_year
WHERE tipo_veiculo = 'carro'
  AND ano_referencia >= latest_year.max_ref - 4
GROUP BY nome_marca
HAVING COUNT(*) > 100
ORDER BY preco_medio_reais DESC
LIMIT 20;

-- 5) Veículos zero-km no período mais recente.
WITH ultimo AS (
  SELECT MAX(ano_referencia * 100 + mes_referencia) AS ref FROM 'fipex-prices-latest-merged.parquet'
)
SELECT
  nome_marca,
  nome_modelo,
  ano_modelo,
  valor_formatado
FROM 'fipex-prices-latest-merged.parquet', ultimo
WHERE zero_km = TRUE
  AND (ano_referencia * 100 + mes_referencia) = ultimo.ref
ORDER BY valor_centavos DESC
LIMIT 50;
