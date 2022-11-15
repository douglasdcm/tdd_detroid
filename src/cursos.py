from src.manager import Manager, Tipos


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
        self._conn = conn
        self._manager = Manager(conn)

    def cria(self, nome):
        if self._manager.pode_criar_curso():
            item = {
                "nome": nome,
            }
            return self._conn.cria(Tipos.CURSOS.value, item)

    def lista_tudo(self):
        return self._conn.lista_tudo(Tipos.CURSOS.value)

    def lista(self, id_):
        result = self._conn.lista(Tipos.CURSOS.value, id_)[0]
        curso = self.Curso()
        curso.id_ = result[0]
        curso.nome = result[1]
        return curso
