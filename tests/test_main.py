"""
test_main.py
Testes unitarios para todas as entradas do menu em src/main.py.
Usa pytest + monkeypatch para simular entradas do usuario e mockar chamadas ao banco.
"""

import sys
from pathlib import Path

# Garante que src/ esteja no sys.path para os imports fallback do main.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import sqlite3
from unittest.mock import patch, MagicMock, call
import pytest

from main import imprimir_tabela, executar_opcao, menu


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def conexao_mock():
    """Retorna uma conexao sqlite3 fake (in-memory) com Row factory."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    return conn


@pytest.fixture
def capsys_mock(capsys):
    """Facilita capturar saida do terminal."""
    return capsys


# ── imprimir_tabela ───────────────────────────────────────────────────────────

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
        assert "id | nome" in saida
        assert "1 | Alice" in saida
        assert "2 | Bob" in saida


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


# ── Opcao 1: Pedidos por cliente ──────────────────────────────────────────────

class TestOpcao1PedidosPorCliente:
    @patch("main.queries")
    def test_opcao1_sucesso(self, mock_queries, conexao_mock, capsys):
        mock_queries.listar_pedidos_por_cliente.return_value = [
            {"id_pedido": 1, "cliente": "Alice", "produto": "Camisa",
             "quantidade": 2, "preco_unit": 50.0, "subtotal": 100.0}
        ]
        with patch("builtins.input", return_value="Alice"):
            executar_opcao(conexao_mock, "1")
        saida = capsys.readouterr().out
        mock_queries.listar_pedidos_por_cliente.assert_called_once_with(conexao_mock, "Alice")
        assert "Alice" in saida
        assert "Camisa" in saida

    @patch("main.queries")
    def test_opcao1_nenhumResultado(self, mock_queries, conexao_mock, capsys):
        mock_queries.listar_pedidos_por_cliente.return_value = []
        with patch("builtins.input", return_value="NaoExiste"):
            executar_opcao(conexao_mock, "1")
        saida = capsys.readouterr().out
        assert "Nenhum resultado encontrado" in saida


# ── Opcao 2: Produto mais vendido ─────────────────────────────────────────────

class TestOpcao2ProdutoMaisVendido:
    @patch("main.queries")
    def test_opcao2_sucesso(self, mock_queries, conexao_mock, capsys):
        mock_queries.produto_mais_vendido.return_value = [
            {"produto": "Camisa", "qtd_vendas": 15, "faturamento": 750.0}
        ]
        executar_opcao(conexao_mock, "2")
        saida = capsys.readouterr().out
        mock_queries.produto_mais_vendido.assert_called_once_with(conexao_mock)
        assert "Camisa" in saida
        assert "15" in saida

    @patch("main.queries")
    def test_opcao2_semVendas(self, mock_queries, conexao_mock, capsys):
        mock_queries.produto_mais_vendido.return_value = []
        executar_opcao(conexao_mock, "2")
        saida = capsys.readouterr().out
        assert "Nenhum resultado encontrado" in saida


# ── Opcao 3: Quantidade de pedidos por cliente ────────────────────────────────

class TestOpcao3PedidosPorCliente:
    def test_opcao3_erroVariavelNaoDefinida(self, conexao_mock, capsys):
        """A opcao 3 tem um bug: 'linhas' nao esta definida. Deve lancar NameError."""
        with pytest.raises(NameError):
            executar_opcao(conexao_mock, "3")


# ── Opcao 4: Ticket medio ─────────────────────────────────────────────────────

class TestOpcao4TicketMedio:
    def test_opcao4_erroTipoInvalido(self, conexao_mock, capsys):
        """A opcao 4 tem um bug: tenta acessar indice de lista vazia como dict. Deve lancar TypeError."""
        with pytest.raises(TypeError):
            executar_opcao(conexao_mock, "4")


# ── Opcao 5: Resumo de gastos por cliente ─────────────────────────────────────

class TestOpcao5ResumoClientes:
    @patch("main.queries")
    def test_opcao5_listaVazia(self, mock_queries, conexao_mock, capsys):
        """A opcao 5 usa lista vazia hardcoded, resultado sempre sera vazio."""
        executar_opcao(conexao_mock, "5")
        saida = capsys.readouterr().out
        assert "Nenhum resultado encontrado" in saida


# ── Opcao 6: Produtos com estoque baixo ───────────────────────────────────────

class TestOpcao6EstoqueBaixo:
    @patch("main.queries")
    def test_opcao6_limitePadrao(self, mock_queries, conexao_mock, capsys):
        mock_queries.produtos_com_estoque_baixo.return_value = [
            {"nome": "Caneta", "categoria": "Papelaria", "estoque": 10}
        ]
        with patch("builtins.input", return_value=""):
            executar_opcao(conexao_mock, "6")
        saida = capsys.readouterr().out
        mock_queries.produtos_com_estoque_baixo.assert_called_once_with(conexao_mock, 25)
        assert "Caneta" in saida

    @patch("main.queries")
    def test_opcao6_limiteCustomizado(self, mock_queries, conexao_mock, capsys):
        mock_queries.produtos_com_estoque_baixo.return_value = []
        with patch("builtins.input", return_value="50"):
            executar_opcao(conexao_mock, "6")
        mock_queries.produtos_com_estoque_baixo.assert_called_once_with(conexao_mock, 50)

    @patch("main.queries")
    def test_opcao6_inputInvalido(self, mock_queries, conexao_mock, capsys):
        with patch("builtins.input", return_value="abc"):
            executar_opcao(conexao_mock, "6")
        saida = capsys.readouterr().out
        assert "Ocorreu um erro" in saida


# ── Opcao 7: Cadastrar novo produto ───────────────────────────────────────────

class TestOpcao7CadastrarProduto:
    @patch("main.cadastro")
    def test_opcao7_sucesso(self, mock_cadastro, conexao_mock, capsys):
        mock_cadastro.cadastrar_produto.return_value = 1
        inputs = ["Camisa", "Vestuario", "59.90", "100"]
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao_mock, "7")
        saida = capsys.readouterr().out
        mock_cadastro.cadastrar_produto.assert_called_once_with(
            conexao_mock, "Camisa", "Vestuario", 59.90, 100
        )
        assert "id 1" in saida

    @patch("main.cadastro")
    def test_opcao7_precoInvalido(self, mock_cadastro, conexao_mock, capsys):
        inputs = ["Camisa", "Vestuario", "abc", "100"]
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao_mock, "7")
        saida = capsys.readouterr().out
        assert "Ocorreu um erro" in saida
        mock_cadastro.cadastrar_produto.assert_not_called()

    @patch("main.cadastro")
    def test_opcao7_estoqueInvalido(self, mock_cadastro, conexao_mock, capsys):
        inputs = ["Camisa", "Vestuario", "59.90", "abc"]
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao_mock, "7")
        saida = capsys.readouterr().out
        assert "Ocorreu um erro" in saida
        mock_cadastro.cadastrar_produto.assert_not_called()


# ── Opcao 8: Cadastrar novo pedido ────────────────────────────────────────────

class TestOpcao8CadastrarPedido:
    @patch("main.cadastro")
    def test_opcao8_sucesso(self, mock_cadastro, conexao_mock, capsys):
        mock_cadastro.cadastrar_pedido.return_value = 1
        inputs = ["1", "10", "2", ""]  # id_cliente, id_produto, qtd, vazio pra sair
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao_mock, "8")
        saida = capsys.readouterr().out
        mock_cadastro.cadastrar_pedido.assert_called_once_with(conexao_mock, 1, [(10, 2)])
        assert "id 1" in saida

    @patch("main.cadastro")
    def test_opcao8_canceladoSemItens(self, mock_cadastro, conexao_mock, capsys):
        inputs = ["1", ""]  # id_cliente, vazio direto
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao_mock, "8")
        saida = capsys.readouterr().out
        assert "pedido cancelado" in saida
        mock_cadastro.cadastrar_pedido.assert_not_called()

    @patch("main.cadastro")
    def test_opcao8MultiplosItens(self, mock_cadastro, conexao_mock, capsys):
        mock_cadastro.cadastrar_pedido.return_value = 2
        inputs = ["1", "10", "2", "20", "3", ""]
        with patch("builtins.input", side_effect=inputs):
            executar_opcao(conexao_mock, "8")
        mock_cadastro.cadastrar_pedido.assert_called_once_with(conexao_mock, 1, [(10, 2), (20, 3)])

    def test_opcao8_idClienteInvalido(self, conexao_mock, capsys):
        with patch("builtins.input", side_effect=["abc", ""]):
            executar_opcao(conexao_mock, "8")
        saida = capsys.readouterr().out
        assert "Ocorreu um erro" in saida


# ── Opcao 9: Exportar CSV ─────────────────────────────────────────────────────

class TestOpcao9ExportarCSV:
    @patch("main.relatorios", create=True)
    def test_opcao9_sucesso(self, mock_relatorios, conexao_mock, capsys):
        mock_relatorios.exportar_faturamento_csv.return_value = "/tmp/faturamento.csv"
        executar_opcao(conexao_mock, "9")
        saida = capsys.readouterr().out
        mock_relatorios.exportar_faturamento_csv.assert_called_once_with(conexao_mock)
        assert "/tmp/faturamento.csv" in saida


# ── Opcao 10: Gerar grafico ───────────────────────────────────────────────────

class TestOpcao10GerarGrafico:
    @patch("main.relatorios", create=True)
    def test_opcao10_sucesso(self, mock_relatorios, conexao_mock, capsys):
        mock_relatorios.gerar_grafico_faturamento.return_value = "/tmp/faturamento.png"
        executar_opcao(conexao_mock, "10")
        saida = capsys.readouterr().out
        mock_relatorios.gerar_grafico_faturamento.assert_called_once_with(conexao_mock)
        assert "/tmp/faturamento.png" in saida


# ── Opcao 0: Sair ─────────────────────────────────────────────────────────────

class TestOpcao0Sair:
    def test_opcao_invalida(self, conexao_mock, capsys):
        executar_opcao(conexao_mock, "0")
        saida = capsys.readouterr().out
        assert "Opcao invalida" in saida


# ── Opcao invalida ────────────────────────────────────────────────────────────

class TestOpcaoInvalida:
    def test_opcao_abc(self, conexao_mock, capsys):
        executar_opcao(conexao_mock, "abc")
        saida = capsys.readouterr().out
        assert "Opcao invalida" in saida

    def test_opcao_99(self, conexao_mock, capsys):
        executar_opcao(conexao_mock, "99")
        saida = capsys.readouterr().out
        assert "Opcao invalida" in saida

    def test_opcao_vazio(self, conexao_mock, capsys):
        executar_opcao(conexao_mock, "")
        saida = capsys.readouterr().out
        assert "Opcao invalida" in saida
