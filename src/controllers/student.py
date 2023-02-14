from src.controllers.curso import CourseController
from src.controllers.materia import DisciplineController
from src.business_logic.student import StudentBL
from src.storage.student import StudentStorage


class StudentController:
    def __init__(self, conn) -> None:
        self._conn = conn
        self._aluno_id = None
        self._student_bl = StudentBL()
        self._storage = StudentStorage()

    @property
    def id(self):
        return self._aluno_id

    @id.setter
    def id(self, valor):
        self._aluno_id = valor
        self._storage.get_student(self._aluno_id)

    def set_grade(self, discipline_id, grade):
        grade = int(grade)
        self._student_bl.check_grade_boundaries(grade)
        self._storage.check_student_in_discipline(self._aluno_id, discipline_id)
        self._storage.update_grade(self._aluno_id, discipline_id, grade)
        self._storage.calculate_coef_rend(self._aluno_id)

    def create(self, nome):
        nome = self._student_bl.clear_name(nome)
        res = self._storage.create(nome)
        self._aluno_id = self._storage.get_maximum_id()
        return res

    def subscribe_in_discipline(self, materia_id):
        curso_id = self._storage.get_course_id(self._aluno_id)
        DisciplineController(self._conn).check_exists(materia_id, curso_id)
        self._storage.check_student_already_in_discipline(self._aluno_id, materia_id)
        self._storage.subscribe_in_discipline(self._aluno_id, materia_id)
        self._storage.check_student_in_tree_disciplines(self._aluno_id)

    def subscribe_in_course(self, curso_id):
        self._storage.get_student(self._aluno_id)
        CourseController().check_exists(curso_id)
        self._storage.can_subscribe_course(self._aluno_id)
        self._storage.subcribe_in_course(self._aluno_id, curso_id)
