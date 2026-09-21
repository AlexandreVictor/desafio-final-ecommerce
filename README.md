# Desafio Final - E-Commerce

Sistema de gerenciamento de loja online desenvolvido em Python com interface de linha de comandos (CLI). O projeto gerencia uma loja de discos de rock, permitindo consultas de relatórios, cadastro de produtos e pedidos, e exportação de dados.

## Funcionalidades

- **Relatórios SQL**: 7 consultas distintas com JOINs, subqueries, aggregations e views
- **Cadastro de produtos**: inserção com validação e rollback automático
- **Cadastro de pedidos**: criação transacional com múltiplos itens
- **Exportação CSV**: dados de faturamento por produto
- **Gráfico de faturamento**: visualização em PNG com matplotlib
- **Tabelas formatadas**: exibição organizada no terminal com tabulate
- **Banco auto-inicializável**: schema + dados de exemplo carregados automaticamente

## Estrutura do Projeto

```
desafio-final-ecommerce/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── loja.db                        # Banco SQLite (gerado automaticamente)
├── sql/
│   ├── schema.sql                     # DDL - criação das tabelas e views
│   ├── seed.sql                       # Dados de exemplo
│   └── queries.sql                    # Consultas de referência
├── src/
│   ├── __init__.py
│   ├── main.py                        # Ponto de entrada - menu interativo
│   ├── database.py                    # Conexão e inicialização do banco
│   ├── queries.py                     # Funções de relatórios (7 consultas)
│   ├── cadastro.py                    # Cadastro de produtos e pedidos
│   ├── relatorios.py                  # Exportação CSV e geração de gráficos
│   └── utils.py                       # Utilitário de formatação de tabelas
└── tests/
    ├── conftest.py                    # Fixtures compartilhadas (banco in-memory)
    ├── test_main.py                   # Testes do menu principal
    ├── test_queries.py                # Testes das funções de relatório
    ├── test_cadastro.py               # Testes de cadastro
    ├── test_relatorios.py             # Testes de exportação
    └── test_utils.py                  # Testes do utilitário de tabelas
```

## Modelo de Dados

O banco SQLite possui **4 tabelas** e **1 view**:

```
┌──────────────┐       ┌──────────────┐
│   clientes   │       │   produtos   │
├──────────────┤       ├──────────────┤
│ id_cliente PK│       │ id_produto PK│
│ nome         │       │ nome         │
│ email   UQ   │       │ categoria    │
│ cidade       │       │ preco  CHECK │
│ data_cadastro│       │ estoque      │
└──────┬───────┘       └──────┬───────┘
       │                      │
       │ 1:N                  │ 1:N
       ▼                      ▼
┌──────────────┐       ┌──────────────┐
│   pedidos    │       │ itens_pedido │
├──────────────┤       ├──────────────┤
│ id_pedido PK │◄──────│ id_item PK   │
│ id_cliente FK│  N:1  │ id_pedido FK │
│ data_pedido  │       │ id_produto FK│
│ status       │       │ quantidade   │
└──────────────┘       │ preco_unit   │
                       └──────────────┘
```

- **clientes**: dados cadastrais dos clientes (nome, email, cidade)
- **produtos**: catálogo de produtos com preço e estoque
- **pedidos**: registro de pedidos vinculados a clientes
- **itens_pedido**: itens de cada pedido com quantidade e preço unitário
- **vw_resumo_clientes**: view agregada com total de pedidos e gastos por cliente

## Como Executar

### Pré-requisitos

- Python 3.11+

### Instalação

```bash
# Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
python src/main.py
```

O banco de dados (`data/loja.db`) é criado automaticamente na primeira execução com schema e dados de exemplo.

### Forçar recriação do banco

```bash
python src/database.py --forcar
```

### Menu Interativo

Ao executar, o usuário é apresentado com 10 opções:

| Opção | Descrição |
|-------|-----------|
| 1 | Pedidos de um cliente (busca por nome) |
| 2 | Produto mais vendido |
| 3 | Quantidade de pedidos por cliente |
| 4 | Ticket médio dos pedidos |
| 5 | Resumo de gastos por cliente (VIEW) |
| 6 | Produtos com estoque baixo |
| 7 | Cadastrar novo produto |
| 8 | Cadastrar novo pedido |
| 9 | Exportar faturamento para CSV |
| 10 | Gerar gráfico de faturamento (PNG) |
| 0 | Sair |

## Como Rodar os Testes

```bash
# Executar todos os testes
pytest

# Executar com saída detalhada
pytest -v

# Executar arquivo específico
pytest tests/test_queries.py
pytest tests/test_cadastro.py
pytest tests/test_relatorios.py
```

Os testes utilizam bancos SQLite **in-memory** (`:memory:`), sem necessidade de arquivos externos. A fixture compartilhada está em `tests/conftest.py`.

## Conceitos Praticados

### SQL
- **JOINs** (INNER JOIN, LEFT JOIN) para relacionar tabelas
- **Subqueries** para cálculos agregados (ticket médio)
- **GROUP BY** com funções de agregação (COUNT, SUM, AVG)
- **VIEW** para consulta resumida de clientes
- **CHECK constraints** para validação de dados
- **Foreign Keys** com CASCADE e RESTRICT
- **Transações** com COMMIT e ROLLBACK

### Python
- Programação orientada a objetos com módulos
- Tratamento de exceções e context managers (`with`)
- Formatação de strings e tabelas no terminal
- Manipulação de arquivos CSV
- Geração de gráficos com matplotlib

### Boas Práticas
- Separação de responsabilidades (queries, cadastro, relatórios, utils)
- Código todo em português (nomes de variáveis, funções, comentários)
- Dados de exemplo realistas (personagens Star Wars + álbuns de rock)
- Ambiente virtual isolado
- Controle de versão com Git e branches

### Testes
- Framework pytest com fixtures compartilhadas
- Banco de dados in-memory para testes isolados
- Mocking com `unittest.mock.patch` para simular inputs do usuário
- Uso de `capsys` para capturar saída do terminal
- Uso de `tmp_path` para arquivos temporários

## Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.11+ | Linguagem principal |
| SQLite3 | - | Banco de dados |
| pytest | >= 7.0 | Framework de testes |
| tabulate | >= 0.10.0 | Formatação de tabelas |
| matplotlib | >= 3.5 | Geração de gráficos |

## Autor

**Alexandre Victor Augusto**

Turma/Curso: Engenharia de Dados e Inteligência Artificial
