from sqlalchemy import Column, Integer, String, ForeignKey
from src.sql_client import Base, SqlClient
import src.cursos


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    coef_rend = Column(Integer)
    curso_id = Column(Integer, ForeignKey("cursos.id"))


class ErroAluno(Exception):
    pass


class Alunos:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def __pega_aluno(self, aluno_id):
        aluno = self._conn.lista(Aluno, aluno_id)
        if aluno:
            return aluno
        else:
            raise ErroAluno(f"Aluno {aluno_id} nao existe")

    def __curso_existe(self, curso_id):
        if self._conn.lista(src.cursos.CursoBd, curso_id):
            return
        else:
            raise ErroAluno(f"Curso {curso_id} nao existe")

    def __pode_inscrever_curso(self, aluno):
        if aluno.curso_id is not None:
            raise ErroAluno("Aluno esta inscrito em outro curso")

    def inscreve_curso(self, aluno_id, curso_id):
        aluno = self.__pega_aluno(aluno_id)
        self.__curso_existe(curso_id)
        self.__pode_inscrever_curso(aluno)
        aluno.curso_id = curso_id
        self._conn.confirma()

    def cria(self, nome):
        aluno = Aluno(nome=nome)
        self._conn.cria(aluno)
        self._id = self._conn.lista_maximo(Aluno).id

    def lista_tudo(self):
        return self._conn.lista_tudo(Aluno)

    def lista(self, id_):
        return self._conn.lista(Aluno, id_)
