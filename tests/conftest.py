from pytest import fixture
from tests.config import conn
from src.utils.utils import inicializa_tabelas
from src.modelos.curso import CursoModelo
from src.modelos.materia import MateriaModelo
from src.modelos.aluno import AlunoModelo


@fixture
def popula_banco_dados(scope="function"):
    CursoModelo(conn).cria(nome="any_1")
    CursoModelo(conn).cria(nome="any_2")
    CursoModelo(conn).cria(nome="any_3")
    for i in range(3):
        MateriaModelo(conn).cria(nome=f"any{i}", curso_id=i + 1)
    AlunoModelo(conn).cria(nome="any")


@fixture(scope="function", autouse=True)
def setup_bando_dados():
    inicializa_tabelas(conn)
