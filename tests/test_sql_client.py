from src.sql_client import SqlClient
from src.cursos import Curso
from tests.config import conn
from src.sql_client import SqlClient


def test_cria_novo_curso():
    curso = Curso(nome="any")
    conn.cria(curso)
    assert conn.lista_tudo(Curso)[0].nome == "any"
