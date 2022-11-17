from pytest import fixture
from tests.config import NOME_BANCO
from src.utils import limpa_tabelas
from src.sql_client import SqlClient
from src.cursos import Cursos
from src.materias import Materias
from src.alunos import Alunos


@fixture
def popula_banco_dados(scope="function"):
    conn = SqlClient(NOME_BANCO)
    limpa_tabelas(conn)
    Cursos(conn).cria(nome="any_1")
    Cursos(conn).cria(nome="any_2")
    Cursos(conn).cria(nome="any_3")
    for i in range(3):
        Materias(conn).cria(nome=f"any{i}", curso_id=i)
    Alunos(conn).cria(nome="any")


@fixture(scope="function", autouse=True)
def setup_bando_dados():
    conn = SqlClient(NOME_BANCO)
    limpa_tabelas(conn)
