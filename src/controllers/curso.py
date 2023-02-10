from src.storage.course import CourseStorage


class CursoModelo:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn
        self._curso_id = None
        self._storage = CourseStorage()

    @property
    def id(self):
        return self._curso_id

    @id.setter
    def id(self, valor):
        self._curso_id = self._storage.get_course(valor)

    def verifica_existencia(self, curso_id):
        self.__pega_curso(curso_id)

    def cria(self, nome):
        self._storage.check_name(nome)
        self._storage.check_has_tree_courses()
        self._storage.check_course_exists(nome)
        self._curso_id = self._storage.create_course(nome)
