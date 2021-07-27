import time


class Materia:
    def __init__(self, nome):
        self._nome = nome
        self._id = None

    def define_id(self, id):
        self._id = id

    def pega_id(self):
        return self._id

    def pega_nome(self):
        return self._nome
