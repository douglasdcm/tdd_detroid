from src.utils.sql_client import SqlClient
from src.schemes.discipline import MateriaBd
from src.models.materia import MateriaModelo


class Disciplines:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def cria(self, nome, curso_id: int):
        """
        :nome nome da matéria
        :curso curso associado à matéria
        """
        assert isinstance(curso_id, int), "curso_id must be an integer"
        MateriaModelo(self._conn).cria(nome, curso_id)

    def lista_tudo(self):
        return self._conn.lista_tudo(MateriaBd)

    def lista(self, id_):
        assert isinstance(id_, int), "id_ must be an integer"
        return self._conn.lista(MateriaBd, id_)
