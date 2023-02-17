from src.utils.sql_client import SqlClient
from src.externals.courses import CourseExternals


class CourseController:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn
        self._curso_id = None
        self._externals = CourseExternals(conn)

    @property
    def id(self):
        return self._curso_id

    @id.setter
    def id(self, valor):
        self._curso_id = self._externals.get_course(valor)

    def create(self, nome):
        self._externals.check_name(nome)
        self._externals.check_three_courses()
        self._externals.check_non_existent_course(nome)
        self._externals.create_course(nome)
