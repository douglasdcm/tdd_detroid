class Discipline:
    def __init__(self) -> None:
        self.__id = None
        self.__grade = 0

    def __eq__(self, other):
        return self.__id == other.get_id()

    def set_id(self, id_):
        self.__id = id_
        return True

    def get_id(self):
        return self.__id

    def set_name(self, name):
        return True

    def get_grade(self):
        return self.__grade

    def set_grade(self, grade):
        if self.__grade < grade:
            self.__grade = grade
        return True
