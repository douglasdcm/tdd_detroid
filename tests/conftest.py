from sqlite3 import connect
from src.model.banco_dados import BancoDados
from pytest import fixture
from src.model.materia import Materia
from src.model.aluno import Aluno
from src.model.curso import Curso

@fixture(scope="function")
def cria_banco():
    return BancoDados(connect(":memory:"))

@fixture(scope="function")
def limpa_banco(cria_banco):
    cria_banco.fecha_conexao_existente()

@fixture
def cria_aluno():
    nome = "José_U"
    return Aluno(nome)

@fixture
def cria_curso_com_materias():
    curso = Curso("pedagogia")
    curso.atualiza_materias(Materia("mat"))
    curso.atualiza_materias(Materia("hist"))
    curso.atualiza_materias(Materia("geo"))
    return curso

@fixture
def inscreve_aluno(cria_aluno, cria_curso_com_materias):
    cria_aluno.inscreve_curso(cria_curso_com_materias)
    return cria_aluno, cria_curso_com_materias