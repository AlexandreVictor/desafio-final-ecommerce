from tabulate import tabulate
"""
Imprime uma tabela formatada no terminal a partir de uma lista de linhas e colunas.
"""
def imprimir_tabela(linhas, colunas):
    if not linhas:
        print("Nenhum resultado encontrado.\n")
        return
    dados = [[linha[c] for c in colunas] for linha in linhas]
    print(tabulate(dados, headers=colunas, tablefmt="simple"))