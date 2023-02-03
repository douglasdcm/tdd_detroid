from sqlalchemy.orm import Query
from src.schemes.course import CursoBd
from src.utils.sql_client import SqlClient
from src.schemes.discipline import MateriaBd
from src.utils.exceptions import ErroBancoDados, ErroMateria


class DisciplineController:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def check_exists(self, materia_id, curso_id):
        query = Query([MateriaBd]).filter(
            MateriaBd.id == materia_id, MateriaBd.curso_id == curso_id
        )
        if len(self._conn.roda_query(query)) == 0:
            raise ErroMateria(f"Matéria {materia_id} não existe no curso {curso_id}")

    def __verifica_duplicidade(self, nome, curso_id):
        query = Query([MateriaBd]).filter(
            MateriaBd.nome == nome, MateriaBd.curso_id == curso_id
        )
        if self._conn.roda_query(query):
            raise ErroMateria("O curso já possui uma matéria com este nome")

    def __existem_3_cursos(self):
        if len(self._conn.lista_tudo(CursoBd)) < 3:
            raise ErroMateria("Necessários 3 cursos para se criar a primeira matéria")

    def __existe_curso(self, curso_id):
        try:
            self._conn.lista(CursoBd, curso_id)
        except ErroBancoDados:
            raise ErroMateria(f"Curso {curso_id} não existe")

    def cria(self, nome, curso_id):
        """
        :nome nome da matéria
        :curso curso associado à matéria
        """
        self.__verifica_duplicidade(nome, curso_id)
        self.__existem_3_cursos()
        self.__existe_curso(curso_id)
        materia = MateriaBd(nome=nome, curso_id=curso_id)
        self._conn.cria(materia)
