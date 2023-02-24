import uuid
from src.controllers import courses
from src.controllers import disciplines
from src.controllers import students
from pytest import raises
from src.utils.utils import inicializa_tabelas


def popula_banco_dados():
    "create 3 cursos com 3 matérias cada, create aluno, inscreve em um dos cursos e inscreve em 3 matérias"
    inicializa_tabelas()
    create_curso()
    create_curso()
    create_curso()
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


def create_materia(curso_id):
    nome_aleatorio = str(uuid.uuid4())
    disciplines.create(nome_aleatorio, curso_id)


def create_curso():
    nome_aleatorio = str(uuid.uuid4())
    courses.create(nome_aleatorio)
