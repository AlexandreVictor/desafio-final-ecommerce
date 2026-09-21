"""
test_utils.py
Testes para utils.py (imprimir_tabela).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from utils import imprimir_tabela


class TestImprimirTabela:
    def test_lista_vazia(self, capsys):
        imprimir_tabela([], ["col1", "col2"])
        saida = capsys.readouterr().out
        assert "Nenhum resultado encontrado" in saida

    def test_lista_com_dados(self, capsys):
        linhas = [
            {"id": 1, "nome": "Alice"},
            {"id": 2, "nome": "Bob"},
        ]
        imprimir_tabela(linhas, ["id", "nome"])
        saida = capsys.readouterr().out
        assert "Alice" in saida
        assert "Bob" in saida

    def test_uma_unica_coluna(self, capsys):
        linhas = [{"nome": "Camisa"}]
        imprimir_tabela(linhas, ["nome"])
        saida = capsys.readouterr().out
        assert "Camisa" in saida

    def test_multiplas_colunas(self, capsys):
        linhas = [{"a": 1, "b": 2, "c": 3}]
        imprimir_tabela(linhas, ["a", "b", "c"])
        saida = capsys.readouterr().out
        assert "1" in saida
        assert "2" in saida
        assert "3" in saida
