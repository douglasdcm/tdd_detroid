import uuid
from src.controllers import courses
from src.controllers.materia import DisciplineController
from src.controllers import students
from tests.config import conn
from pytest import raises
from src.utils.utils import inicializa_tabelas


def popula_banco_dados():
    "create 3 cursos com 3 matérias cada, create aluno, inscreve em um dos cursos e inscreve em 3 matérias"
    inicializa_tabelas(conn)
    create_curso(conn)
    create_curso(conn)
    create_curso(conn)
    for i in range(3):
        for _ in range(3):
            create_materia(conn, i + 1)
            create_materia(conn, i + 1)
            create_materia(conn, i + 1)
    create_aluno_completo(conn)


def create_aluno_completo(conn):
    students.create("test_manual")
    student_id = len(students.get_all())
    students.subscribe_in_course(student_id, 1)
    with raises(Exception):
        students.subscribe_in_discipline(student_id, 1)
    with raises(Exception):
        students.subscribe_in_discipline(student_id, 2)
    students.subscribe_in_discipline(student_id, 3)


def create_materia(conn, curso_id):
    nome_aleatorio = str(uuid.uuid4())
    DisciplineController(conn).create(nome_aleatorio, curso_id)


def create_curso(conn):
    nome_aleatorio = str(uuid.uuid4())
    courses.create(nome_aleatorio)
