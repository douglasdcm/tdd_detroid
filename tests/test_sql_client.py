from src.sql_client import SqlClient
from src.cursos import Curso
from tests.config import NOME_BANCO
from src.sql_client import SqlClient


def test_cria_novo_curso():
    conn = SqlClient(NOME_BANCO)
    curso = Curso(nome="any")
    conn.cria(curso)
    assert conn.lista_tudo(Curso)[0].nome == "any"
