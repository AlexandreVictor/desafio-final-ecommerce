"""
test_main.py
Testes para main.py (executar_opcao, menu).
Usa mocks para simular entradas do usuario.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import sqlite3
from unittest.mock import patch, MagicMock
import pytest

from main import executar_opcao, menu


# ── menu ──────────────────────────────────────────────────────────────────────

class TestMenu:
    def test_menu_exibe_opcoes(self, capsys):
        menu()
        saida = capsys.readouterr().out
        assert "1. Pedidos de um cliente" in saida
        assert "2. Produto mais vendido" in saida
        assert "3. Quantidade de pedidos por cliente" in saida
        assert "4. Ticket medio dos pedidos" in saida
        assert "5. Resumo de gastos por cliente" in saida
        assert "6. Produtos com estoque baixo" in saida
        assert "7. Cadastrar novo produto" in saida
        assert "8. Cadastrar novo pedido" in saida
        assert "9. Exportar faturamento para CSV" in saida
        assert "10. Gerar grafico de faturamento" in saida
        assert "0. Sair" in saida


# ── Opcao 1: Pedidos por cliente ─────────────────────────────────────────────

class TestOpcao1PedidosPorCliente:
    def test_opcao1_com_dados(self, conexao, capsys):
        with patch("builtins.input", return_value="Luke"):
            executar_opcao(conexao, "1")
        saida = capsys.readouterr().out
        assert "Luke" in saida

    def test_opcao1_cliente_inexistente(self, conexao, capsys):
        with patch("builtins.input", return_value="NaoExiste"):
            executar_opcao(conexao, "1")
        saida = capsys.readouterr().out
        assert "Nenhum resultado encontrado" in saida


# ── Opcao 2: Produto mais vendido ────────────────────────────────────────────

class TestOpcao2ProdutoMaisVendido:
    def test_opcao2_com_dados(self, conexao, capsys):
        executar_opcao(conexao, "2")
        saida = capsys.readouterr().out
        assert len(saida.strip()) > 0


# ── Opcao 3: Quantidade de pedidos por cliente ──────────────────────────────

class TestOpcao3PedidosPorCliente:
    def test_opcao3_com_dados(self, conexao, capsys):
        executar_opcao(conexao, "3")
        saida = capsys.readouterr().out
        assert len(saida.strip()) > 0


# ── Opcao 4: Ticket medio ───────────────────────────────────────────────────

class TestOpcao4TicketMedio:
    def test_opcao4_com_dados(self, conexao, capsys):
        executar_opcao(conexao, "4")
        saida = capsys.readouterr().out
        assert "Ticket medio" in saida

    def test_opcao4_banco_vazio(self, conexao_vazia, capsys):
        executar_opcao(conexao_vazia, "4")
        saida = capsys.readouterr().out
        assert "Sem pedidos registrados" in saida


# ── Opcao 5: Resumo de gastos por cliente ───────────────────────────────────

class TestOpcao5ResumoClientes:
    def test_opcao5_com_dados(self, conexao, capsys):
        executar_opcao(conexao, "5")
        saida = capsys.readouterr().out
        assert len(saida.strip()) > 0


# ── Opcao 6: Produtos com estoque baixo ─────────────────────────────────────

class TestOpcao6EstoqueBaixo:
    def test_opcao6_limite_padrao(self, conexao, capsys):
        with patch("builtins.input", return_value=""):
            executar_opcao(conexao, "6")
        saida = capsys.readouterr().out
        assert len(saida.strip()) > 0

    def test_opcao6_limite_customizado(self, conexao, capsys):
        with patch("builtins.input", return_value="100"):
            executar_opcao(conexao, "6")
        saida = capsys.readouterr().out
        assert len(saida.strip()) > 0

    def test_opcao6_input_invalido(self, conexao, capsys):
        with patch("builtins.input", return_value="abc"):
            executar_opcao(conexao, "6")
        saida = capsys.readouterr().out
        assert "Ocorreu um erro" in saida


# ── Opcao 7: Cadastrar novo produto ─────────────────────────────────────────

class TestOpcao7CadastrarProduto:
    def test_opcao7_sucesso(self, conexao, capsys):
        inputs = ["Violao", "Instrumentos", "350.00", "10"]
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao, "7")
        saida = capsys.readouterr().out
        assert "cadastrado com id" in saida

    def test_opcao7_preco_invalido(self, conexao, capsys):
        inputs = ["Violao", "Instrumentos", "abc", "10"]
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao, "7")
        saida = capsys.readouterr().out
        assert "Ocorreu um erro" in saida

    def test_opcao7_estoque_invalido(self, conexao, capsys):
        inputs = ["Violao", "Instrumentos", "350.00", "abc"]
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao, "7")
        saida = capsys.readouterr().out
        assert "Ocorreu um erro" in saida


# ── Opcao 8: Cadastrar novo pedido ──────────────────────────────────────────

class TestOpcao8CadastrarPedido:
    def test_opcao8_sucesso(self, conexao, capsys):
        inputs = ["1", "1", "2", ""]
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao, "8")
        saida = capsys.readouterr().out
        assert "cadastrado com id" in saida

    def test_opcao8_cancelado_sem_itens(self, conexao, capsys):
        inputs = ["1", ""]
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao, "8")
        saida = capsys.readouterr().out
        assert "pedido cancelado" in saida

    def test_opcao8_multiplos_itens(self, conexao, capsys):
        inputs = ["1", "1", "2", "3", "1", ""]
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao, "8")
        saida = capsys.readouterr().out
        assert "cadastrado com id" in saida

    def test_opcao8_id_cliente_invalido(self, conexao, capsys):
        with patch("builtins.input", side_effect=["abc", ""]):
            executar_opcao(conexao, "8")
        saida = capsys.readouterr().out
        assert "Ocorreu um erro" in saida


# ── Opcao 9: Exportar CSV ───────────────────────────────────────────────────

class TestOpcao9ExportarCSV:
    def test_opcao9_sucesso(self, conexao, capsys):
        executar_opcao(conexao, "9")
        saida = capsys.readouterr().out
        assert "CSV exportado em" in saida


# ── Opcao 10: Gerar grafico ─────────────────────────────────────────────────

class TestOpcao10GerarGrafico:
    def test_opcao10_sucesso(self, conexao, capsys):
        executar_opcao(conexao, "10")
        saida = capsys.readouterr().out
        assert "Grafico gerado em" in saida


# ── Opcao invalida ──────────────────────────────────────────────────────────

class TestOpcaoInvalida:
    def test_opcao_abc(self, conexao, capsys):
        executar_opcao(conexao, "abc")
        saida = capsys.readouterr().out
        assert "Opcao invalida" in saida

    def test_opcao_99(self, conexao, capsys):
        executar_opcao(conexao, "99")
        saida = capsys.readouterr().out
        assert "Opcao invalida" in saida

    def test_opcao_vazio(self, conexao, capsys):
        executar_opcao(conexao, "")
        saida = capsys.readouterr().out
        assert "Opcao invalida" in saida
