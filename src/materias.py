from sqlalchemy import Column, Integer, String, ForeignKey
from src.sql_client import Base
from sqlalchemy.orm import Query
import src.cursos
from src.sql_client import SqlClient


class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    curso = Column(Integer, ForeignKey("cursos.id"))


class ErroMateria(Exception):
    pass


class Materias:
    def __init__(self, conn: SqlClient) -> None:
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

    def __existe_curso(self, curso_id):
        if self._conn.lista(src.cursos.Curso, curso_id) is None:
            raise ErroMateria(f"Curso {curso_id} não existe")

    def cria(self, nome, curso_id: int):
        """
        :nome nome da matéria
        :curso curso associado à matéria
        """
        self.__eh_materia_unica(nome, curso_id)
        self.__existem_3_cursos()
        self.__existe_curso(curso_id)
        materia = Materia(nome=nome, curso=curso_id)
        self._conn.cria(materia)

    def lista_tudo(self):
        return self._conn.lista_tudo(Materia)

    def lista(self, id_):
        return self._conn.lista(Materia, id_)
