from src.banco_dados import BancoDados as bd
from src.manager import ErroCurso
from src.cursos import Cursos
from src.materias import Materias
from tests.config import NOME_BANCO
from src.banco_dados import Tabela
from pytest import fixture, raises
from src.banco_dados import ErroBancoDados
from src.manager import Tipos


@fixture
def setup():
    class Any:
        pass

    conn = bd(NOME_BANCO)

    try:
        conn.deleta_tabela(Any.__name__)
    except:
        pass
    yield conn, Any.__name__


def test_nao_criar_quarto_curso_se_menos_de_tres_materias_por_curso():
    Cursos(bd(NOME_BANCO)).cria("any")
    Cursos(bd(NOME_BANCO)).cria("any")
    Cursos(bd(NOME_BANCO)).cria("any")
    item_materia = {"nome": "any", "curso": 1}
    bd(NOME_BANCO).cria(Tipos.MATERIAS.value, item_materia)
    with raises(
        ErroCurso,
        match="Necessários 3 cursos com 3 três matérias para se criar novos cursos",
    ):
        Cursos(bd(NOME_BANCO)).cria("quarto")


def test_nao_criar_quarto_curso_se_todos_cursos_sem_materias():
    Cursos(bd(NOME_BANCO)).cria("any")
    Cursos(bd(NOME_BANCO)).cria("any")
    Cursos(bd(NOME_BANCO)).cria("any")
    with raises(
        ErroCurso,
        match="Necessários 3 cursos com 3 três matérias para se criar novos cursos",
    ):
        Cursos(bd(NOME_BANCO)).cria("quarto")


def test_materia_nao_criada_se_menos_de_tres_cursos_existentes():
    with raises(
        ErroCurso, match="Necessários 3 cursos para se criar a primeira matéria"
    ):
        Materias(bd(NOME_BANCO)).cria("any", 1)


def test_materia_nao_associada_curso_inexistente():
    item_materia = {"nome": "any", "curso": 1}
    with raises(ErroBancoDados):
        bd(NOME_BANCO).cria(Tipos.MATERIAS.value, item_materia)


def test_materia_associada_curso_existente():
    item_curso = {"nome": "any"}
    item_materia = {"nome": "any", "curso": 1}
    assert bd(NOME_BANCO).cria(Tipos.CURSOS.value, item_curso) == True
    assert bd(NOME_BANCO).cria(Tipos.MATERIAS.value, item_materia) == True


def test_cria_tabela_com_dados(setup):
    conn, any_ = setup
    conn = bd(NOME_BANCO)
    tabela = Tabela(any_)
    tabela.colunas = ["any", "other"]
    item = {"any": "any1", "other": "other1"}
    conn.cria_tabela(tabela)
    conn.cria(any_, item)
    conn.cria(any_, item)
    conn.cria(any_, item)
    assert len(conn.lista_tudo(any_)) == 3


def test_cria_tabela_vazia(setup):
    conn, any_ = setup
    conn = bd(NOME_BANCO)
    tabela = Tabela(any_)
    tabela.colunas = ["any", "other"]
    conn.cria_tabela(tabela)
    assert len(conn.lista_tudo(any_)) == 0


def test_lista_tudo_bd():
    item = {"nome": "any"}
    bd(NOME_BANCO).cria(Tipos.CURSOS.value, item)
    assert len(bd(NOME_BANCO).lista_tudo(Tipos.CURSOS.value)) == 1


def test_cria_item_bd():
    item = {"nome": "any"}
    assert bd(NOME_BANCO).cria(Tipos.CURSOS.value, item) == True


def test_lista_por_id_bd():
    assert len(bd(NOME_BANCO).lista(Tipos.CURSOS.value, 1)) == 0
