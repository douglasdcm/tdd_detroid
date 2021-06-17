import time


class Materia:
    def __init__(self, nome):
        self._identificador_unico = time.time()
        self._nome = nome
        self._id = None

    def define_id(self, id):
        self._id = id

    def pega_identificador_unico(self):
        return self._identificador_unico

    def pega_nome(self):
        return self._nome
