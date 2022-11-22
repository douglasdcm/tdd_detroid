from src.alunos import Alunos, Aluno, ErroAluno
from tests.config import conn
from pytest import fixture, raises
from src.cursos import Cursos
from time import sleep


@fixture
def setup():
    yield Alunos(conn)


def test_aluno_pode_se_inscrever_em_apenas_um_curso(setup, popula_banco_dados):
    alunos = setup
    alunos.cria("any")
    Cursos(conn).cria("other")
    alunos.inscreve_curso(1, 4)

    for _ in range(3):
        if alunos.lista(1).curso_id is not None:
            break
        sleep(1)

    with raises(ErroAluno, match="Aluno esta inscrito em outro curso"):
        alunos.inscreve_curso(1, 3)

    aluno = alunos.lista(1)
    assert aluno.curso_id == 4


def test_nao_inscreve_em_curso_aluno_nao_existente(setup, popula_banco_dados):
    alunos = setup
    Cursos(conn).cria("other")

    with raises(ErroAluno, match="Aluno 42 nao existe"):
        alunos.inscreve_curso(42, 1)


def test_nao_inscreve_aluno_se_curso_existente(setup):
    alunos = setup
    alunos.cria("any")

    with raises(ErroAluno, match="Curso 42 nao existe"):
        alunos.inscreve_curso(1, 42)


def test_cria_aluno_por_api(setup):
    alunos = setup
    alunos.cria("any")

    aluno = alunos.lista(1)

    assert aluno.id == 1


def test_alunos_lista_por_id(setup):
    alunos = setup
    alunos.cria(nome="any")
    alunos.cria(nome="other")
    assert alunos.lista(id_=2).nome == "other"
    assert conn.lista(Aluno, id_=2).nome == "other"


def test_alunos_lista_tudo(setup):
    alunos = setup
    alunos.cria(nome="any")
    alunos.cria(nome="other")
    assert len(alunos.lista_tudo()) == 2
    assert len(conn.lista_tudo(Aluno)) == 2


def test_alunos_cria_banco_dados(setup):
    alunos = setup
    alunos.cria(nome="any")
    assert conn.lista(Aluno, id_=1).nome == "any"


def test_alunos_cria(setup):
    alunos = setup
    alunos.cria(nome="any")
    assert alunos.lista(1).nome == "any"
