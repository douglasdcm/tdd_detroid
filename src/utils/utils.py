from src.schemes.course import CursoBd
from src.schemes.discipline import MateriaBd
from src.schemes.student import AlunoBd
from src.schemes.for_association import MateriaAlunoBd
from src.utils.sql_client import SqlClient


def inicializa_tabelas(conn: SqlClient):
    conn.inicializa_tabela(CursoBd)
    conn.inicializa_tabela(AlunoBd)
    conn.inicializa_tabela(MateriaBd)
    conn.inicializa_tabela(MateriaAlunoBd)
