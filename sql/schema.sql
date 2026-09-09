-- =========================================================
-- schema.sql
-- Estrutura do banco de dados da loja (SQLite)
-- 4 tabelas relacionadas: clientes, produtos, pedidos, itens_pedido
-- =========================================================

PRAGMA foreign_keys = ON;

-- Apaga as tabelas existentes para recriá-las
DROP TABLE IF EXISTS itens_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;

-- Criação das tabelas
------------------------------------
-- Tabela clientes: Armazena informações dos clientes da loja.
------------------------------------
CREATE TABLE clientes (
    id_cliente   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL,
    email        TEXT NOT NULL UNIQUE,
    cidade       TEXT NOT NULL,
    data_cadastro TEXT NOT NULL DEFAULT (date('now'))
);
------------------------------------
-- Tabela produtos: Armazena informações dos produtos disponíveis na loja.
------------------------------------
CREATE TABLE produtos (
    id_produto   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL,
    categoria    TEXT NOT NULL,
    preco        REAL NOT NULL CHECK (preco >= 0),
    estoque      INTEGER NOT NULL DEFAULT 0
);
------------------------------------
-- Tabela pedidos: Armazena informações dos pedidos realizados na loja.
------------------------------------
CREATE TABLE pedidos (
    id_pedido    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente   INTEGER NOT NULL,
    data_pedido  TEXT NOT NULL DEFAULT (date('now')),
    status       TEXT NOT NULL DEFAULT 'concluido',
    FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
        ON DELETE CASCADE
);
------------------------------------
-- Tabela itens_pedido: Armazena informações sobre os itens incluídos em cada pedido.
------------------------------------
CREATE TABLE itens_pedido (
    id_item      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido    INTEGER NOT NULL,
    id_produto   INTEGER NOT NULL,
    quantidade   INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unit   REAL NOT NULL,
    FOREIGN KEY (id_pedido)  REFERENCES pedidos  (id_pedido)  ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produtos (id_produto) ON DELETE RESTRICT
);

-- View: resumo de gastos por cliente (agregação elaborada)
CREATE VIEW IF NOT EXISTS vw_resumo_clientes AS
SELECT
    c.id_cliente,
    c.nome,
    c.cidade,
    COUNT(DISTINCT p.id_pedido)                     AS total_pedidos,
    COALESCE(SUM(ip.quantidade * ip.preco_unit), 0) AS total_gasto
FROM clientes c
LEFT JOIN pedidos p       ON p.id_cliente = c.id_cliente
LEFT JOIN itens_pedido ip ON ip.id_pedido = p.id_pedido
GROUP BY c.id_cliente, c.nome, c.cidade;
