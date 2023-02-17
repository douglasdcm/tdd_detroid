from pytest import fixture
from tests.config import conn
from src.utils.utils import inicializa_tabelas
from src.controllers.curso import CourseController
from src.controllers.materia import DisciplineController
from src.controllers.student import StudentController
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
    CourseController(conn).create(nome="any_1")
    CourseController(conn).create(nome="any_2")
    CourseController(conn).create(nome="any_3")
    for i in range(3):
        for j in range(3):
            DisciplineController(conn).cria(nome=f"any{j}", curso_id=i + 1)
    aluno = StudentController(conn)
    aluno.create(nome="anyone")
    aluno.subscribe_in_course(curso_id=1)
    with raises(Exception):
        aluno.subscribe_in_discipline(materia_id=1)
    with raises(Exception):
        aluno.subscribe_in_discipline(materia_id=2)
    aluno.subscribe_in_discipline(materia_id=3)


@fixture(scope="function", autouse=True)
def setup_bando_dados():
    inicializa_tabelas(conn)
