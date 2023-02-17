from sqlalchemy.orm import Query
import src.disciplines
from src.schemes.course import CourseDB
from src.utils.sql_client import SqlClient
from src.utils.exceptions import ErrorCourse, ErroBancoDados, ErroAluno


class CourseExternals:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn
        self._curso_id = None

    @property
    def id(self):
        return self._curso_id

    @id.setter
    def id(self, valor):
        self._curso_id = self.get_course(valor)

    def check_exists(self, course_id):
        self.get_course(course_id)

    def get_course(self, curso_id):
        try:
            return self._conn.lista(CourseDB, curso_id)
        except ErroBancoDados:
            raise ErroAluno(f"Curso {curso_id} não existe")

    def cria(self, nome):
        self.check_name(nome)
        self.check_three_courses()
        self.check_non_existent_course(nome)
        self._conn.cria(CourseDB(nome=nome))
        self._curso_id = len(self._conn.lista_tudo(CourseDB))

    def check_name(self, nome):
        if len(nome.strip()) == 0:
            raise ErrorCourse("Nome do curso invalido")

    def check_non_existent_course(self, nome):
        query = Query(CourseDB).filter(CourseDB.nome == nome)
        if len(self._conn.roda_query(query)) > 0:
            raise ErrorCourse(f"Existe outro curso com o nome {nome}")

    def create_course(self, nome):
        self._conn.cria(CourseDB(nome=nome))
        self._curso_id = len(self._conn.lista_tudo(CourseDB))

    def check_three_courses(self):
        query_cursos = Query([CourseDB])

        resultado = len(self._conn.roda_query(query_cursos))
        if resultado < 3:
            return

        query_materias = Query([src.disciplines.MateriaBd]).group_by(
            src.disciplines.MateriaBd.curso_id, src.disciplines.MateriaBd.id
        )
        resultado = len(self._conn.roda_query(query_materias))

        if resultado < 3:
            raise ErrorCourse(
                "Necessários 3 cursos com 3 três matérias para se criar novos cursos"
            )
