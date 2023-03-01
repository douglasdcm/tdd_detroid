from sqlalchemy.orm import Query
from src.schemes.course import CourseDB
from src.schemes.discipline import MateriaBd
from src.utils.exceptions import ErrorDatabase, ErrorDiscipline, ErrorInvalidInteger
from src.utils import sql_client
from src.utils.utils import convert_id_to_integer


def check_exists(discipline_id, course_id):
    query = Query([MateriaBd]).filter(
        MateriaBd.id == discipline_id, MateriaBd.course_id == course_id
    )
    if len(sql_client.run_query(query)) == 0:
        raise ErrorDiscipline(f"Matéria {discipline_id} não existe no course {course_id}")


def __verifica_duplicidade(name, course_id):
    query = Query([MateriaBd]).filter(
        MateriaBd.name == name, MateriaBd.course_id == course_id
    )
    if sql_client.run_query(query):
        raise ErrorDiscipline("O course já possui uma matéria com este name")


def __existem_3_courses():
    if len(sql_client.get_all(CourseDB)) < 3:
        raise ErrorDiscipline("Necessários 3 courses para se criar a primeira matéria")


def __existe_course(course_id):
    try:
        sql_client.get(CourseDB, course_id)
    except ErrorDatabase:
        raise ErrorDiscipline(f"course {course_id} não existe")


def get(id_):
    return sql_client.get(MateriaBd, id_)


def get_all():
    return sql_client.get_all(MateriaBd)


def get_maximum():
    return sql_client.get_maximum(MateriaBd)


def create(name, course_id):
    """
    :name name da matéria
    :course course associado à matéria
    """
    try:
        course_id = convert_id_to_integer(course_id)
    except ErrorInvalidInteger:
        raise ErrorDiscipline("Course id is not a valid integer")
    __verifica_duplicidade(name, course_id)
    __existem_3_courses()
    __existe_course(course_id)
    materia = MateriaBd(name=name, course_id=course_id)
    sql_client.create(materia)


