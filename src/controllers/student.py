from src.utils.sql_client import SqlClient
from src.controllers.curso import CourseController
from src.controllers.materia import DisciplineController
from src.business_logic.student import StudentBL
from src.storage.student import StudentStorage
from src.utils.rest import patch


class StudentController:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn
        self._aluno_id = None
        self._student_bl = StudentBL()
        self._student_storage = StudentStorage()

    @property
    def id(self):
        return self._aluno_id

    @id.setter
    def id(self, valor):
        self._aluno_id = valor
        self._student_storage.get_student(self._aluno_id)

    def set_grade(self, discipline_id, grade):
        grade = int(grade)
        self._student_bl.check_grade_boundaries(grade)
        self._student_storage.check_student_in_discipline(self._aluno_id, discipline_id)
        self._student_storage.update_grade(self._aluno_id, discipline_id, grade)
        self._student_storage.calculate_coef_rend(self._aluno_id)

    def create(self, nome):
        nome = self._student_bl.clear_name(nome)
        self._student_storage.create(nome)
        self._aluno_id = self._student_storage.get_maximum_id()

    def subscribe_in_discipline(self, materia_id):
        curso_id = self._student_storage.get_course_id(self._aluno_id)
        DisciplineController(self._conn).check_exists(materia_id, curso_id)
        self._student_storage.check_student_already_in_discipline(
            self._aluno_id, materia_id
        )
        self._student_storage.subscribe_in_discipline(self._aluno_id, materia_id)
        self._student_storage.check_student_in_tree_disciplines(self._aluno_id)

    def subscribe_in_course(self, curso_id):
        self._student_storage.get_student(self._aluno_id)
        CourseController(self._conn).check_exists(curso_id)
        self._student_storage.can_subscribe_course(self._aluno_id)
        patch("alunos", self._aluno_id, {"curso_id": curso_id})
