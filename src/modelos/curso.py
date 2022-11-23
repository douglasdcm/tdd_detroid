from sqlalchemy.orm import Query
import src.materias
from src.esquemas.curso import CursoBd
from src.utils.sql_client import SqlClient
from src.utils.exceptions import ErroCurso, ErroBancoDados, ErroAluno


class CursoModelo:
    def __init__(self, conn: SqlClient, curso_id=None) -> None:
        self._conn = conn
        self._nome = None
        self._curso_id = curso_id
        if curso_id:
            self.__curso_existe(curso_id)

    @property
    def nome(self):
        return self._nome

    def cria(self, nome):
        self.__verifica_nome(nome)
        self.__verifica_existem_3_cursos()
        self.__verifica_curso_inexistente(nome)
        curso = CursoBd(nome=nome)
        self._conn.cria(curso)
        self._nome = nome

    def __curso_existe(self, curso_id):
        try:
            self._conn.lista(CursoBd, curso_id)
        except ErroBancoDados:
            raise ErroAluno(f"Curso {curso_id} nao existe")

    def __verifica_nome(self, nome):
        if len(nome.strip()) == 0:
            raise ErroCurso("Nome do curso invalido")

    def __verifica_curso_inexistente(self, nome):
        query = Query(CursoBd).filter(CursoBd.nome == nome)
        if self._conn.conta(query) > 0:
            raise ErroCurso(f"Existe outro curso com o nome {nome}")

    def __verifica_existem_3_cursos(self):
        query_cursos = Query([CursoBd])

        resultado = self._conn.conta(query_cursos)
        if resultado < 3:
            return

        query_materias = Query([src.materias.MateriaBd]).group_by(
            src.materias.MateriaBd.curso
        )
        resultado = self._conn.conta(query_materias)

        if resultado < 3:
            raise ErroCurso(
                "Necessários 3 cursos com 3 três matérias para se criar novos cursos"
            )
