import src.cursos
import src.materias
import src.alunos
from src.sql_client import SqlClient


def inicializa_tabelas(conn: SqlClient):
    conn.inicializa_tabela(src.cursos.CursoBd)
    conn.inicializa_tabela(src.alunos.Aluno)
    conn.inicializa_tabela(src.materias.Materia)
