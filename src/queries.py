"""
queries.py
Funcoes que executam as consultas (relatorios) no banco de dados.
Cada funcao recebe uma conexao sqlite3 ja aberta e devolve os resultados.
"""

import sqlite3


def listar_pedidos_por_cliente(conexao: sqlite3.Connection, nome_cliente: str):
    """Detalhes dos pedidos de um cliente especifico."""
    sql = """
        SELECT 
               p.id_pedido, 
               c.nome AS cliente, 
               pr.nome AS produto,
               ip.quantidade, 
               ip.preco_unit,
               (ip.quantidade * ip.preco_unit) AS subtotal
        FROM pedidos        p
        JOIN clientes       c  ON c.id_cliente = p.id_cliente
        JOIN itens_pedido   ip ON ip.id_pedido = p.id_pedido
        JOIN produtos       pr ON pr.id_produto = ip.id_produto
        WHERE c.nome LIKE ?
        ORDER BY p.id_pedido;
    """
    cursor = conexao.execute(sql, (f"%{nome_cliente}%",))
    return cursor.fetchall()


def produto_mais_vendido(conexao: sqlite3.Connection):
    """Produto mais vendido."""
    sql = """
        SELECT 
            pr.nome AS produto, 
            COUNT(*) AS qtd_vendas,
            SUM(ip.quantidade * ip.preco_unit) AS faturamento
        FROM itens_pedido ip
        JOIN produtos pr ON pr.id_produto = ip.id_produto
        GROUP BY pr.nome
        ORDER BY qtd_vendas DESC;
    """
    return conexao.execute(sql).fetchall()


def pedidos_por_cliente(conexao: sqlite3.Connection):
    """GROUP BY + COUNT: quantidade de pedidos por cliente."""
    sql = """
        SELECT c.nome AS cliente, COUNT(p.id_pedido) AS qtd_pedidos
        FROM clientes c
        LEFT JOIN pedidos p ON p.id_cliente = c.id_cliente
        GROUP BY c.nome
        ORDER BY qtd_pedidos DESC;
    """
    return conexao.execute(sql).fetchall()

#REFATORAR 
def ticket_medio(conexao: sqlite3.Connection):
    """AVG: valor medio gasto por pedido."""
    sql = """
        SELECT AVG(total_pedido) AS ticket_medio
        FROM (
            SELECT p.id_pedido, SUM(ip.quantidade * ip.preco_unit) AS total_pedido
            FROM pedidos p
            JOIN itens_pedido ip ON ip.id_pedido = p.id_pedido
            GROUP BY p.id_pedido
        );
    """
    return conexao.execute(sql).fetchone()


def resumo_clientes(conexao: sqlite3.Connection):
    """Usa a VIEW vw_resumo_clientes criada no schema.sql."""
    sql = "SELECT * FROM vw_resumo_clientes ORDER BY total_gasto DESC;"
    return conexao.execute(sql).fetchall()


def produtos_com_estoque_baixo(conexao: sqlite3.Connection, limite: int = 25):
    """WHERE simples: produtos com estoque abaixo de um limite."""
    sql = "SELECT nome, categoria, estoque FROM produtos WHERE estoque < ? ORDER BY estoque;"
    return conexao.execute(sql, (limite,)).fetchall()
