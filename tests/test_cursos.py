from tests.config import NOME_BANCO
from src.cursos import Curso
from src.sql_client import SqlClient


def test_cursos_cria():
    curso = Curso(nome="any")
    sql = SqlClient(NOME_BANCO)
    sql.cria(curso)

    assert sql.lista(Curso, 1).nome == "any"
    assert len(sql.lista_tudo(Curso)) == 1
