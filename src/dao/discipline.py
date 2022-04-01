from dis import dis
from src.model.discipline import Discipline
from src.model.student import Student
from src.libs.database import Database


class DisciplineDao:
    def __init__(self, connection) -> None:
        self.__connection = connection
        self.__table = "disciplines"

    def update(self, discipline, id_):
        sets = "grade = {}".format(discipline.get_grade())
        return Database(self.__connection).update(self.__table, sets, id_)

    def read(self, id_):
        row = Database(self.__connection).get_by_id(self.__table, id_)[0]
        discipline = Discipline()
        discipline.set_id(id_)
        discipline.set_grade(row[1])
        return discipline

    def create(self, discipline):
        grade = discipline.get_grade()
        return Database(self.__connection).save(self.__table, "grade", grade)
