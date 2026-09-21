"""
relatorios.py
Bonus: exportacao de relatorios em CSV e geracao de grafico simples
com matplotlib (opcional - so roda se a biblioteca estiver instalada).
"""

import csv
import sqlite3
from pathlib import Path

import queries

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data"


def exportar_faturamento_csv(conexao: sqlite3.Connection, caminho: str = None) -> str:
    """Exporta o faturamento por produto para um arquivo CSV."""
    caminho = caminho or (OUTPUT_DIR / "faturamento_por_produto.csv")
    linhas = queries.faturamento_por_produto(conexao)

    try:
        with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["produto", "faturamento"])
            for linha in linhas:
                escritor.writerow([linha["produto"], linha["faturamento"]])
        return str(caminho)
    except OSError as erro:
        raise RuntimeError(f"Erro ao exportar CSV: {erro}") from erro


def gerar_grafico_faturamento(conexao: sqlite3.Connection, caminho: str = None) -> str:
    """Gera um grafico de barras do faturamento por produto (requer matplotlib)."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as erro:
        raise RuntimeError(
            "matplotlib nao esta instalado. Rode: pip install matplotlib"
        ) from erro

    caminho = caminho or (OUTPUT_DIR / "faturamento_por_produto.png")
    linhas = queries.faturamento_por_produto(conexao)
    produtos = [linha["produto"] for linha in linhas]
    valores = [linha["faturamento"] for linha in linhas]

    plt.figure(figsize=(8, 5))
    plt.bar(produtos, valores, color="#4C72B0")
    plt.title("Faturamento por produto")
    plt.ylabel("Faturamento (R$)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()
    return str(caminho)
