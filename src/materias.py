from src.utils.sql_client import SqlClient
from src.esquemas.materia import MateriaBd
from src.modelos.materia import MateriaModelo


class Materias:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def cria(self, nome, curso_id: int):
        """
        :nome nome da matéria
        :curso curso associado à matéria
        """
        MateriaModelo(self._conn).cria(nome, curso_id)

    def lista_tudo(self):
        return self._conn.lista_tudo(MateriaBd)

    def lista(self, id_):
        return self._conn.lista(MateriaBd, id_)
