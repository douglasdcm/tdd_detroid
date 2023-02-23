from src.controllers import courses as controller
from src.schemes.course import CourseDB
from src.utils import sql_client


def create(nome):
    controller.create(nome)


def get_all():
    return sql_client.get_all(CourseDB)


def get(id_):
    return sql_client.get(CourseDB, id_)
