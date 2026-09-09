"""
cadastro.py
Funcoes de cadastro (INSERT)
e novos pedidos (com itens) via Python.
"""

import sqlite3


def cadastrar_produto(conexao: sqlite3.Connection, nome: str, categoria: str,
                       preco: float, estoque: int) -> int:
    """Insere um novo produto e retorna o id gerado."""
    sql = "INSERT INTO produtos (nome, categoria, preco, estoque) VALUES (?, ?, ?, ?);"
    try:
        cursor = conexao.execute(sql, (nome, categoria, preco, estoque))
        conexao.commit()
        return cursor.lastrowid
    except sqlite3.Error as erro:
        conexao.rollback()
        raise RuntimeError(f"Erro ao cadastrar produto: {erro}") from erro


def cadastrar_pedido(conexao: sqlite3.Connection, id_cliente: int,
                      itens: list[tuple[int, int]]) -> int:
    """
    Cria um novo pedido para um cliente.
    itens: lista de tuplas (id_produto, quantidade).
    Retorna o id do pedido criado.
    """
    try:
        cursor = conexao.execute(
            "INSERT INTO pedidos (id_cliente) VALUES (?);", (id_cliente,)
        )
        id_pedido = cursor.lastrowid

        for id_produto, quantidade in itens:
            preco = conexao.execute(
                "SELECT preco FROM produtos WHERE id_produto = ?;", (id_produto,)
            ).fetchone()
            if preco is None:
                raise ValueError(f"Produto id={id_produto} nao encontrado.")
            conexao.execute(
                """INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unit)
                   VALUES (?, ?, ?, ?);""",
                (id_pedido, id_produto, quantidade, preco["preco"]),
            )

        conexao.commit()
        return id_pedido
    except (sqlite3.Error, ValueError) as erro:
        conexao.rollback()
        raise RuntimeError(f"Erro ao cadastrar pedido: {erro}") from erro
