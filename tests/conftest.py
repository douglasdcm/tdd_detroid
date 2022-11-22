from pytest import fixture
from tests.config import conn
from src.utils import inicializa_tabelas
from src.cursos import Cursos
from src.materias import Materias
from src.alunos import Alunos


@fixture
def popula_banco_dados(scope="function"):
    Cursos(conn).cria(nome="any_1")
    Cursos(conn).cria(nome="any_2")
    Cursos(conn).cria(nome="any_3")
    for i in range(3):
        Materias(conn).cria(nome=f"any{i}", curso_id=i + 1)
    Alunos(conn).cria(nome="any")


@fixture(scope="function", autouse=True)
def setup_bando_dados():
    inicializa_tabelas(conn)
