from sqlalchemy.orm import Query
import src.materias
from src.curso_bd import CursoBd
from src.sql_client import SqlClient


class ErroCurso(Exception):
    pass


class CursoModelo:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def valida_nome(self, nome):
        if len(nome.strip()) == 0:
            raise ErroCurso("Nome do curso invalido")

    def valida_curso_inexistente(self, nome):
        query = Query(CursoBd).filter(CursoBd.nome == nome)
        if self._conn.conta(query) > 0:
            raise ErroCurso(f"Existe outro curso com o nome {nome}")

    def valida_existem_3_cursos(self):
        query_cursos = Query([CursoBd])

        resultado = self._conn.conta(query_cursos)
        if resultado < 3:
            return

        query_materias = Query([src.materias.Materia]).group_by(
            src.materias.Materia.curso
        )
        resultado = self._conn.conta(query_materias)

        if resultado < 3:
            raise ErroCurso(
                "Necessários 3 cursos com 3 três matérias para se criar novos cursos"
            )
