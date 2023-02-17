import uuid
from src.controllers.curso import CourseController
from src.controllers.materia import DisciplineController
from src.controllers.student import StudentController
from tests.config import conn
from pytest import raises
from src.utils.utils import inicializa_tabelas


def popula_banco_dados():
    "Cria 3 cursos com 3 matérias cada, cria aluno, inscreve em um dos cursos e inscreve em 3 matérias"
    inicializa_tabelas(conn)
    cria_curso(conn)
    cria_curso(conn)
    cria_curso(conn)
    for i in range(3):
        for _ in range(3):
            cria_materia(conn, i + 1)
            cria_materia(conn, i + 1)
            cria_materia(conn, i + 1)
    cria_aluno_completo(conn)


def cria_aluno_completo(conn):
    aluno = StudentController(conn)
    aluno.create("test_manual")
    aluno.subscribe_in_course(1)
    with raises(Exception):
        aluno.subscribe_in_discipline(1)
    with raises(Exception):
        aluno.subscribe_in_discipline(2)
    aluno.subscribe_in_discipline(3)


def cria_materia(conn, curso_id):
    nome_aleatorio = str(uuid.uuid4())
    DisciplineController(conn).cria(nome_aleatorio, curso_id)


def cria_curso(conn):
    nome_aleatorio = str(uuid.uuid4())
    CourseController(conn).create(nome_aleatorio)
