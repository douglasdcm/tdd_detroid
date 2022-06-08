from src.persister import Persister
from src.student import Student

persister = Persister()


class StudentController:

    def save(self):
        persister.save_student(1000, Student())

    def set_score(self, id_, score):
        student = persister.get_student(id_)
        student.set_score(score)
        persister.save_student(id_, student)

    def get_score(self, id_):
        student = persister.get_student(id_)
        return student.get_score()


class DisciplineController:

    def save(self, discipline):
        persister.get_discipline(self.__id)
