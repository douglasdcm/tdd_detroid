from pytest import fixture
from tests.config import conn
from src.utils.utils import inicializa_tabelas
from src.controllers import courses, students
from src.controllers.materia import DisciplineController
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
    courses.create(nome="any_1")
    courses.create(nome="any_2")
    courses.create(nome="any_3")
    for i in range(3):
        for j in range(3):
            DisciplineController(conn).create(nome=f"any{j}", curso_id=i + 1)
    students.create(nome="anyone")
    students.subscribe_in_course(student_id=1, curso_id=1)
    with raises(Exception):
        students.subscribe_in_discipline(student_id=1, materia_id=1)
    with raises(Exception):
        students.subscribe_in_discipline(student_id=1, materia_id=2)
    students.subscribe_in_discipline(student_id=1, materia_id=3)


@fixture(scope="function", autouse=True)
def setup_bando_dados():
    inicializa_tabelas(conn)
