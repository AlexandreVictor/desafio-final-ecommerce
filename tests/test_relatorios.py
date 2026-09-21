"""
test_relatorios.py
Testes para relatorios.py (exportar CSV, gerar grafico).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import csv
import os
import tempfile
import pytest
import relatorios


# ── exportar_faturamento_csv ─────────────────────────────────────────────────

class TestExportarFaturamentoCsv:
    def test_csv_criado(self, conexao, tmp_path):
        caminho = str(tmp_path / "faturamento.csv")
        resultado = relatorios.exportar_faturamento_csv(conexao, caminho)
        assert os.path.exists(resultado)

    def test_csv_conteudo(self, conexao, tmp_path):
        caminho = str(tmp_path / "faturamento.csv")
        resultado = relatorios.exportar_faturamento_csv(conexao, caminho)
        with open(resultado, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            linhas = list(reader)
        assert linhas[0] == ["produto", "faturamento"]
        assert len(linhas) > 1

    def test_csv_valores_numericos(self, conexao, tmp_path):
        caminho = str(tmp_path / "faturamento.csv")
        resultado = relatorios.exportar_faturamento_csv(conexao, caminho)
        with open(resultado, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                float(row["faturamento"])

    def test_csv_produtos_corretos(self, conexao, tmp_path):
        caminho = str(tmp_path / "faturamento.csv")
        resultado = relatorios.exportar_faturamento_csv(conexao, caminho)
        with open(resultado, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            produtos = [row["produto"] for row in reader]
        assert len(produtos) > 0

    def test_caminho_padrao(self, conexao):
        resultado = relatorios.exportar_faturamento_csv(conexao)
        assert os.path.exists(resultado)
        os.remove(resultado)


# ── gerar_grafico_faturamento ────────────────────────────────────────────────

class TestGerarGraficoFaturamento:
    def test_grafico_criado(self, conexao, tmp_path):
        caminho = str(tmp_path / "grafico.png")
        resultado = relatorios.gerar_grafico_faturamento(conexao, caminho)
        assert os.path.exists(resultado)

    def test_grafico_tamanho_minimo(self, conexao, tmp_path):
        caminho = str(tmp_path / "grafico.png")
        resultado = relatorios.gerar_grafico_faturamento(conexao, caminho)
        assert os.path.getsize(resultado) > 0

    def test_caminho_padrao(self, conexao):
        resultado = relatorios.gerar_grafico_faturamento(conexao)
        assert os.path.exists(resultado)
        os.remove(resultado)
