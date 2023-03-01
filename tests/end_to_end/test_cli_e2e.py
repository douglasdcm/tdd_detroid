import subprocess
from src.controllers import courses, students, disciplines
from src.schemes.course import CourseDB
from src.schemes.student import StudentDB
from src.schemes.discipline import MateriaBd
from src.schemes.for_association import MateriaStudentDB
from src.utils import sql_client
from pytest import fixture
from time import sleep
from tests.utils import create_course, popula_banco_dados
from src.utils.utils import inicializa_tabelas


@fixture
def setup():
    inicializa_tabelas()


@fixture
def __popula_banco_dados():
    popula_banco_dados()


def test_init_data_base():

    temp = subprocess.Popen(
        ["python", "cli.py", "init-bd"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    assert len(students.get_all()) == 0
    assert "Database initialized" in output


def test_aluno_pode_lancar_notas(__popula_banco_dados):
    student_id = len(sql_client.get_all(StudentDB))
    discipline_id = 1
    nota = 7
    nota_bd = None

    temp = subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "lanca-nota",
            "--student-id",
            f"{student_id}",
            "--discipline-id",
            f"{discipline_id}",
            "--nota",
            f"{nota}",
        ],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())

    # verifica pelo banco
    materia_aluno = sql_client.get_all(MateriaStudentDB)
    for ma in materia_aluno:
        if ma.student_id == student_id and ma.discipline_id == discipline_id:
            nota_bd = ma.aluno_nota
            break
    assert nota == nota_bd
    assert (
        f"Nota {nota} do aluno {student_id} na materia {discipline_id} lancada com sucesso"
        in output
    )


def test_students_deve_inscreve_3_materias_no_minimo(__popula_banco_dados):
    students.create("any")
    student_id = len(students.get_all())

    uma_materia = disciplines.get_all()[0]
    discipline_id = uma_materia.id
    course_id = uma_materia.course_id

    students.subscribe_in_course(student_id, course_id)

    temp = subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "inscreve-materia",
            "--student-id",
            f"{student_id}",
            "--discipline-id",
            f"{discipline_id}",
        ],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())

    # verifica pelo banco
    materia_aluno = sql_client.get_all(MateriaStudentDB)
    assert len(materia_aluno) > 1
    assert "Aluno deve se inscrever em 3 materias no minimo" in output


def test_aluno_pode_se_inscrever_em_course(__popula_banco_dados):

    courses.create("other")
    course_id = len(courses.get_all())
    students.create("any")
    student_id = len(students.get_all())

    temp = subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "inscreve-course",
            "--student-id",
            f"{student_id}",
            "--course-id",
            f"{course_id}",
        ],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())

    aluno = students.get(student_id)
    # verifica pela API
    assert aluno.course_id == course_id
    # verifica pelo banco
    assert sql_client.get(StudentDB, student_id).course_id == 4
    assert "Aluno inscrito no course 4" in output


def test_cli_materia_name_igual_mas_id_diferente(setup):

    create_course()
    create_course()
    create_course()
    for _ in range(3):
        if len(courses.get_all()) >= 3:
            break
        sleep(1)
    disciplines.create("any", 1)
    temp = subprocess.Popen(
        ["python", "cli.py", "materia", "create", "--name", "other", "--course-id", "1"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    # verifica pela API
    assert len(disciplines.get_all()) == 2
    assert disciplines.get(1).name == "any"
    assert disciplines.get(2).name == "other"
    assert disciplines.get(2).course_id == 1
    # verifica banco de dados
    assert len(sql_client.get_all(MateriaBd)) == 2
    assert sql_client.get(MateriaBd, 1).name == "any"
    assert sql_client.get(MateriaBd, 2).name == "other"
    assert "Materia definida: id 2, name other" in output


def test_cli_aluno_deve_ter_name(setup):
    subprocess.Popen(
        ["python", "cli.py", "aluno", "create", "--name", "any"],
        stdout=subprocess.PIPE,
    ).communicate()
    temp = subprocess.Popen(
        ["python", "cli.py", "aluno", "create", "--name", "other"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    # verifica pela API
    assert len(students.get_all()) == 2
    assert students.get(1).name == "any"
    assert students.get(2).name == "other"
    # verifica banco de dados
    assert len(sql_client.get_all(StudentDB)) == 2
    assert sql_client.get(StudentDB, 1).name == "any"
    assert sql_client.get(StudentDB, 2).name == "other"
    assert "Aluno definido: id 2, name other" in output


def test_cli_course_com_name_e_id(setup):
    courses.create("any")
    temp = subprocess.Popen(
        ["python", "cli.py", "course", "create", "--name", "other"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    assert "course definido: id 2, name other" in output
    # verifica pela API
    assert len(courses.get_all()) == 2
    assert courses.get(1).name == "any"
    assert courses.get(2).name == "other"
    # verifica banco de dados
    assert len(sql_client.get_all(CourseDB)) == 2
    assert sql_client.get(CourseDB, 1).name == "any"
    assert sql_client.get(CourseDB, 2).name == "other"
    assert "course definido: id 2, name other" in output
