from sqlite3 import connect

from attr.setters import NO_OP
from src.model.banco_dados import BancoDados
from pytest import fixture
from src.model.materia import Materia
from src.model.aluno import Aluno
from src.model.curso import Curso

@fixture
def cria_banco():
    bd = BancoDados(connect(":memory:"))
    yield bd
    bd.fecha_conexao_existente()

@fixture
def cria_aluno():
    nome = "José"
    aluno = Aluno(nome)
    yield aluno
    aluno = None

@fixture
def cria_curso_com_materias():
    curso = Curso("pedagogia")
    curso.atualiza_materias(Materia("mat"))
    curso.atualiza_materias(Materia("hist"))
    curso.atualiza_materias(Materia("geo"))
    yield curso
    curso = None

@fixture
def inscreve_aluno(cria_aluno, cria_curso_com_materias):
    cria_aluno.inscreve_curso(cria_curso_com_materias)
    yield cria_aluno, cria_curso_com_materias
    