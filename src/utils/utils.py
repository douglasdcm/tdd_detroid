from src.schemes.course import CursoBd
from src.schemes.discipline import MateriaBd
from src.schemes.student import AlunoBd
from src.schemes.for_association import MateriaAlunoBd
from src.utils.sql_client import SqlClient
import uuid


def generate_random_value():
    return str(uuid.uuid4())


def inicializa_tabelas(conn: SqlClient):
    # try:
    conn.init_table(MateriaAlunoBd)
    # conn.init_table(CursoBd)
    # conn.init_table(AlunoBd)
    # conn.init_table(MateriaBd)
    # except Exception:
    # pass
