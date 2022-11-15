from src.banco_dados import BancoDados
from src.manager import Tipos


class Alunos:
    class Aluno:
        def __init__(self) -> None:
            self._nome = None

        @property
        def nome(self):
            return self._nome

        @nome.setter
        def nome(self, valor):
            self._nome = valor

    def __init__(self, conn: BancoDados) -> None:
        self._conn = conn

    def cria(self, nome):
        item = {"nome": nome}
        self._conn.cria(Tipos.ALUNOS.value, item)
        return True

    def lista_tudo(self):
        return self._conn.lista_tudo(Tipos.ALUNOS.value)

    def lista(self, id_):
        resultado = self._conn.lista(Tipos.ALUNOS.value, id_)[0]
        aluno = self.Aluno()
        aluno.nome = resultado[1]
        return aluno
