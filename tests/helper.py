from subprocess import PIPE, STDOUT, run
from src.config import ponto_entrada
from src.utils.tables import get_table_list
from src.model.banco_dados import BancoDados
from src.exceptions.exceptions import ComandoInvalido
from src import tabelas


def executa_comando(argumentos):
    try:
        comando = ["python", ponto_entrada]
        comando.extend(argumentos)
        return run(comando, stdout=PIPE, stderr=STDOUT, encoding="utf-8").stdout.strip()
    except Exception as e:
        raise ComandoInvalido(e)


def build_database_with_empty_tables(connection):
    tables = get_table_list()
    db = BancoDados(connection)
    for table in tables:
        db.create_table(table)
    return connection


def build_database_with_empty_tables_v2(connection=None):
    tables = get_table_list()
    db = BancoDados(connection)
    for table in tables:
        db.create_table(table)
    return connection


def clean_database(connection):
    tables = get_table_list()
    db = BancoDados(connection)
    for table in tables:
        db.deleta_tabela(table["name"])
    return connection


def populate_database(connection):
    tables = get_table_list()
    db = BancoDados(connection)
    for table in tables:
        db.create_table(table)
    students = [
        {"name": "student_name_1", "score": 10, "situation": "in progress"},
        {"name": "student_name_2", "score": 3, "situation": "in progress"},
        {"name": "student_name_3", "score": 5, "situation": "locked"},
        {"name": "student_name_4", "score": 0, "situation": "reproved"},
        {"name": "student_name_5", "score": 8, "situation": "approved"},
    ]
    disciplines = [
        {"nome": "discipline_1"},
        {"nome": "discipline_2"},
        {"nome": "discipline_3"},
    ]
    courses = [
        {"name": "course_1"},
        {"name": "course_2"},
        {"name": "course_3"},
    ]
    cursos = [
        {"nome": "course_1"},
        {"nome": "course_2"},
        {"nome": "course_3"},
    ]
    assoc_cursos_materia = [
        {"curso_id": 1, "materia_id": 1},
        {"curso_id": 1, "materia_id": 2},
        {"curso_id": 1, "materia_id": 3},
    ]
    assoc_aluno_cursos = [
        {"aluno_id": 1, "curso_id": 1},
    ]
    general_coordinator = [
        {
            "_": "coord_1",
        },
    ]
    db.save(tabelas.alunos, students)
    db.save(tabelas.materias, disciplines)
    db.save(tabelas.courses, courses)
    db.save(tabelas.cursos, cursos)
    db.save(tabelas.associa_curso_materia, assoc_cursos_materia)
    db.save(tabelas.inscricao_aluno_curso, assoc_aluno_cursos)
    db.save(tabelas.coordenador_geral, general_coordinator)
    return connection
