"""
test_cadastro.py
Testes para cadastro.py (cadastrar_produto, cadastrar_pedido).
Usa banco in-memory com schema (e seed opcional).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import sqlite3
import pytest
import cadastro


# ── cadastrar_produto ────────────────────────────────────────────────────────

class TestCadastrarProduto:
    def test_cadastrar_produto_sucesso(self, conexao):
        id_produto = cadastro.cadastrar_produto(
            conexao, "Violao", "Instrumentos", 350.00, 10
        )
        assert id_produto is not None
        assert id_produto > 0

    def test_produto_existe_no_banco(self, conexao):
        id_produto = cadastro.cadastrar_produto(
            conexao, "Bateria", "Instrumentos", 1500.00, 5
        )
        cursor = conexao.execute(
            "SELECT * FROM produtos WHERE id_produto = ?", (id_produto,)
        )
        row = cursor.fetchone()
        assert row is not None
        assert row["nome"] == "Bateria"
        assert row["categoria"] == "Instrumentos"
        assert row["preco"] == 1500.00
        assert row["estoque"] == 5

    def test_cadastrar_multiplos_produtos(self, conexao):
        id1 = cadastro.cadastrar_produto(conexao, "A", "Cat", 10.0, 1)
        id2 = cadastro.cadastrar_produto(conexao, "B", "Cat", 20.0, 2)
        assert id1 != id2

    def test_rollback_em_erro(self, conexao_vazia):
        conexao_vazia.execute("DROP TABLE IF EXISTS produtos")
        with pytest.raises(RuntimeError):
            cadastro.cadastrar_produto(
                conexao_vazia, "Teste", "Cat", 10.0, 1
            )


# ── cadastrar_pedido ─────────────────────────────────────────────────────────

class TestCadastrarPedido:
    def test_cadastrar_pedido_sucesso(self, conexao):
        itens = [(1, 2)]
        id_pedido = cadastro.cadastrar_pedido(conexao, 1, itens)
        assert id_pedido is not None
        assert id_pedido > 0

    def test_pedido_existe_no_banco(self, conexao):
        itens = [(1, 1)]
        id_pedido = cadastro.cadastrar_pedido(conexao, 1, itens)
        cursor = conexao.execute(
            "SELECT * FROM pedidos WHERE id_pedido = ?", (id_pedido,)
        )
        row = cursor.fetchone()
        assert row is not None
        assert row["id_cliente"] == 1

    def test_itens_pedido_salvos(self, conexao):
        itens = [(1, 3), (2, 1)]
        id_pedido = cadastro.cadastrar_pedido(conexao, 1, itens)
        cursor = conexao.execute(
            "SELECT COUNT(*) as cnt FROM itens_pedido WHERE id_pedido = ?",
            (id_pedido,),
        )
        assert cursor.fetchone()["cnt"] == 2

    def test_preco_unit_preenchido(self, conexao):
        itens = [(1, 1)]
        id_pedido = cadastro.cadastrar_pedido(conexao, 1, itens)
        cursor = conexao.execute(
            "SELECT preco_unit FROM itens_pedido WHERE id_pedido = ?",
            (id_pedido,),
        )
        row = cursor.fetchone()
        assert row["preco_unit"] > 0

    def test_produto_inexistente_erro(self, conexao):
        with pytest.raises(RuntimeError):
            cadastro.cadastrar_pedido(conexao, 1, [(9999, 1)])

    def test_cliente_inexistente_erro(self, conexao):
        with pytest.raises(RuntimeError):
            cadastro.cadastrar_pedido(conexao, 9999, [(1, 1)])

    def test_rollback_em_erro(self, conexao):
        with pytest.raises(RuntimeError):
            cadastro.cadastrar_pedido(conexao, 1, [(9999, 1)])
        cursor = conexao.execute("SELECT COUNT(*) as cnt FROM pedidos")
        # O pedido foi criado mas o rollback deve ter revertido
