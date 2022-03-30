import time


class Materia:
    def __init__(self, nome=None):
        self._nome = nome
        self._id = None
        self.__grade = 0

    def define_id(self, id):
        self._id = id
        return self

    def pega_id(self):
        return self._id

    def pega_nome(self):
        return self._nome

    def set_grade(self, grade):
        self.__grade = grade
        return self
