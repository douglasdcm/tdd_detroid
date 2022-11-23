from src.modelos.curso import CursoModelo
from src.esquemas.curso import CursoBd
from src.utils.sql_client import SqlClient


class Cursos:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def cria(self, nome):
        CursoModelo(self._conn).cria(nome)

    def lista_tudo(self):
        return self._conn.lista_tudo(CursoBd)

    def lista(self, id_):
        return self._conn.lista(CursoBd, id_)
