from src.cursos import CursoBd
from tests.config import conn
from src.sql_client import SqlClient


def test_cria_novo_curso():
    curso = CursoBd(nome="any")
    conn.cria(curso)
    assert conn.lista_tudo(CursoBd)[0].nome == "any"
