"""
test_queries.py
Testes para queries.py (todas as funcoes de consulta).
Usa banco in-memory com schema e seed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import queries


# ── listar_pedidos_por_cliente ────────────────────────────────────────────────

class TestListarPedidosPorCliente:
    def test_cliente_com_pedidos(self, conexao):
        resultado = queries.listar_pedidos_por_cliente(conexao, "Luke")
        assert len(resultado) > 0
        for row in resultado:
            assert "Luke" in row["cliente"]

    def test_cliente_sem_pedidos(self, conexao):
        resultado = queries.listar_pedidos_por_cliente(conexao, "NaoExiste")
        assert len(resultado) == 0

    def test_busca_parcial_nome(self, conexao):
        resultado = queries.listar_pedidos_por_cliente(conexao, "Solo")
        assert len(resultado) > 0
        for row in resultado:
            assert "Han Solo" in row["cliente"]

    def test_colunas_retornadas(self, conexao):
        resultado = queries.listar_pedidos_por_cliente(conexao, "Luke")
        assert len(resultado) > 0
        row = resultado[0]
        assert "id_pedido" in row.keys()
        assert "cliente" in row.keys()
        assert "produto" in row.keys()
        assert "quantidade" in row.keys()
        assert "preco_unit" in row.keys()
        assert "subtotal" in row.keys()

    def test_subtotal_calculado(self, conexao):
        resultado = queries.listar_pedidos_por_cliente(conexao, "Luke")
        for row in resultado:
            assert row["subtotal"] == row["quantidade"] * row["preco_unit"]


# ── produto_mais_vendido ─────────────────────────────────────────────────────

class TestProdutoMaisVendido:
    def test_retorna_resultados(self, conexao):
        resultado = queries.produto_mais_vendido(conexao)
        assert len(resultado) > 0

    def test_colunas_retornadas(self, conexao):
        resultado = queries.produto_mais_vendido(conexao)
        row = resultado[0]
        assert "produto" in row.keys()
        assert "qtd_vendas" in row.keys()
        assert "faturamento" in row.keys()

    def test_ordenado_por_vendas_desc(self, conexao):
        resultado = queries.produto_mais_vendido(conexao)
        vendas = [r["qtd_vendas"] for r in resultado]
        assert vendas == sorted(vendas, reverse=True)


# ── pedidos_por_cliente ──────────────────────────────────────────────────────

class TestPedidosPorCliente:
    def test_retorna_resultados(self, conexao):
        resultado = queries.pedidos_por_cliente(conexao)
        assert len(resultado) > 0

    def test_colunas_retornadas(self, conexao):
        resultado = queries.pedidos_por_cliente(conexao)
        row = resultado[0]
        assert "cliente" in row.keys()
        assert "qtd_pedidos" in row.keys()

    def test_ordenado_por_qtd_pedidos_desc(self, conexao):
        resultado = queries.pedidos_por_cliente(conexao)
        qtds = [r["qtd_pedidos"] for r in resultado]
        assert qtds == sorted(qtds, reverse=True)

    def test_todos_clientes_aparecem(self, conexao):
        resultado = queries.pedidos_por_cliente(conexao)
        nomes = {r["cliente"] for r in resultado}
        assert "Luke Skywalker" in nomes
        assert "Leia Organa" in nomes
        assert "Han Solo" in nomes


# ── ticket_medio ─────────────────────────────────────────────────────────────

class TestTicketMedio:
    def test_retorna_ticket(self, conexao):
        resultado = queries.ticket_medio(conexao)
        assert resultado is not None
        assert resultado["ticket_medio"] is not None
        assert resultado["ticket_medio"] > 0

    def test_ticket_positivo(self, conexao):
        resultado = queries.ticket_medio(conexao)
        assert resultado["ticket_medio"] > 0

    def test_banco_vazio_retorna_none(self, conexao_vazia):
        resultado = queries.ticket_medio(conexao_vazia)
        assert resultado["ticket_medio"] is None


# ── resumo_clientes ──────────────────────────────────────────────────────────

class TestResumoClientes:
    def test_retorna_resultados(self, conexao):
        resultado = queries.resumo_clientes(conexao)
        assert len(resultado) > 0

    def test_colunas_retornadas(self, conexao):
        resultado = queries.resumo_clientes(conexao)
        row = resultado[0]
        assert "id_cliente" in row.keys()
        assert "nome" in row.keys()
        assert "cidade" in row.keys()
        assert "total_pedidos" in row.keys()
        assert "total_gasto" in row.keys()

    def test_ordenado_por_total_gasto_desc(self, conexao):
        resultado = queries.resumo_clientes(conexao)
        gastos = [r["total_gasto"] for r in resultado]
        assert gastos == sorted(gastos, reverse=True)

    def test_todos_clientes_aparecem(self, conexao):
        resultado = queries.resumo_clientes(conexao)
        nomes = {r["nome"] for r in resultado}
        assert "Luke Skywalker" in nomes
        assert "Leia Organa" in nomes

    def test_cliente_sem_pedido_tem_zero(self, conexao):
        resultado = queries.resumo_clientes(conexao)
        for row in resultado:
            assert row["total_gasto"] >= 0


# ── produtos_com_estoque_baixo ───────────────────────────────────────────────

class TestProdutosComEstoqueBaixo:
    def test_limite_padrao(self, conexao):
        resultado = queries.produtos_com_estoque_baixo(conexao)
        for row in resultado:
            assert row["estoque"] < 25

    def test_limite_customizado(self, conexao):
        resultado = queries.produtos_com_estoque_baixo(conexao, 50)
        for row in resultado:
            assert row["estoque"] < 50

    def test_limite_grande(self, conexao):
        resultado = queries.produtos_com_estoque_baixo(conexao, 1000)
        assert len(resultado) > 0

    def test_limite_zero(self, conexao):
        resultado = queries.produtos_com_estoque_baixo(conexao, 0)
        assert len(resultado) == 0

    def test_colunas_retornadas(self, conexao):
        resultado = queries.produtos_com_estoque_baixo(conexao)
        if len(resultado) > 0:
            row = resultado[0]
            assert "nome" in row.keys()
            assert "categoria" in row.keys()
            assert "estoque" in row.keys()


# ── faturamento_por_produto ──────────────────────────────────────────────────

class TestFaturamentoPorProduto:
    def test_retorna_resultados(self, conexao):
        resultado = queries.faturamento_por_produto(conexao)
        assert len(resultado) > 0

    def test_colunas_retornadas(self, conexao):
        resultado = queries.faturamento_por_produto(conexao)
        row = resultado[0]
        assert "produto" in row.keys()
        assert "faturamento" in row.keys()

    def test_ordenado_por_faturamento_desc(self, conexao):
        resultado = queries.faturamento_por_produto(conexao)
        fats = [r["faturamento"] for r in resultado]
        assert fats == sorted(fats, reverse=True)

    def test_valores_positivos(self, conexao):
        resultado = queries.faturamento_por_produto(conexao)
        for row in resultado:
            assert row["faturamento"] > 0
