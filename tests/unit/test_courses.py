from tests.config import conn
from src.schemes.course import CourseDB
from src.utils.exceptions import ErrorCourse
from pytest import raises, mark
from src.controllers import courses


def test_curso_pega_id():
    courses.create(nome="any")
    assert courses.id == len(conn.lista_tudo(CourseDB))


def test_curso_cria():
    courses.create(nome="any")
    assert conn.get(CourseDB, 1).nome == "any"


@mark.parametrize("input", [(""), ("  ")])
def test_nome_curso_nao_vazio(input):
    with raises(ErrorCourse, match="Nome do curso invalido"):
        courses.create(input)


def test_nao_cria_curso_com_mesmo_nome():
    courses.create("any")
    with raises(ErrorCourse, match="Existe outro curso com o nome any"):
        courses.create("any")
