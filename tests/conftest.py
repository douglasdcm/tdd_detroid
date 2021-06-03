from sqlite3 import connect

from attr.setters import NO_OP
from src.model.banco_dados import BancoDados
from pytest import fixture
from src.model.materia import Materia
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.config import banco_dados
from src.tabelas import alunos, cursos
from tests.massa_dados import aluno_nome_1, curso_nome_1, materia_nome_1, materia_nome_2, materia_nome_3
from src.controller.controller import Controller

IN_MEMORY = ":memory:"

@fixture
def cria_banco():
    bd = BancoDados(connect(IN_MEMORY))
    yield bd
    bd.fecha_conexao_existente()

@fixture
def cria_massa_dados_em_memoria():
    bd = BancoDados(connect(IN_MEMORY))
    Controller(Aluno(aluno_nome_1), bd).salva()
    Controller(Curso(curso_nome_1), bd).salva()
    yield
    bd.fecha_conexao_existente()

@fixture
def cria_massa_dados():
    bd = BancoDados(connect(banco_dados))
    bd.deleta_tabela(cursos)
    bd.deleta_tabela(alunos)
    Controller(Aluno(aluno_nome_1), bd).salva()
    Controller(Curso(curso_nome_1), bd).salva()
    yield
    bd.fecha_conexao_existente()  

@fixture
def cria_aluno():
    aluno = Aluno(aluno_nome_1)
    yield aluno
    aluno = None

@fixture
def cria_curso_com_materias():
    curso = Curso(curso_nome_1)
    curso.atualiza_materias(Materia(materia_nome_1))
    curso.atualiza_materias(Materia(materia_nome_2))
    curso.atualiza_materias(Materia(materia_nome_3))
    yield curso
    curso = None

@fixture
def inscreve_aluno(cria_aluno, cria_curso_com_materias):
    cria_aluno.inscreve_curso(cria_curso_com_materias)
    yield cria_aluno, cria_curso_com_materias
    