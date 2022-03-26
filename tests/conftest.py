from sqlite3 import connect as connect
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
    clean_database(connection)
    yield build_database_with_empty_tables(connection)


@fixture
def setup_empty_database_real():
    connection = connect(database_name)
    clean_database(connection)
    yield build_database_with_empty_tables(connection)
    BancoDados(connection).close()


@fixture
def setup_empty_database_real_v2():
    """Return a connection"""
    connection = connect(database_name)
    clean_database(connection)
    yield build_database_with_empty_tables_v2(connection)
    BancoDados(connection).close()


@fixture
def setup_database_in_memory():
    connection = connect(memory_database)
    clean_database(connection)
    yield populate_database(connection)
    BancoDados(connection).close()


@fixture
def setup_database_in_real_db():
    connection = connect(database_name)
    clean_database(connection)
    yield populate_database(connection)
    BancoDados(connection).close()


@fixture
def cria_massa_dados():
    connection = connect(database_name)
    clean_database(connection)
    populate_database(connection)
    yield 1, 1
    BancoDados(connection).close()


@fixture
def enroll_student_in_course():
    connection = connect(database_name)
    clean_database(connection)
    populate_database(connection)

    student_obj = Controller(Aluno(), connection).pega_registro_por_id(1)

    course_obj = Controller(Curso(), connection).pega_registro_por_id(1)

    yield student_obj, course_obj, connection


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
