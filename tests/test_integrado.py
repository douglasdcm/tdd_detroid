from src.cursos import Cursos, ErroCurso, Curso
from src.materias import Materias, ErroMateria, Materia
from tests.config import NOME_BANCO
from pytest import fixture, raises
from src.sql_client import SqlClient, ErroBancoDados
from src.utils import limpa_tabelas


@fixture
def setup():
    yield SqlClient(NOME_BANCO)


def test_curso_nao_pode_ter_materias_com_mesmo_nome():
    conn = SqlClient(NOME_BANCO)

    Cursos(conn).cria("any_1")
    Cursos(conn).cria("any_2")
    Cursos(conn).cria("any_3")
    Materias(conn).cria("any", 1)
    with raises(
        ErroMateria,
        match="O curso já possui uma matéria com este nome",
    ):
        Materias(conn).cria("any", 1)


def test_nao_criar_quarto_curso_se_menos_de_tres_materias_por_curso(setup):
    conn = setup
    Cursos(conn).cria("any_1")
    Cursos(conn).cria("any_2")
    Cursos(conn).cria("any_3")
    Materias(conn).cria(nome="any", curso_id=1)
    with raises(
        ErroCurso,
        match="Necessários 3 cursos com 3 três matérias para se criar novos cursos",
    ):
        Cursos(conn).cria("quarto")


def test_nao_criar_quarto_curso_se_todos_cursos_sem_materias(setup):
    conn = setup
    Cursos(conn).cria("any_1")
    Cursos(conn).cria("any_2")
    Cursos(conn).cria("any_3")
    with raises(
        ErroCurso,
        match="Necessários 3 cursos com 3 três matérias para se criar novos cursos",
    ):
        Cursos(conn).cria("quatro")


def test_materia_nao_criada_se_menos_de_tres_cursos_existentes(setup):
    conn = setup
    with raises(
        ErroMateria, match="Necessários 3 cursos para se criar a primeira matéria"
    ):
        Materias(conn).cria("any", 1)


def test_materia_nao_associada_curso_inexistente(setup, popula_banco_dados):
    conn = setup
    with raises(ErroMateria):
        Materias(conn).cria("any", 42)


def test_materia_associada_curso_existente(setup):
    setup.cria(Curso(nome="any"))
    setup.cria(Materia(nome="any", curso=1))
    assert setup.lista(Materia, 1).nome == "any"


def test_cria_tabela_com_dados(setup):
    conn = setup
    conn.cria(Curso(nome="any_1"))
    conn.cria(Curso(nome="any_2"))
    conn.cria(Curso(nome="any_3"))
    assert len(conn.lista_tudo(Curso)) == 3


def test_cria_item_bd(setup):
    setup.cria(Curso(nome="any"))
    assert len(setup.lista_tudo(Curso)) == 1


def test_lista_por_id_bd(setup):
    conn = SqlClient(NOME_BANCO)
    Cursos(conn).cria("any")
    limpa_tabelas(conn)
    assert len(setup.lista_tudo(Curso)) == 0
