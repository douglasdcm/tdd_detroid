from tests.config import conn
from src.cursos import Curso, Cursos
from src.materias import Materias
from tests.utils import cria_curso, cria_materia


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
    curso = Curso(nome="any")
    conn.cria(curso)

    assert conn.lista(Curso, 1).nome == "any"
    assert len(conn.lista_tudo(Curso)) == 1
