from src.model.student import Student
from src.libs.database import Database


class StudentDao:
    def __init__(self, connection) -> None:
        self.__connection = connection
        self.__table = "students"

    def update(self, student, id_):
        sets = "score = {}".format(student.get_score())
        return Database(self.__connection).update(self.__table, sets, id_)

    def create(self, student):
        score = student.get_score()
        return Database(self.__connection).save(self.__table, "score", score)

    def read(self, id_):
        data = Database(self.__connection).get_by_id(self.__table, id_)[0]
        student = Student()
        student.set_score(data[1])
        return student
