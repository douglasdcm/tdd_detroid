from src.esquemas.aluno import AlunoBd
from src.modelos.aluno import AlunoModelo
from src.modelos.aluno import ErroAluno
from src.utils.exceptions import ErroAluno, ErroMateriaAluno
from tests.config import conn
from pytest import raises


def test_aluno_nao_pode_se_inscrever_duas_vezes_na_mesma_materia(popula_banco_dados):
    aluno = AlunoModelo(conn, 1)
    with raises(ErroMateriaAluno):
        aluno.inscreve_materia(1)
        aluno.inscreve_materia(2)
        aluno.inscreve_materia(3)
    with raises(ErroMateriaAluno, match="Aluno 1 ja esta inscrito na materia 1"):
        aluno.inscreve_materia(1)


def test_inscreve_aluno_numa_materia(popula_banco_dados):
    aluno = AlunoModelo(conn, 1)
    with raises(
        ErroMateriaAluno, match="Aluno deve se inscrever em 3 materias no minimo"
    ):
        aluno.inscreve_materia(1)


def test_aluno_cria():
    aluno = AlunoModelo(conn)
    aluno.cria(nome="any")
    assert conn.lista(AlunoBd, 1).nome == "any"
    assert conn.lista(AlunoBd, 1).id == 1


def test_inscreve_aluno_curso(popula_banco_dados):
    aluno = AlunoModelo(conn, 1)
    aluno.inscreve_curso(curso_id=1)
    assert conn.lista(AlunoBd, 1).curso_id == 1


def test_verifica_aluno_existe(popula_banco_dados):
    with raises(ErroAluno, match="Aluno 42 nao existe"):
        AlunoModelo(conn, 42)


def test_nao_inscreve_aluno_se_curso_existente():
    aluno = AlunoModelo(conn)
    aluno.cria("any")
    with raises(ErroAluno, match="Curso 42 nao existe"):
        aluno.inscreve_curso(42)


def test_alunos_lista_por_id():
    aluno = AlunoModelo(conn)
    aluno.cria(nome="any")
    aluno.cria(nome="other")
    assert conn.lista(AlunoBd, id_=2).nome == "other"


def test_alunos_lista_tudo():
    aluno = AlunoModelo(conn)
    aluno.cria(nome="any")
    aluno.cria(nome="other")
    assert len(conn.lista_tudo(AlunoBd)) == 2


def test_alunos_cria_banco_dados():
    aluno = AlunoModelo(conn)
    aluno.cria(nome="any")
    assert conn.lista(AlunoBd, id_=1).nome == "any"
