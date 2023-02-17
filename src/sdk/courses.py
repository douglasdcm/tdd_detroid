from src.controllers.curso import CourseController
from src.schemes.course import CourseDB
from src.utils.sql_client import SqlClient


class Courses:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def cria(self, nome):
        CourseController(self._conn).create(nome)

    def lista_tudo(self):
        return self._conn.lista_tudo(CourseDB)

    def lista(self, id_):
        return self._conn.lista(CourseDB, id_)
