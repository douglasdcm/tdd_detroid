from sqlalchemy import Column, Integer, String
from src.sql_client import Base, SqlClient


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)


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

    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def cria(self, nome):
        aluno = Aluno(nome=nome)
        self._conn.cria(aluno)
        return True

    def lista_tudo(self):
        return self._conn.lista_tudo(Aluno)

    def lista(self, id_):
        return self._conn.lista(Aluno, id_)
