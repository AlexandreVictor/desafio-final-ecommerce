"""
database.py
Responsavel pela conexao com o banco SQLite
inicial das tabelas a partir dos scripts em sql/.
"""


import sqlite3
from pathlib import Path

"""
Variaveis de caminho para o banco de dados e scripts SQL.
BASE_DIR: Caminho base do projeto.
DB_PATH: Caminho para o arquivo do banco de dados SQLite.
SCHEMA_PATH: Caminho para o script SQL de criacao das tabelas.
SEED_PATH: Caminho para o script SQL de populacao inicial do banco.
"""

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "loja.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
SEED_PATH = BASE_DIR / "sql" / "seed.sql"


def conectar() -> sqlite3.Connection:
    """Abre e retorna uma conexao com o banco de dados SQLite."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute("PRAGMA foreign_keys = ON;")
    conexao.row_factory = sqlite3.Row
    return conexao


def banco_existe() -> bool:
    """Verifica se o banco de dados ja existe e não esta vazio."""
    return DB_PATH.exists() and DB_PATH.stat().st_size > 0


def inicializar_banco(forcar: bool = False) -> None:
    """
    Cria as tabelas e popula com dados de exemplo.
    Se forcar=True, recria o banco do zero mesmo que ja exista.
    """
    if banco_existe() and not forcar:
        return

    try:
        with conectar() as conexao:
            schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
            seed_sql = SEED_PATH.read_text(encoding="utf-8")
            # Executa os scripts SQL para criar as tabelas e popular o banco
            conexao.executescript(schema_sql)
            conexao.executescript(seed_sql)
        print("Banco de dados inicializado com sucesso.")
    except (sqlite3.Error, OSError) as erro:
        print(f"Erro ao inicializar o banco de dados: {erro}")
        raise


if __name__ == "__main__":
    import sys

    forcar = "--forcar" in sys.argv
    inicializar_banco(forcar=forcar)
