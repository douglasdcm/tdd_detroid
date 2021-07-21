from sqlite3 import connect
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.banco_dados import BancoDados
from pytest import fixture
from src.model.materia import Materia
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.config import banco_dados
from src.tabelas import alunos, cursos, inscricao_aluno_curso, materias
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
    Controller(Aluno(aluno_nome_1), cria_banco).salva()
    Controller(Curso(curso_nome_1), cria_banco).salva()
    Controller(Materia(materia_nome_1), cria_banco).salva()
    Controller(Materia(materia_nome_2), cria_banco).salva()
    Controller(Materia(materia_nome_3), cria_banco).salva()
    Controller(AssociaCursoMateria(curso_id=1, materia_id=1),
               cria_banco).salva()
    Controller(AssociaCursoMateria(curso_id=2, materia_id=1),
               cria_banco).salva()
    Controller(AssociaCursoMateria(curso_id=3, materia_id=1),
               cria_banco).salva()
    Controller(InscricaoAlunoCurso(aluno_id=1, curso_id=1), cria_banco)
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
