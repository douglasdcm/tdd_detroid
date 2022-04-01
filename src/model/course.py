from src.model.discipline import Discipline


class Course:
    def __init__(self) -> None:
        self.__disciplines = []
        self.__id = None

    def get_id(self):
        return self.__id

    def set_id(self, id_):
        self.__id = id_

    def add_discipline(self, discipline):
        self.__disciplines.append(discipline)
        return True

    def get_disciplines(self):
        return self.__disciplines
