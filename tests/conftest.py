from pytest import fixture
from tests.config import conn
from src.utils.utils import inicializa_tabelas
from src.models.curso import CursoModelo
from src.models.materia import MateriaModelo
from src.models.aluno import AlunoModelo
from pytest import raises


@fixture
def popula_banco_dados(scope="function"):
    """Combinacao de materia x curso
    m = materia, c = curso
    m1 c1
    m2 c1
    m3 c1

    m1 c2
    m2 c2
    m3 c2

    m7 c3
    m8 c3
    m9 c3
    """
    CursoModelo(conn).cria(nome="any_1")
    CursoModelo(conn).cria(nome="any_2")
    CursoModelo(conn).cria(nome="any_3")
    for i in range(3):
        for j in range(3):
            MateriaModelo(conn).cria(nome=f"any{j}", curso_id=i + 1)
    aluno = AlunoModelo(conn)
    aluno.cria(nome="anyone")
    aluno.inscreve_curso(curso_id=1)
    aluno.inscreve_materia(materia_id=1)
    aluno.inscreve_materia(materia_id=2)
    aluno.inscreve_materia(materia_id=3)


@fixture(scope="function", autouse=True)
def setup_bando_dados():
    inicializa_tabelas(conn)
