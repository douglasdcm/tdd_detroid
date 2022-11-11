from src.banco_dados import BancoDados as bd
from src.config import NOME_BANCO


class Cursos:
    class Curso:
        def __init__(self):
            self._nome = None
            self._id = None

        @property
        def id_(self):
            return self._id

        @id_.setter
        def id_(self, id_):
            self._id = id_

        @property
        def nome(self):
            return self._nome

        @nome.setter
        def nome(self, nome):
            self._nome = nome

    def __init__(self, conn) -> None:
        self.__conn = conn

    def cria(self, nome):
        item = {
            "nome": nome,
        }
        return self.__conn.cria(Cursos, item)

    def lista_tudo(self):
        return self.__conn.lista_tudo(Cursos)

    def lista(self, id_):
        result = self.__conn.lista(Cursos, id_)[0]
        curso = self.Curso()
        curso.id_ = result[0]
        curso.nome = result[1]
        return curso
