from src.schemes.for_association import MateriaAlunoBd
from src.utils.sql_client import SqlClient
import uuid


def generate_random_value():
    return str(uuid.uuid4())


def inicializa_tabelas(conn: SqlClient):
    conn.create_schema()
    conn.init_table(MateriaAlunoBd)
    conn.grant_permissions()
