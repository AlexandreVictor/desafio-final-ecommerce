-- =========================================================
-- queries.sql
-- Consultas de referencia (as mesmas usadas em src/queries.py)
-- =========================================================

-- 1) JOIN + WHERE: pedidos de um cliente especifico com detalhes dos produtos
SELECT p.id_pedido, c.nome, pr.nome AS produto, ip.quantidade, ip.preco_unit
FROM pedidos p
JOIN clientes c        ON c.id_cliente = p.id_cliente
JOIN itens_pedido ip    ON ip.id_pedido = p.id_pedido
JOIN produtos pr        ON pr.id_produto = ip.id_produto
WHERE c.nome = 'Ana Souza';

-- 2) GROUP BY + SUM: faturamento total por produto
SELECT pr.nome, SUM(ip.quantidade * ip.preco_unit) AS faturamento
FROM itens_pedido ip
JOIN produtos pr ON pr.id_produto = ip.id_produto
GROUP BY pr.nome
ORDER BY faturamento DESC;

-- 3) GROUP BY + COUNT: quantidade de pedidos por cliente
SELECT c.nome, COUNT(p.id_pedido) AS qtd_pedidos
FROM clientes c
LEFT JOIN pedidos p ON p.id_cliente = c.id_cliente
GROUP BY c.nome
ORDER BY qtd_pedidos DESC;

-- 4) AVG: ticket medio (valor medio por pedido)
SELECT AVG(total_pedido) AS ticket_medio
FROM (
    SELECT p.id_pedido, SUM(ip.quantidade * ip.preco_unit) AS total_pedido
    FROM pedidos p
    JOIN itens_pedido ip ON ip.id_pedido = p.id_pedido
    GROUP BY p.id_pedido
);

-- 5) VIEW (definida em schema.sql): resumo por cliente
SELECT * FROM vw_resumo_clientes ORDER BY total_gasto DESC;
