-- =========================================================
-- seed.sql
-- Dados de exemplo: 5+ clientes, 5+ produtos, pedidos e itens
-- =========================================================

-- Clientes (Personagens de Star Wars)
INSERT INTO clientes (nome, email, cidade) VALUES
('Luke Skywalker',   'luke.skywalker@jedi.org',    'Tatooine'),
('Leia Organa',      'leia.organa@rebellion.gov',  'Alderaan'),
('Han Solo',         'han.solo@falcon.space',      'Corellia'),
('Darth Vader',      'darth.vader@empire.gov',     'Coruscant'),
('Obi-Wan Kenobi',   'obiwan.kenobi@jedi.org',     'Stewjon'),
('Lando Calrissian', 'lando@cloudcity.io',         'Socorro');

-- Produtos (Álbuns e CDs de Rock)
INSERT INTO produtos (nome, categoria, preco, estoque) VALUES
('The Dark Side of the Moon - Pink Floyd', 'Rock Progressivo',  120.00, 45),
('Back in Black - AC/DC',                  'Hard Rock',          95.00, 80),
('Led Zeppelin IV - Led Zeppelin',         'Hard Rock',         110.00, 30),
('Nevermind - Nirvana',                    'Grunge',             85.00, 60),
('Abbey Road - The Beatles',               'Rock Clássico',     130.00, 25),
('Master of Puppets - Metallica',          'Heavy Metal',        99.90, 50);

-- Pedidos (Inalterados em FKs e datas)
INSERT INTO pedidos (id_cliente, data_pedido, status) VALUES
(1, '2026-06-01', 'concluido'),
(2, '2026-06-03', 'concluido'),
(1, '2026-06-10', 'concluido'),
(3, '2026-06-12', 'concluido'),
(4, '2026-06-15', 'pendente'),
(5, '2026-06-18', 'concluido'),
(2, '2026-06-20', 'concluido');

-- Itens dos pedidos (Com preços de CDs de Rock e +15 novas vendas)
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unit) VALUES
-- Registros Originais Ajustados (11 itens)
(1, 1, 1, 120.00), -- Dark Side of the Moon
(1, 2, 2,  95.00), -- Back in Black
(2, 5, 1, 130.00), -- Abbey Road
(2, 6, 1,  99.90), -- Master of Puppets
(3, 3, 2, 110.00), -- Led Zeppelin IV
(4, 4, 1,  85.00), -- Nevermind
(4, 2, 3,  95.00), -- Back in Black
(5, 1, 1, 120.00), -- Dark Side of the Moon
(6, 6, 2,  99.90), -- Master of Puppets
(7, 5, 2, 130.00), -- Abbey Road
(7, 3, 1, 110.00), -- Led Zeppelin IV
(1, 4, 1,  85.00), -- Nevermind
(1, 5, 1, 130.00), -- Abbey Road
(2, 1, 2, 120.00), -- Dark Side of the Moon
(2, 3, 1, 110.00), -- Led Zeppelin IV
(3, 2, 1,  95.00), -- Back in Black
(3, 6, 1,  99.90), -- Master of Puppets
(4, 1, 1, 120.00), -- Dark Side of the Moon
(4, 5, 2, 130.00), -- Abbey Road
(5, 2, 1,  95.00), -- Back in Black
(5, 3, 1, 110.00), -- Led Zeppelin IV
(5, 4, 2,  85.00), -- Nevermind
(6, 1, 1, 120.00), -- Dark Side of the Moon
(6, 3, 1, 110.00), -- Led Zeppelin IV
(7, 4, 3,  85.00), -- Nevermind
(7, 6, 1,  99.90); -- Master of Puppets