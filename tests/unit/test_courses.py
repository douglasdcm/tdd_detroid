from tests.config import conn
from src.schemes.course import CourseDB
from src.utils.exceptions import ErrorCourse
from pytest import raises, mark
from src.controllers.curso import CourseController


def test_curso_pega_id():
    curso = CourseController(conn)
    curso.create(nome="any")
    assert curso.id == len(conn.lista_tudo(CourseDB))


def test_curso_cria():
    curso = CourseController(conn)
    curso.create(nome="any")
    assert conn.lista(CourseDB, 1).nome == "any"


@mark.parametrize("input", [(""), ("  ")])
def test_nome_curso_nao_vazio(input):
    curso = CourseController(conn)
    with raises(ErrorCourse, match="Nome do curso invalido"):
        curso.create(input)


def test_nao_cria_curso_com_mesmo_nome():
    curso = CourseController(conn)
    curso.create("any")
    with raises(ErrorCourse, match="Existe outro curso com o nome any"):
        curso.create("any")
