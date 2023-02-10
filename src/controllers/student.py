<<<<<<< HEAD
from src.controllers.curso import CourseController
from src.controllers.materia import DisciplineController
=======
from src.utils.sql_client import SqlClient
from src.schemes.student import AlunoBd
from src.schemes.for_association import MateriaAlunoBd
from src.controllers.curso import CursoModelo
from src.utils.exceptions import ErroAluno, ErroBancoDados, ErroMateriaAluno
from src.controllers.materia import MateriaModelo
>>>>>>> parent of f573f1d... First test test_calcula_cr_aluno_como_media_simples_das_notas_lancadas working with postgREST calls
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

    async def create(self, nome):
        nome = self._student_bl.clear_name(nome)
        res = await self._storage.create(nome)
        self._aluno_id = await self._storage.get_maximum_id()
        return res

    def subscribe_in_discipline(self, materia_id):
        curso_id = self._student_storage.get_course_id(self._aluno_id)
        MateriaModelo(self._conn).verifica_existencia(materia_id, curso_id)
        self._student_storage.check_student_already_in_discipline(
            self._aluno_id, materia_id
        )
        self._student_storage.subscribe_in_discipline(self._aluno_id, materia_id)
        self._student_storage.check_student_in_tree_disciplines(self._aluno_id)

    def subscribe_in_course(self, curso_id):
        aluno = self._student_storage.get_student(self._aluno_id)
        CursoModelo(self._conn).verifica_existencia(curso_id)
        self._student_storage.can_subscribe_course(self._aluno_id)
        aluno.curso_id = curso_id
        self._conn.confirma()
