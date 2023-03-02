from sqlalchemy.orm import Query
from src.schemes.course import CourseDB
from src.utils.sql_client import SqlClient
from src.schemes.discipline import MateriaBd
from src.utils.exceptions import ErroBancoDados, ErroMateria
from src.utils import sql_client


class DisciplineController:
    def __init__(self, conn=None) -> None:
        pass

    def check_exists(self, materia_id, curso_id):
        query = Query([MateriaBd]).filter(
            MateriaBd.id == materia_id, MateriaBd.curso_id == curso_id
        )
        if len(sql_client.run_query(query)) == 0:
            raise ErroMateria(f"Matéria {materia_id} não existe no curso {curso_id}")

    def __verifica_duplicidade(self, nome, curso_id):
        query = Query([MateriaBd]).filter(
            MateriaBd.nome == nome, MateriaBd.curso_id == curso_id
        )
        if sql_client.run_query(query):
            raise ErroMateria("O curso já possui uma matéria com este nome")

    def __existem_3_cursos(self):
        if len(sql_client.get_all(CourseDB)) < 3:
            raise ErroMateria("Necessários 3 cursos para se criar a primeira matéria")

    def __existe_curso(self, curso_id):
        try:
            sql_client.get(CourseDB, curso_id)
        except ErroBancoDados:
            raise ErroMateria(f"Curso {curso_id} não existe")

    def create(self, nome, curso_id):
        """
        :nome nome da matéria
        :curso curso associado à matéria
        """
        self.__verifica_duplicidade(nome, curso_id)
        self.__existem_3_cursos()
        self.__existe_curso(curso_id)
        materia = MateriaBd(nome=nome, curso_id=curso_id)
        sql_client.create(materia)
