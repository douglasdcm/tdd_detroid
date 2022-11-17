import src.cursos
import src.materias
import src.alunos
from src.sql_client import SqlClient


def limpa_tabelas(conn: SqlClient):
    conn.deleta_tabela(src.materias.Materia)
    conn.deleta_tabela(src.cursos.Curso)
    conn.deleta_tabela(src.alunos.Aluno)
