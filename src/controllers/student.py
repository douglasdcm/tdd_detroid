from src.utils.sql_client import SqlClient
from src.controllers.materia import DisciplineController
from src.externals.student import StudentExternals


class StudentController:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn
        self._aluno_id = None
        self._externals = StudentExternals(conn)

    @property
    def id(self):
        return self._aluno_id

    @id.setter
    def id(self, valor):
        self._aluno_id = valor
        self._externals.get_student(self._aluno_id)

    def set_grade(self, discipline_id, grade):
        grade = int(grade)
        self._externals.check_grade_boundaries(grade)
        self._externals.check_student_in_discipline(self._aluno_id, discipline_id)
        self._externals.update_grade(self._aluno_id, discipline_id, grade)
        self._externals.calculate_coef_rend(self._aluno_id)

    def create(self, nome):
        nome = self._externals.clear_name(nome)
        self._externals.create(nome)
        self._aluno_id = self._externals.get_maximum_id()

    def subscribe_in_discipline(self, materia_id):
        curso_id = self._externals.get_course_id(self._aluno_id)
        DisciplineController(self._conn).check_exists(materia_id, curso_id)
        self._aluno_id = self._externals.get_maximum_id()
        self._externals.check_student_already_in_discipline(self._aluno_id, materia_id)
        self._externals.subscribe_in_discipline(self._aluno_id, materia_id)
        self._externals.check_student_in_tree_disciplines(self._aluno_id)

    def subscribe_in_course(self, curso_id):
        self._externals.get_student(self._aluno_id)
        self._externals.can_subscribe_course(self._aluno_id)
        self._externals.subscribe_in_course(self._aluno_id, curso_id)
