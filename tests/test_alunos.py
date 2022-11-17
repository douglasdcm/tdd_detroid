from src.alunos import Alunos, Aluno
from tests.config import NOME_BANCO
from pytest import fixture
from src.sql_client import SqlClient


@fixture
def setup():
    conn = SqlClient(NOME_BANCO)
    yield Alunos(conn), conn


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
    assert alunos.cria(nome="any") == True
