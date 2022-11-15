from src.banco_dados import BancoDados as bd
from src.manager import Manager, Tipos


class Materias:
    class Materia:
        def __init__(self) -> None:
            self._nome = None
            self._curso = None

        @property
        def curso(self):
            return self._curso

        @curso.setter
        def curso(self, valor):
            self._curso = valor

        @property
        def nome(self):
            return self._nome

        @nome.setter
        def nome(self, valor):
            self._nome = valor

    def __init__(self, conn: bd) -> None:
        self._conn = conn
        self._manager = Manager(conn)

    def cria(self, nome, curso):
        """
        :nome nome da matéria
        :curso curso associado à matéria
        """
        if self._manager.pode_criar_materia():
            item = {"nome": nome, "curso": curso}
            self._conn.cria(Tipos.MATERIAS.value, item)

    def lista_tudo(self):
        return self._conn.lista_tudo(Tipos.MATERIAS.value)

    def lista(self, id_):
        result = self._conn.lista(Tipos.MATERIAS.value, id_)[0]
        materia = self.Materia()
        materia.nome = result[1]
        materia.curso = result[2]
        return materia
