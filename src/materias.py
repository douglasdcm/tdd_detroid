from sqlalchemy import Column, Integer, String, ForeignKey
from src.sql_client import Base
from sqlalchemy.orm import Query
import src.cursos
from sqlalchemy.orm import relationship


class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    curso = Column(Integer, ForeignKey("cursos.id", back_populates="children"))
    parent = relationship("Curso", back_populates="children")


class ErroMateria(Exception):
    pass


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

    def __init__(self, conn) -> None:
        self._conn = conn

    def __eh_materia_unica(self, nome, curso_id):
        query = Query([Materia]).filter(Materia.nome == nome, Materia.curso == curso_id)
        if self._conn.roda_query(query):
            raise ErroMateria("O curso já possui uma matéria com este nome")
        return True

    def __existem_3_cursos(self):
        if len(self._conn.lista_tudo(src.cursos.Curso)) < 3:
            raise ErroMateria("Necessários 3 cursos para se criar a primeira matéria")
        return True

    def cria(self, nome, curso_id: int):
        """
        :nome nome da matéria
        :curso curso associado à matéria
        """
        self.__eh_materia_unica(nome, curso_id)
        self.__existem_3_cursos()
        materia = Materia(nome=nome, curso=curso_id)
        self._conn.cria(materia)

    def lista_tudo(self):
        return self._conn.lista_tudo(Materia)

    def lista(self, id_):
        return self._conn.lista(Materia, id_)
