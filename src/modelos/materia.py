from sqlalchemy.orm import Query
from src.esquemas.curso import CursoBd
from src.utils.sql_client import SqlClient
from src.esquemas.materia import MateriaBd
from src.utils.exceptions import ErroBancoDados, ErroMateria


class MateriaModelo:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def __eh_materia_unica(self, nome, curso_id):
        query = Query([MateriaBd]).filter(
            MateriaBd.nome == nome, MateriaBd.curso == curso_id
        )
        if self._conn.roda_query(query):
            raise ErroMateria("O curso já possui uma matéria com este nome")
        return True

    def __existem_3_cursos(self):
        if len(self._conn.lista_tudo(CursoBd)) < 3:
            raise ErroMateria("Necessários 3 cursos para se criar a primeira matéria")
        return True

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
        self.__eh_materia_unica(nome, curso_id)
        self.__existem_3_cursos()
        self.__existe_curso(curso_id)
        materia = MateriaBd(nome=nome, curso=curso_id)
        self._conn.cria(materia)
