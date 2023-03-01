import uuid
from src.controllers import courses
from src.controllers import disciplines
from src.controllers import students
from pytest import raises
from src.utils.utils import inicializa_tabelas


def popula_banco_dados():
    "create 3 courses com 3 matérias cada, create aluno, inscreve em um dos courses e inscreve em 3 matérias"
    inicializa_tabelas()
    create_course()
    create_course()
    create_course()
    for i in range(3):
        for _ in range(3):
            create_materia(i + 1)
            create_materia(i + 1)
            create_materia(i + 1)
    create_aluno_completo()


def create_aluno_completo():
    students.create("test_manual")
    student_id = len(students.get_all())
    students.subscribe_in_course(student_id, 1)
    with raises(Exception):
        students.subscribe_in_discipline(student_id, 1)
    with raises(Exception):
        students.subscribe_in_discipline(student_id, 2)
    students.subscribe_in_discipline(student_id, 3)


def create_materia(course_id):
    name_aleatorio = str(uuid.uuid4())
    disciplines.create(name_aleatorio, course_id)


def create_course():
    name_aleatorio = str(uuid.uuid4())
    courses.create(name_aleatorio)
