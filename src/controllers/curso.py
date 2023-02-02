from sqlalchemy.orm import Query
import src.disciplines
from src.schemes.course import CursoBd
from src.utils.sql_client import SqlClient
from src.utils.exceptions import ErroCurso, ErroBancoDados, ErroAluno


class CursoModelo:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn
        self._curso_id = None

    @property
    def id(self):
        return self._curso_id

    @id.setter
    def id(self, valor):
        self._curso_id = self.__pega_curso(valor)

    def __pega_curso(self, curso_id):
        try:
            return self._conn.lista(CursoBd, curso_id)
        except ErroBancoDados:
            raise ErroAluno(f"Curso {curso_id} não existe")

    def verifica_existencia(self, curso_id):
        self.__pega_curso(curso_id)

    def cria(self, nome):
        self.__verifica_nome(nome)
        self.__verifica_existem_3_cursos()
        self.__verifica_curso_inexistente(nome)
        self._conn.cria(CursoBd(nome=nome))
        self._curso_id = len(self._conn.lista_tudo(CursoBd))

    def __verifica_nome(self, nome):
        if len(nome.strip()) == 0:
            raise ErroCurso("Nome do curso invalido")

    def __verifica_curso_inexistente(self, nome):
        query = Query(CursoBd).filter(CursoBd.nome == nome)
        if len(self._conn.roda_query(query)) > 0:
            raise ErroCurso(f"Existe outro curso com o nome {nome}")

    def __verifica_existem_3_cursos(self):
        query_cursos = Query([CursoBd])

        resultado = len(self._conn.roda_query(query_cursos))
        if resultado < 3:
            return

        query_materias = Query([src.disciplines.MateriaBd]).group_by(
            src.disciplines.MateriaBd.curso_id, src.disciplines.MateriaBd.id
        )
        resultado = len(self._conn.roda_query(query_materias))

        if resultado < 3:
            raise ErroCurso(
                "Necessários 3 cursos com 3 três matérias para se criar novos cursos"
            )
