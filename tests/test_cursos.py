from tests.config import conn
from src.curso_bd import CursoBd
from src.curso_modelo import ErroCurso
from src.cursos import Cursos
from src.materias import Materias
from tests.utils import cria_curso, cria_materia
from pytest import raises, mark


@mark.parametrize("input", [(""), ("  ")])
def test_nome_curso_nao_vazio(input):
    cursos = Cursos(conn)
    with raises(ErroCurso, match="Nome do curso invalido"):
        cursos.cria(input)


def test_cria_curso_se_nao_existe():
    cursos = Cursos(conn)
    cursos.cria("any")
    with raises(ErroCurso, match="Existe outro curso com o nome any"):
        cursos.cria("any")


def test_cli_tres_cursos_com_tres_materias_cada():
    cursos = Cursos(conn)
    materias = Materias(conn)
    cria_curso(conn)
    cria_curso(conn)
    cria_curso(conn)
    for _ in range(3):
        cria_materia(conn, 1)
        cria_materia(conn, 2)
        cria_materia(conn, 3)

    # verifica pela API
    assert len(cursos.lista_tudo()) == 3
    assert len(materias.lista_tudo()) == 9


def test_cursos_cria():
    curso = CursoBd(nome="any")
    conn.cria(curso)

    assert conn.lista(CursoBd, 1).nome == "any"
    assert len(conn.lista_tudo(CursoBd)) == 1
