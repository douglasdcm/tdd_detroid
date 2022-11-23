from src.esquemas.curso import CursoBd
from src.esquemas.materia import MateriaBd
from src.esquemas.aluno import AlunoBd
from src.esquemas.para_associacao import MateriaAlunoBd
from src.utils.sql_client import SqlClient


def inicializa_tabelas(conn: SqlClient):
    conn.inicializa_tabela(CursoBd)
    conn.inicializa_tabela(AlunoBd)
    conn.inicializa_tabela(MateriaBd)
    conn.inicializa_tabela(MateriaAlunoBd)
