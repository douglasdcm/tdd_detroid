from src.schemes.for_association import MateriaStudentDB
from src.utils.sql_client import SqlClient


def inicializa_tabelas(conn: SqlClient):
    conn.create_schema()
    conn.init_table(MateriaStudentDB)
    conn.grant_permissions()
