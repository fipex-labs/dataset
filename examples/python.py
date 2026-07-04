#!/usr/bin/env python3
"""
Exemplo de uso do dataset fipeX.
Demonstra carregamento, análise básica e comparação entre formatos CSV e Parquet.
"""
import time
from pathlib import Path

import polars as pl


# Raiz do repositório (os arquivos de dados ficam um nível acima de examples/)
BASE_DIR = Path(__file__).resolve().parent.parent


def load_csv(filename: str) -> pl.DataFrame:
    """Carrega arquivo CSV (separado por tabulação)."""
    path = BASE_DIR / filename
    return pl.read_csv(path, separator="\t")


def load_parquet(filename: str) -> pl.DataFrame:
    """Carrega arquivo Parquet."""
    path = BASE_DIR / filename
    return pl.read_parquet(path)


def show_basic_stats(df: pl.DataFrame, name: str):
    """Mostra estatísticas básicas do dataset."""
    print(f"\n{'='*60}")
    print(f"Estatísticas - {name}")
    print(f"{'='*60}")
    print(f"Total de registros:     {df.height:,}")
    print(f"Total de marcas:        {df['nome_marca'].n_unique():,}")
    print(f"Total de modelos:       {df['nome_modelo'].n_unique():,}")
    print(f"Total de códigos FIPE:  {df['codigo_fipe'].n_unique():,}")

    # Período de referência
    periods = df.select("ano_referencia", "mes_referencia").unique()
    min_row = periods.sort("ano_referencia", "mes_referencia").row(0)
    max_row = periods.sort("ano_referencia", "mes_referencia").row(-1)
    print(f"Períodos de referência: {periods.height:,}")
    print(f"  Mais antigo:  {min_row[1]:02d}/{min_row[0]}")
    print(f"  Mais recente: {max_row[1]:02d}/{max_row[0]}")

    # Top 10 marcas por quantidade de registros
    print(f"\nTop 10 marcas (por quantidade de registros):")
    top_brands = (
        df.group_by("nome_marca")
        .len()
        .sort("len", descending=True)
        .head(10)
    )
    for idx, row in enumerate(top_brands.iter_rows(), 1):
        print(f"  {idx:2d}. {row[0]:20s} {row[1]:>8,} registros")


def compare_versions():
    """Compara versões merged e original do dataset."""
    print(f"\n{'='*60}")
    print("Comparação: Original vs Merged")
    print(f"{'='*60}")

    df_original = load_csv("fipex-prices-latest.csv")
    df_merged = load_csv("fipex-prices-latest-merged.csv")

    orig_models = df_original["nome_modelo"].n_unique()
    merged_models = df_merged["nome_modelo"].n_unique()

    print(f"Registros na versão original: {df_original.height:,}")
    print(f"Registros na versão merged:   {df_merged.height:,}")
    print(f"Modelos únicos no original:   {orig_models:,}")
    print(f"Modelos únicos no merged:     {merged_models:,}")
    print(f"Modelos renomeados/mesclados: {orig_models - merged_models:,}")
    print("\nInterpretação:")
    print("  - Ambas versões contêm os mesmos registros de preços")
    print("  - Original: usa os nomes de modelos como publicados originalmente")
    print("  - Merged: unifica modelos renomeados sob o nome atual")
    print("  - A diferença está na atribuição de nomes, não na quantidade de dados")


def show_price_evolution():
    """Mostra evolução de preço de um modelo específico."""
    print(f"\n{'='*60}")
    print("Evolução de Preço - Exemplo")
    print(f"{'='*60}")

    df = load_csv("fipex-prices-latest.csv")

    # Exemplo: buscar um modelo Gol da VW, ano 2020
    model_data = (
        df.filter(
            pl.col("nome_marca").str.contains("(?i)volks")
            & pl.col("nome_modelo").str.contains("(?i)gol")
            & (pl.col("ano_modelo") == 2020)
        )
        .sort("ano_referencia", "mes_referencia")
    )

    if model_data.height > 0:
        first = model_data.row(0, named=True)
        print(f"Marca:  {first['nome_marca']}")
        print(f"Modelo: {first['nome_modelo']}")
        print(f"Ano:    {first['ano_modelo']}")
        print(f"\nEvolução de preços (últimos 12 meses):")
        print(f"{'Período':<12} {'Preço':>15}")
        print("-" * 30)
        for row in model_data.tail(12).iter_rows(named=True):
            period = f"{row['mes_referencia']:02d}/{row['ano_referencia']}"
            print(f"{period:<12} {row['valor_formatado']:>15}")
    else:
        print("Modelo de exemplo não encontrado no dataset")
        # Mostra primeiro modelo disponível como fallback
        first = df.row(0, named=True)
        print(f"Primeiro modelo disponível: {first['nome_marca']} - {first['nome_modelo']}")


def compare_performance():
    """Compara performance de leitura entre CSV e Parquet."""
    print(f"\n{'='*60}")
    print("Comparação de Performance: CSV vs Parquet")
    print(f"{'='*60}")

    # Tamanho dos arquivos
    csv_path = BASE_DIR / "fipex-prices-latest.csv"
    parquet_path = BASE_DIR / "fipex-prices-latest.parquet"

    if not csv_path.exists() or not parquet_path.exists():
        print("Arquivos necessários não encontrados para comparação de performance")
        return

    csv_size = csv_path.stat().st_size
    parquet_size = parquet_path.stat().st_size

    print(f"Tamanho dos arquivos:")
    print(f"  CSV:     {csv_size / 1024 / 1024:>10.2f} MB")
    print(f"  Parquet: {parquet_size / 1024 / 1024:>10.2f} MB")
    if csv_size > 0:
        print(f"  Redução: {(1 - parquet_size / csv_size) * 100:>9.1f}%")

    # Tempo de leitura
    print(f"\nTempo de carregamento:")

    start = time.time()
    df_csv = load_csv("fipex-prices-latest.csv")
    csv_time = time.time() - start
    print(f"  CSV:     {csv_time:>10.3f}s ({df_csv.height:,} linhas)")

    start = time.time()
    df_parquet = load_parquet("fipex-prices-latest.parquet")
    parquet_time = time.time() - start
    print(f"  Parquet: {parquet_time:>10.3f}s ({df_parquet.height:,} linhas)")
    if parquet_time > 0:
        print(f"  Speedup: {csv_time / parquet_time:>9.2f}x")


def main():
    print("=" * 60)
    print("FipeX - Exemplos de Uso dos Dados")
    print("=" * 60)

    # Carrega dados merged para estatísticas
    print("\nCarregando dados (versão merged)...")
    df_merged = load_csv("fipex-prices-latest-merged.csv")

    # Mostra estatísticas básicas
    show_basic_stats(df_merged, "Versão Merged (Consolidada)")

    # Compara versões original e merged
    compare_versions()

    # Mostra evolução de preço de um modelo
    show_price_evolution()

    # Compara performance CSV vs Parquet
    compare_performance()

    print("\n" + "=" * 60)
    print("Exemplos concluídos!")
    print("=" * 60)


if __name__ == "__main__":
    main()
