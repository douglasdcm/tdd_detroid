from sqlalchemy.orm import Query
from sqlalchemy import Column, Integer, String
from src.sql_client import Base
import src.materias
import src.cursos
from src.sql_client import SqlClient
from sqlalchemy.orm import relationship


class ErroCurso(Exception):
    pass


class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    children = relationship("Materia", back_populates="parent")


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

    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def __valida_3_cursos(self):
        query_cursos = Query([src.cursos.Curso])

        resultado = self._conn.conta(query_cursos)
        if resultado < 3:
            return

        query_materias = Query([src.materias.Materia]).group_by(
            src.materias.Materia.curso
        )
        resultado = self._conn.conta(query_materias)

        if resultado < 3:
            raise ErroCurso(
                "Necessários 3 cursos com 3 três matérias para se criar novos cursos"
            )

    def cria(self, nome):
        self.__valida_3_cursos()
        curso = Curso(nome=nome)
        return self._conn.cria(curso)

    def lista_tudo(self):
        return self._conn.lista_tudo(Curso)

    def lista(self, id_):
        return self._conn.lista(Curso, id_)
