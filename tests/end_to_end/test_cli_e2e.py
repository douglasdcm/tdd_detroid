import subprocess
from src.sdk.courses import Courses
from src.sdk.students import Students
from src.disciplines import Disciplines
from src.schemes.course import CourseDB
from src.schemes.student import StudentDB
from src.schemes.discipline import MateriaBd
from src.schemes.for_association import MateriaStudentDB
from src.config import conn_external
from pytest import fixture
from time import sleep
from tests.utils import cria_curso, popula_banco_dados
from src.utils.utils import inicializa_tabelas


@fixture
def setup():
    inicializa_tabelas(conn_external)


@fixture
def __popula_banco_dados():
    popula_banco_dados()


def test_init_data_base():

    alunos = Students(conn_external)

    temp = subprocess.Popen(
        ["python", "cli.py", "init-bd"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    assert len(alunos.lista_tudo()) == 0
    assert "Database initialized" in output


def test_aluno_pode_lancar_notas(__popula_banco_dados):
    aluno_id = len(conn_external.lista_tudo(StudentDB))
    materia_id = 1
    nota = 7
    nota_bd = None

    temp = subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "lanca-nota",
            "--aluno-id",
            f"{aluno_id}",
            "--materia-id",
            f"{materia_id}",
            "--nota",
            f"{nota}",
        ],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())

    # verifica pelo banco
    materia_aluno = conn_external.lista_tudo(MateriaStudentDB)
    for ma in materia_aluno:
        if ma.aluno_id == aluno_id and ma.materia_id == materia_id:
            nota_bd = ma.aluno_nota
            break
    assert nota == nota_bd
    assert (
        f"Nota {nota} do aluno {aluno_id} na materia {materia_id} lancada com sucesso"
        in output
    )


def test_alunos_deve_inscreve_3_materias_no_minimo(__popula_banco_dados):

    alunos = Students(conn_external)
    alunos.create("any")
    aluno_id = len(alunos.lista_tudo())

    materias = Disciplines(conn_external)
    uma_materia = materias.lista_tudo()[0]
    materia_id = uma_materia.id
    curso_id = uma_materia.curso_id

    alunos.subscribe_in_course(aluno_id, curso_id)

    temp = subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "inscreve-materia",
            "--aluno-id",
            f"{aluno_id}",
            "--materia-id",
            f"{materia_id}",
        ],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())

    # verifica pelo banco
    materia_aluno = conn_external.lista_tudo(MateriaStudentDB)
    assert len(materia_aluno) > 1
    assert f"Aluno deve se inscrever em 3 materias no minimo" in output


def test_aluno_pode_se_inscrever_em_curso(__popula_banco_dados):

    cursos = Courses(conn_external)
    cursos.cria("other")
    curso_id = len(cursos.lista_tudo())
    alunos = Students(conn_external)
    alunos.create("any")
    aluno_id = len(alunos.lista_tudo())

    temp = subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "inscreve-curso",
            "--aluno-id",
            f"{aluno_id}",
            "--curso-id",
            f"{curso_id}",
        ],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())

    aluno = alunos.lista(aluno_id)
    # verifica pela API
    assert aluno.curso_id == curso_id
    # verifica pelo banco
    assert conn_external.lista(StudentDB, aluno_id).curso_id == 4
    assert f"Aluno inscrito no curso 4" in output


def test_cli_materia_nome_igual_mas_id_diferente(setup):

    cria_curso(conn_external)
    cria_curso(conn_external)
    cria_curso(conn_external)
    cursos = Courses(conn_external)
    for _ in range(3):
        if len(cursos.lista_tudo()) >= 3:
            break
        sleep(1)
    materias = Disciplines(conn_external)
    materias.cria("any", 1)
    temp = subprocess.Popen(
        ["python", "cli.py", "materia", "cria", "--nome", "other", "--curso-id", "1"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    # verifica pela API
    assert len(materias.lista_tudo()) == 2
    assert materias.lista(1).nome == "any"
    assert materias.lista(2).nome == "other"
    assert materias.lista(2).curso_id == 1
    # verifica banco de dados
    assert len(conn_external.lista_tudo(MateriaBd)) == 2
    assert conn_external.lista(MateriaBd, 1).nome == "any"
    assert conn_external.lista(MateriaBd, 2).nome == "other"
    assert f"Materia definida: id 2, nome other" in output


def test_cli_aluno_deve_ter_nome(setup):

    alunos = Students(conn_external)
    subprocess.Popen(
        ["python", "cli.py", "aluno", "cria", "--nome", "any"],
        stdout=subprocess.PIPE,
    ).communicate()
    temp = subprocess.Popen(
        ["python", "cli.py", "aluno", "cria", "--nome", "other"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    # verifica pela API
    assert len(alunos.lista_tudo()) == 2
    assert alunos.lista(1).nome == "any"
    assert alunos.lista(2).nome == "other"
    # verifica banco de dados
    assert len(conn_external.lista_tudo(StudentDB)) == 2
    assert conn_external.lista(StudentDB, 1).nome == "any"
    assert conn_external.lista(StudentDB, 2).nome == "other"
    assert f"Aluno definido: id 2, nome other" in output


def test_cli_curso_com_nome_e_id(setup):
    cursos = Courses(conn_external)
    cursos.cria("any")
    temp = subprocess.Popen(
        ["python", "cli.py", "curso", "cria", "--nome", "other"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    assert f"Curso definido: id 2, nome other" in output
    # verifica pela API
    assert len(cursos.lista_tudo()) == 2
    assert cursos.lista(1).nome == "any"
    assert cursos.lista(2).nome == "other"
    # verifica banco de dados
    assert len(conn_external.lista_tudo(CourseDB)) == 2
    assert conn_external.lista(CourseDB, 1).nome == "any"
    assert conn_external.lista(CourseDB, 2).nome == "other"
    assert f"Curso definido: id 2, nome other" in output
