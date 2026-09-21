"""
conftest.py
Fixtures compartilhadas para todos os testes.
Cria um banco in-memory com schema e dados de exemplo.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import sqlite3
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
SEED_PATH = BASE_DIR / "sql" / "seed.sql"


@pytest.fixture
def conexao():
    """Conexao in-memory com schema + seed carregados."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    seed = SEED_PATH.read_text(encoding="utf-8")
    conn.executescript(schema)
    conn.executescript(seed)
    yield conn
    conn.close()


@pytest.fixture
def conexao_vazia():
    """Conexao in-memory apenas com schema (sem dados)."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema)
    yield conn
    conn.close()
