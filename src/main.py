"""
main.py
Ponto de entrada da aplicacao: exibe um menu no terminal para o usuario
escolher qual relatorio deseja ver, alem de opcoes de cadastro (bonus).
"""

import sqlite3
import sys

# Permite rodar "python src/main.py" diretamente (sem -m)
import cadastro
import database
import queries
import relatorios
from utils import imprimir_tabela


def menu() -> None:
    opcoes = """
========== RELATORIOS DA LOJA ==========
1. Pedidos de um cliente (busca por nome)
2. Produto mais vendido
3. Quantidade de pedidos por cliente
4. Ticket medio dos pedidos
5. Resumo de gastos por cliente (VIEW)
6. Produtos com estoque baixo
7. Cadastrar novo produto
8. Cadastrar novo pedido
9. Exportar faturamento para CSV*
10. Gerar grafico de faturamento (PNG)*
0. Sair
=========================================
"""
    print(opcoes)


def executar_opcao(conexao: sqlite3.Connection, opcao: str) -> None:
    try:
        if opcao == "1":
            nome = input("Digite o nome (ou parte do nome) do cliente: ").strip()
            linhas = queries.listar_pedidos_por_cliente(conexao, nome)
            imprimir_tabela(linhas, ["id_pedido", "cliente", "produto", "quantidade", "preco_unit", "subtotal"])

        elif opcao == "2":
            linhas = queries.produto_mais_vendido(conexao)
            imprimir_tabela(linhas, ["produto", "qtd_vendas", "faturamento"])

        elif opcao == "3":
            linhas = queries.pedidos_por_cliente(conexao)
            imprimir_tabela(linhas, ["cliente", "qtd_pedidos"])

        elif opcao == "4":
            resultado = queries.ticket_medio(conexao)
            valor = resultado["ticket_medio"]
            print(f"Ticket medio: R$ {valor:.2f}\n" if valor else "Sem pedidos registrados.\n")

        elif opcao == "5":
            linhas = queries.resumo_clientes(conexao)
            imprimir_tabela(linhas, ["id_cliente", "nome", "cidade", "total_pedidos", "total_gasto"])

        elif opcao == "6":
            limite = input("Estoque abaixo de quanto? (padrao 25): ").strip()
            limite = int(limite) if limite else 25
            linhas = queries.produtos_com_estoque_baixo(conexao, limite)
            imprimir_tabela(linhas, ["nome", "categoria", "estoque"])

        elif opcao == "7":
            nome = input("Nome do produto: ").strip()
            categoria = input("Categoria: ").strip()
            preco = float(input("Preco: ").strip())
            estoque = int(input("Estoque inicial: ").strip())
            id_produto = cadastro.cadastrar_produto(conexao, nome, categoria, preco, estoque)
            print(f"Produto cadastrado com id {id_produto}.\n")

        elif opcao == "8":
            id_cliente = int(input("Id do cliente: ").strip())
            itens = []
            print("Digite os itens do pedido (id_produto e quantidade). Deixe id_produto vazio para terminar.")
            while True:
                id_produto = input("  id_produto: ").strip()
                if not id_produto:
                    break
                quantidade = int(input("  quantidade: ").strip())
                itens.append((int(id_produto), quantidade))
            if not itens:
                print("Nenhum item informado, pedido cancelado.\n")
            else:
                id_pedido = cadastro.cadastrar_pedido(conexao, id_cliente, itens)
                print(f"Pedido cadastrado com id {id_pedido}.\n")

        elif opcao == "9":
            caminho = relatorios.exportar_faturamento_csv(conexao)
            print(f"CSV exportado em: {caminho}\n")

        elif opcao == "10":
            caminho = relatorios.gerar_grafico_faturamento(conexao)
            print(f"Grafico gerado em: {caminho}\n")

        else:
            print("Opcao invalida.\n")

    except (ValueError, sqlite3.Error, RuntimeError) as erro:
        print(f"Ocorreu um erro ao processar sua solicitacao: {erro}\n")


def main() -> None:
    database.inicializar_banco()

    try:
        conexao = database.conectar()
    except sqlite3.Error as erro:
        print(f"Nao foi possivel conectar ao banco de dados: {erro}")
        sys.exit(1)

    try:
        while True:
            menu()
            opcao = input("Escolha uma opcao: ").strip()
            if opcao == "0":
                print("Encerrando. Ate mais!")
                break
            executar_opcao(conexao, opcao)
    finally:
        conexao.close()


if __name__ == "__main__":
    main()