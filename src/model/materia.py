import time
class Materia:
    def __init__(self, nome):
        self._identificador_unico = time.time()
        self._nome = nome

    def pega_identificador_unico(self):
        return self._identificador_unico

    def pega_nome(self):
        return self._nome
