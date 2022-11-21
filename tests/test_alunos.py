from src.alunos import Alunos, Aluno, ErroAluno
from tests.config import NOME_BANCO
from pytest import fixture, raises
from src.sql_client import SqlClient


@fixture
def setup():
    conn = SqlClient(NOME_BANCO)
    yield Alunos(conn), conn


def test_nao_inscreve_aluno_se_curso_existente(setup):
    alunos, _ = setup
    alunos.cria("any")

    with raises(ErroAluno, match="Curso 42 nao existe"):
        alunos.inscreve_curso(1, 42)


def test_cria_aluno_por_api(setup):
    alunos, _ = setup
    alunos.cria("any")

    aluno = alunos.lista(1)

    assert aluno.id == 1


def test_alunos_lista_por_id(setup):
    alunos, conn = setup
    alunos.cria(nome="any")
    alunos.cria(nome="other")
    assert alunos.lista(id_=2).nome == "other"
    assert conn.lista(Aluno, id_=2).nome == "other"


def test_alunos_lista_tudo(setup):
    alunos, conn = setup
    alunos.cria(nome="any")
    alunos.cria(nome="other")
    assert len(alunos.lista_tudo()) == 2
    assert len(conn.lista_tudo(Aluno)) == 2


def test_alunos_cria_banco_dados(setup):
    alunos, conn = setup
    alunos.cria(nome="any")
    assert conn.lista(Aluno, id_=1).nome == "any"


def test_alunos_cria(setup):
    alunos, _ = setup
    alunos.cria(nome="any")
    assert alunos.lista(1).nome == "any"
