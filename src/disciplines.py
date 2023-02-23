from src.utils.sql_client import SqlClient
from src.schemes.discipline import MateriaBd
from src.controllers.materia import DisciplineController


class Disciplines:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def create(self, nome, curso_id: int):
        """
        :nome nome da matéria
        :curso curso associado à matéria
        """
        DisciplineController(self._conn).create(nome, curso_id)

    def get_all(self):
        return self._conn.get_all(MateriaBd)

    def lista(self, id_):
        return self._conn.get(MateriaBd, id_)
