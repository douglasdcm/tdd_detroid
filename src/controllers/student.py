from src.utils.sql_client import SqlClient
from src.schemes.student import AlunoBd
from src.schemes.for_association import MateriaAlunoBd
from src.controllers.curso import CourseController
from src.controllers.materia import DisciplineController
from src.business_logic.student import StudentBL
from src.storage.student import StudentStorage


class StudentController:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn
        self._aluno_id = None
        self._student_bl = StudentBL()
        self._student_storage = StudentStorage(conn)

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
        aluno = self._student_storage.get_student(self._aluno_id)
        CourseController(self._conn).check_exists(curso_id)
        self._student_storage.can_subscribe_course(self._aluno_id)
        # aluno.curso_id = curso_id
        # print("alunoCid", aluno.__dict__)
        # self._conn.confirma()
        # x = self._conn.lista(AlunoBd, self._aluno_id)
        # print("aluno update", x.__dict__)
        import requests
        import json

        url = f"http://minikube:30501/alunos?id=eq.{self._aluno_id}"

        payload = json.dumps({"curso_id": 1})
        headers = {"Content-Type": "application/json"}

        response = requests.request("PATCH", url, headers=headers, data=payload)

        print(response.text)
