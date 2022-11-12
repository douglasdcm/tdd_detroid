from src.alunos import Alunos
from src.banco_dados import BancoDados as bd
from tests.config import NOME_BANCO
from pytest import fixture


@fixture
def setup():
    conn = bd(NOME_BANCO)
    yield Alunos(conn), conn


def test_alunos_lista_por_id(setup):
    alunos, conn = setup
    alunos.cria(nome="any")
    alunos.cria(nome="other")
    assert alunos.lista(id_=2).nome == "other"
    assert conn.lista(Alunos, id_=2) == [(2, "other")]


def test_alunos_lista_tudo(setup):
    alunos, conn = setup
    alunos.cria(nome="any")
    alunos.cria(nome="other")
    assert len(alunos.lista_tudo()) == 2
    assert len(conn.lista_tudo(Alunos)) == 2


def test_alunos_cria_banco_dados(setup):
    alunos, conn = setup
    alunos.cria(nome="any")
    assert len(conn.lista(Alunos, id_=1)) == 1


def test_alunos_cria(setup):
    alunos, _ = setup
    assert alunos.cria(nome="any") == True
