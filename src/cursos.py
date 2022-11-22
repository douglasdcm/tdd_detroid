from src.sql_client import SqlClient
from src.curso_modelo import CursoModelo
from src.curso_bd import CursoBd


class Cursos:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn
        self._curso_modelo = CursoModelo(conn)

    def cria(self, nome):
        self._curso_modelo.valida_nome(nome)
        self._curso_modelo.valida_existem_3_cursos()
        self._curso_modelo.valida_curso_inexistente(nome)
        curso = CursoBd(nome=nome)
        return self._conn.cria(curso)

    def lista_tudo(self):
        return self._conn.lista_tudo(CursoBd)

    def lista(self, id_):
        return self._conn.lista(CursoBd, id_)
