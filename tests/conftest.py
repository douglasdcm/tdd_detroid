import os
from sqlite3 import connect
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.banco_dados import BancoDados
from pytest import fixture
from src.model.materia import Materia
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.config import banco_dados
from src.tabelas import alunos, cursos, materias
from tests.massa_dados import aluno_nome_1, curso_nome_1, materia_nome_1, \
    materia_nome_2, materia_nome_3
from src.controller.controller import Controller

IN_MEMORY = ":memory:"


@fixture
def cria_banco():
    bd = BancoDados(connect(IN_MEMORY))
    yield bd
    bd.fecha_conexao_existente()


@fixture
def cria_banco_real():
    bd = BancoDados(connect(banco_dados))
    yield bd
    bd.fecha_conexao_existente()


@fixture
def cria_massa_dados_em_memoria(cria_banco):
    aluno = Aluno(aluno_nome_1)
    curso = Curso(curso_nome_1)
    materia_1 = Materia(materia_nome_1)
    materia_2 = Materia(materia_nome_2)
    materia_3 = Materia(materia_nome_3)
    aluno_obj = Controller(aluno, cria_banco).salva()
    curso_obj = Controller(curso, cria_banco).salva()
    materia_1_obj = Controller(materia_1, cria_banco).salva()
    materia_2_obj = Controller(materia_2, cria_banco).salva()
    materia_3_obj = Controller(materia_3, cria_banco).salva()
    Controller(AssociaCursoMateria(curso_obj, materia_1_obj),
               cria_banco).salva()
    Controller(AssociaCursoMateria(curso_obj, materia_2_obj),
               cria_banco).salva()
    Controller(AssociaCursoMateria(curso_obj, materia_3_obj),
               cria_banco).salva()
    Controller(InscricaoAlunoCurso(aluno_obj, curso_obj), cria_banco)
    yield
    cria_banco.deleta_tabela(cursos)
    cria_banco.deleta_tabela(alunos)


@fixture
def cria_massa_dados(cria_banco_real):
    bd = cria_banco_real
    bd.deleta_tabela(cursos)
    bd.deleta_tabela(alunos)
    aluno_id = Controller(Aluno(aluno_nome_1), bd).salva()
    curso_id = Controller(Curso(curso_nome_1), bd).salva()
    yield aluno_id, curso_id
    bd.deleta_tabela(cursos)
    bd.deleta_tabela(alunos)


@fixture
def cria_curso_materias_real(cria_banco_real):
    bd = cria_banco_real
    bd.deleta_tabela(cursos)
    bd.deleta_tabela(alunos)
    bd.deleta_tabela(materias)

    aluno = Aluno(aluno_nome_1)
    aluno = Controller(aluno, bd).salva()

    curso = Curso(curso_nome_1)
    curso = Controller(curso, bd).salva()

    Controller(InscricaoAlunoCurso(aluno, curso), bd).salva()

    lista_materias = [materia_nome_1, materia_nome_2, materia_nome_3]
    lista_materia_obj = []
    for materia in lista_materias:
        materia_obj = Materia(materia)
        materia_obj = Controller(materia_obj, bd).salva()
        lista_materia_obj.append(materia_obj)
        Controller(AssociaCursoMateria(curso, materia), bd).salva()
    yield aluno, curso, lista_materia_obj


@fixture
def cria_aluno_banco_real(cria_banco_real):
    bd = cria_banco_real
    bd.deleta_tabela(alunos)
    Controller(Aluno(aluno_nome_1), bd).salva()
    yield
    bd.deleta_tabela(alunos)


@fixture
def cria_curso_banco_real(cria_banco_real):
    bd = cria_banco_real
    bd.deleta_tabela(cursos)
    Controller(Curso(curso_nome_1), bd).salva()
    yield
    bd.deleta_tabela(cursos)


@fixture
def cria_curso_em_memoria():
    bd = cria_banco
    Controller(Curso(curso_nome_1), bd).salva()


@fixture
def cria_aluno_em_memoria():
    bd = cria_banco
    Controller(Aluno(aluno_nome_1), bd).salva()


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
def cria_curso_cancelado(cria_curso_com_materias):
    curso = cria_curso_com_materias
    curso.define_situacao("cancelado")
    yield curso


@fixture
def inscreve_aluno(cria_aluno, cria_curso_com_materias):
    cria_aluno.inscreve_curso(cria_curso_com_materias)
    yield cria_aluno, cria_curso_com_materias
