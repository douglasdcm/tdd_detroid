from os import remove
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
from tests.massa_dados import (
    aluno_nome_1,
    curso_nome_1,
    materia_nome_1,
    materia_nome_2,
    materia_nome_3,
)
from src.controller.controller import Controller

IN_MEMORY = ":memory:"


@fixture
def cria_banco():
    bd = BancoDados(connect(IN_MEMORY))
    yield bd
    bd.fecha_conexao_existente()


@fixture
def setup_database_in_memory_2(cria_banco):
    table = {
        "name": "student",
        "columns": [
            {"name": "name", "type": "text", "constraints": "not null"},
            {"name": "score", "type": "integer", "constraints": "not null"},
            {"name": "situation", "type": "text", "constraints": "not null"},
        ],
    }
    student = [
        {"name": "student_name", "score": 10, "situation": "in progress"},
        {"name": "student_name_2", "score": 9.6, "situation": "approved"},
        {"name": "student_name_3", "score": 4.7, "situation": "reproved"},
    ]
    database = cria_banco
    database.create_table(table)
    database.save(table["name"], student)
    yield database


@fixture
def setup_database_in_memory(cria_banco):
    table = {
        "name": "alunos",
        "columns": [
            {"name": "nome", "type": "text", "constraints": "not null"},
            {"name": "cr", "type": "integer", "constraints": "not null"},
            {"name": "situacao", "type": "text", "constraints": "not null"},
        ],
    }
    student = [
        {"nome": "student_nome", "cr": 10, "situacao": "in progress"},
        {"nome": "student_nome_2", "cr": 9.6, "situacao": "approved"},
        {"nome": "student_name_3", "cr": 4.7, "situacao": "reproved"},
    ]
    database = cria_banco
    database.create_table(table)
    database.save(table["name"], student)
    yield database


@fixture
def setup_database_in_real_db(cria_banco_real):
    table = {
        "name": "student",
        "columns": [
            {"name": "name", "type": "text", "constraints": "not null"},
            {"name": "score", "type": "integer", "constraints": "not null"},
            {"name": "situation", "type": "text", "constraints": "not null"},
        ],
    }
    student = [
        {"name": "student_name", "score": 10, "situation": "in progress"},
        {"name": "student_name_2", "score": 9.6, "situation": "approved"},
        {"name": "student_name_3", "score": 4.7, "situation": "reproved"},
    ]
    database = cria_banco_real
    database.create_table(table)
    database.save(table["name"], student)
    yield database


@fixture
def cria_banco_real():
    remove(banco_dados)
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
    Controller(AssociaCursoMateria(curso_obj, materia_1_obj), cria_banco).salva()
    Controller(AssociaCursoMateria(curso_obj, materia_2_obj), cria_banco).salva()
    Controller(AssociaCursoMateria(curso_obj, materia_3_obj), cria_banco).salva()
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
def enroll_student_in_course(cria_banco_real):
    bd = cria_banco_real
    bd.deleta_tabela(cursos)
    bd.deleta_tabela(alunos)
    bd.deleta_tabela(materias)

    student_controller = Controller(Aluno(aluno_nome_1), bd)
    student_controller.salva()
    student_obj = student_controller.get_by_biggest_id()

    course_controller = Controller(Curso(curso_nome_1), bd)
    course_controller.salva()
    course_obj = course_controller.get_by_biggest_id()

    lista_materias = [materia_nome_1, materia_nome_2, materia_nome_3]
    for materia in lista_materias:
        materia_controller = Controller(Materia(materia), bd)
        materia_controller.salva()
        materia_obj = materia_controller.get_by_biggest_id()
        Controller(AssociaCursoMateria(course_obj, materia_obj), bd).salva()

    enrollment = InscricaoAlunoCurso(student_obj, course_obj)
    Controller(enrollment, bd).salva()

    student_obj = Controller(student_obj, bd).pega_registro_por_id(
        student_obj.pega_id()
    )

    course_obj = Controller(course_obj, bd).pega_registro_por_id(course_obj.pega_id())

    yield student_obj, course_obj
    bd.deleta_tabela(cursos)
    bd.deleta_tabela(alunos)
    bd.deleta_tabela(materias)


@fixture
def cria_aluno_banco_real(cria_banco_real):
    bd = cria_banco_real
    bd.deleta_tabela(alunos)
    Controller(Aluno(aluno_nome_1), bd).salva()
    yield
    bd.deleta_tabela(alunos)


@fixture
def cria_curso_banco_real(cria_banco_real):
    # bd = cria_banco_real
    # bd.deleta_tabela(cursos)
    # bd.deleta_tabela(materias)
    # lista_materias = [materia_nome_1, materia_nome_2, materia_nome_3]
    # curso_controller = Controller(Curso(curso_nome_1), bd)
    # curso_controller.salva()
    # curso_obj = curso_controller.get_by_biggest_id()
    # for materia in lista_materias:
    #     discipline_controller = Controller(Materia(materia), bd)
    #     discipline_controller.salva()
    #     discipline_obj = discipline_controller.get_by_biggest_id()

    #     assoc_controller = Controller(
    #         AssociaCursoMateria(curso_obj, discipline_obj), bd
    #     )
    #     assoc_controller.salva()
    #     assoc_obj = assoc_controller.get_by_biggest_id()
    bd = cria_banco_real
    bd.deleta_tabela(cursos)
    bd.deleta_tabela(alunos)
    bd.deleta_tabela(materias)

    student_controller = Controller(Aluno(aluno_nome_1), bd)
    student_controller.salva()
    student_obj = student_controller.get_by_biggest_id()

    course_controller = Controller(Curso(curso_nome_1), bd)
    course_controller.salva()
    course_obj = course_controller.get_by_biggest_id()

    lista_materias = [materia_nome_1, materia_nome_2, materia_nome_3]
    for materia in lista_materias:
        materia_controller = Controller(Materia(materia), bd)
        materia_controller.salva()
        materia_obj = materia_controller.get_by_biggest_id()
        Controller(AssociaCursoMateria(course_obj, materia_obj), bd).salva()
    yield student_obj, course_obj
    bd.deleta_tabela(cursos)
    bd.deleta_tabela(alunos)
    bd.deleta_tabela(materias)


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
