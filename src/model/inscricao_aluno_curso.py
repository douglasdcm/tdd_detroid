from src.model.aluno import Aluno
from src.model.curso import Curso
from src.enums.enums import SituacaoCurso, Situacao
from src.exceptions.exceptions import InvalidStatus


class InscricaoAlunoCurso:
    def __init__(self):
        self.__student = None
        self.__course = None

    def subscribe(self, student: Aluno, course: Curso):
        if (
            course.pega_situacao() == SituacaoCurso.available.value
            and student.get_status() == Situacao.unsubscribed.value
        ):
            student.set_course(course)
            course.add_student(student)
            self.__student = student
            self.__course = course
            return True
        else:
            raise (
                InvalidStatus(
                    "The student status must be 'unsubscribed' and the course status must be 'available' to subscribe."
                )
            )

    def unsubscribe(self, student, course):
        return True

    def get_student(self) -> Aluno:
        return self.__student

    def get_course(self) -> Curso:
        return self.__course
