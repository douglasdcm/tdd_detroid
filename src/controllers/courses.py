from src.utils.exceptions import ErrorCourse, ErroBancoDados, ErroAluno
from sqlalchemy.orm import Query
from src.schemes.course import CourseDB
from src.utils import sql_client
from src.schemes.discipline import MateriaBd


def check_name(nome):
    if len(nome.strip()) == 0:
        raise ErrorCourse("Nome do curso invalido")


def get_course(curso_id):
    try:
        return sql_client.get(CourseDB, curso_id)
    except ErroBancoDados:
        raise ErroAluno(f"Curso {curso_id} não existe")


def check_exists(course_id):
    get_course(course_id)


def check_exists_three():
    query_cursos = Query([CourseDB])

    resultado = len(sql_client.run_query(query_cursos))
    if resultado < 3:
        return

    query_materias = Query([MateriaBd]).group_by(
        MateriaBd.curso_id, MateriaBd.id
    )
    resultado = len(sql_client.run_query(query_materias))

    if resultado < 3:
        raise ErrorCourse(
            "Necessários 3 cursos com 3 três matérias para se criar novos cursos"
        )


def check_non_existent(nome):
    query = Query(CourseDB).filter(CourseDB.nome == nome)
    if len(sql_client.run_query(query)) > 0:
        raise ErrorCourse(f"Existe outro curso com o nome {nome}")


def get(id_):
    return sql_client.get(CourseDB, id_)


def get_all():
    return sql_client.get_all(CourseDB)


def create(nome):
    check_name(nome)
    check_exists_three()
    check_non_existent(nome)
    sql_client.create(CourseDB(nome=nome))
