from src.utils.exceptions import ErrorCourse, ErrorDatabase, ErrorStudent
from sqlalchemy.orm import Query
from src.schemes.course import CourseDB
from src.utils import sql_client
from src.schemes.discipline import MateriaBd


def check_name(name):
    if len(name.strip()) == 0:
        raise ErrorCourse("name do course invalido")


def get_course(course_id):
    try:
        return sql_client.get(CourseDB, course_id)
    except ErrorDatabase:
        raise ErrorStudent(f"course {course_id} não existe")


def check_exists(course_id):
    get_course(course_id)


def check_exists_three():
    query_courses = Query([CourseDB])

    resultado = len(sql_client.run_query(query_courses))
    if resultado < 3:
        return

    query_materias = Query([MateriaBd]).group_by(
        MateriaBd.course_id, MateriaBd.id
    )
    resultado = len(sql_client.run_query(query_materias))

    if resultado < 3:
        raise ErrorCourse(
            "Necessários 3 courses com 3 três matérias para se criar novos courses"
        )


def check_non_existent(name):
    query = Query(CourseDB).filter(CourseDB.name == name)
    if len(sql_client.run_query(query)) > 0:
        raise ErrorCourse(f"Existe outro course com o name {name}")


def get(id_):
    return sql_client.get(CourseDB, id_)


def get_all():
    return sql_client.get_all(CourseDB)


def create(name):
    check_name(name)
    check_exists_three()
    check_non_existent(name)
    sql_client.create(CourseDB(name=name))
