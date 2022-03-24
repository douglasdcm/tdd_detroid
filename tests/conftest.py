from multiprocessing import connection
from sqlite3 import connect as connect
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.banco_dados import BancoDados
from pytest import fixture
from src.model.materia import Materia
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.config import database_name, memory_database
from tests.massa_dados import (
    aluno_nome_1,
    curso_nome_1,
    materia_nome_1,
    materia_nome_2,
    materia_nome_3,
)
from src.controller.controller import Controller
from tests.helper import (
    populate_database,
    build_database_with_empty_tables,
    clean_database,
    build_database_with_empty_tables_v2,
)


@fixture
def setup_empty_database_in_memory():
    connection = connect(memory_database)
    yield build_database_with_empty_tables(connection)
    clean_database(connection)


@fixture
def setup_empty_database_real():
    connection = connect(database_name)
    clean_database(connection)
    yield build_database_with_empty_tables(connection)


@fixture
def setup_empty_database_real_v2():
    """Return a connection"""
    connection = connect(database_name)
    clean_database(connection)
    yield build_database_with_empty_tables_v2(connection)


@fixture
def setup_database_in_memory():
    connection = connect(memory_database)
    clean_database(connection)
    yield populate_database(connection)


@fixture
def setup_database_in_real_db():
    connection = connect(database_name)
    clean_database(connection)
    yield populate_database(connection)


@fixture
def cria_massa_dados_em_memoria(setup_database_in_memory):
    aluno = Aluno(aluno_nome_1)
    curso = Curso(curso_nome_1)
    materia_1 = Materia(materia_nome_1)
    materia_2 = Materia(materia_nome_2)
    materia_3 = Materia(materia_nome_3)
    aluno_obj = Controller(aluno, setup_database_in_memory).salva()
    curso_obj = Controller(curso, setup_database_in_memory).salva()
    materia_1_obj = Controller(materia_1, setup_database_in_memory).salva()
    materia_2_obj = Controller(materia_2, setup_database_in_memory).salva()
    materia_3_obj = Controller(materia_3, setup_database_in_memory).salva()
    Controller(
        AssociaCursoMateria(curso_obj, materia_1_obj), setup_database_in_memory
    ).salva()
    Controller(
        AssociaCursoMateria(curso_obj, materia_2_obj), setup_database_in_memory
    ).salva()
    Controller(
        AssociaCursoMateria(curso_obj, materia_3_obj), setup_database_in_memory
    ).salva()
    Controller(InscricaoAlunoCurso(aluno_obj, curso_obj), setup_database_in_memory)


@fixture
def cria_massa_dados():
    connection = connect(database_name)
    populate_database(connection)
    yield 1, 1
    clean_database(connection)


@fixture
def enroll_student_in_course():
    connection = connect(database_name)
    clean_database(connection)
    populate_database(connection)

    student_obj = Controller(Aluno(), connection).pega_registro_por_id(1)

    course_obj = Controller(Curso(), connection).pega_registro_por_id(1)

    yield student_obj, course_obj, connection


@fixture
def cria_aluno_banco_real(setup_database_in_real_db):
    bd = setup_database_in_real_db
    Controller(Aluno(aluno_nome_1), bd).salva()
    yield


@fixture
def cria_curso_banco_real(setup_database_in_real_db):
    bd = setup_database_in_real_db

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


@fixture
def cria_curso_em_memoria(setup_database_in_memory):
    bd = setup_database_in_memory
    Controller(Curso(curso_nome_1), bd).salva()


@fixture
def cria_aluno_em_memoria(setup_database_in_memory):
    bd = setup_database_in_memory
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
