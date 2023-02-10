from tests.config import conn
from src.schemes.course import CursoBd
from src.utils.exceptions import CourseException
from pytest import raises, mark
from src.controllers.curso import CursoModelo


def test_curso_pega_id():
    curso = CursoModelo(conn)
    curso.cria(nome="any")
    assert curso.id == len(conn.lista_tudo(CursoBd))


def test_curso_cria():
    curso = CursoModelo(conn)
    curso.cria(nome="any")
    assert conn.lista(CursoBd, 1).nome == "any"


@mark.parametrize("input", [(""), ("  ")])
def test_nome_curso_nao_vazio(input):
    curso = CursoModelo(conn)
    with raises(ErroCurso, match="Nome do curso invalido"):
        curso.cria(input)


def test_nao_cria_curso_com_mesmo_nome():
    curso = CursoModelo(conn)
    curso.cria("any")
    with raises(CourseException, match="Existe outro curso com o nome any"):
        curso.cria("any")
