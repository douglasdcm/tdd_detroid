from src.utils.sql_client import SqlClient
from src.schemes.student import AlunoBd
from src.controllers.student import StudentController


class Students:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def set_grade(self, aluno_id, materia_id, nota):
        aluno = StudentController(self._conn)
        aluno.id = aluno_id
        aluno.set_grade(materia_id, nota)

    def subscribe_in_course(self, aluno_id, curso_id):
        aluno = StudentController(self._conn)
        aluno.id = aluno_id
        aluno.subscribe_in_course(curso_id)

    def subscribe_in_discipline(self, aluno_id, materia_id):
        aluno = StudentController(self._conn)
        aluno.id = aluno_id
        aluno.subscribe_in_discipline(materia_id)

    def create(self, nome):
        return StudentController(self._conn).create(nome)

    def lista_tudo(self):
        return self._conn.lista_tudo(AlunoBd)

    def lista(self, id_):
        return self._conn.lista(AlunoBd, id_)
