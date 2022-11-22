from src.cursos import Cursos, ErroCurso, Curso
from src.materias import Materias, ErroMateria, Materia
from tests.config import conn
from pytest import raises
from src.utils import inicializa_tabelas


def test_curso_nao_pode_ter_materias_com_mesmo_nome():

    Cursos(conn).cria("any_1")
    Cursos(conn).cria("any_2")
    Cursos(conn).cria("any_3")
    Materias(conn).cria("any", 1)
    with raises(
        ErroMateria,
        match="O curso já possui uma matéria com este nome",
    ):
        Materias(conn).cria("any", 1)


def test_nao_criar_quarto_curso_se_menos_de_tres_materias_por_curso():
    Cursos(conn).cria("any_1")
    Cursos(conn).cria("any_2")
    Cursos(conn).cria("any_3")
    Materias(conn).cria(nome="any", curso_id=1)
    with raises(
        ErroCurso,
        match="Necessários 3 cursos com 3 três matérias para se criar novos cursos",
    ):
        Cursos(conn).cria("quarto")


def test_nao_criar_quarto_curso_se_todos_cursos_sem_materias():
    Cursos(conn).cria("any_1")
    Cursos(conn).cria("any_2")
    Cursos(conn).cria("any_3")
    with raises(
        ErroCurso,
        match="Necessários 3 cursos com 3 três matérias para se criar novos cursos",
    ):
        Cursos(conn).cria("quatro")


def test_materia_nao_criada_se_menos_de_tres_cursos_existentes():
    with raises(
        ErroMateria, match="Necessários 3 cursos para se criar a primeira matéria"
    ):
        Materias(conn).cria("any", 1)


def test_materia_nao_associada_curso_inexistente(popula_banco_dados):
    with raises(ErroMateria):
        Materias(conn).cria("any", 42)


def test_materia_associada_curso_existente():
    conn.cria(Curso(nome="any"))
    conn.cria(Materia(nome="any", curso=1))
    assert conn.lista(Materia, 1).nome == "any"


def test_cria_tabela_com_dados():
    conn.cria(Curso(nome="any_1"))
    conn.cria(Curso(nome="any_2"))
    conn.cria(Curso(nome="any_3"))
    assert len(conn.lista_tudo(Curso)) == 3


def test_cria_item_bd():
    conn.cria(Curso(nome="any"))
    assert len(conn.lista_tudo(Curso)) == 1


def test_lista_por_id_bd():
    Cursos(conn).cria("any")
    inicializa_tabelas(conn)
    assert len(conn.lista_tudo(Curso)) == 0
