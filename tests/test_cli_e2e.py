import subprocess
from src.cursos import Cursos, Curso
from src.config import NOME_BANCO
from pytest import fixture
from src.alunos import Alunos, Aluno
from src.materias import Materias, Materia
import uuid
from src.sql_client import SqlClient
from time import sleep


@fixture
def setup():
    conn = SqlClient(NOME_BANCO)
    subprocess.Popen(
        ["python", "cli.py", "init-bd"],
        stdout=subprocess.PIPE,
    ).communicate()
    yield conn


@fixture
def popula_banco_dados():
    __cria_curso()
    __cria_curso()
    __cria_curso()
    for _ in range(3):
        __cria_materia(1)
        __cria_materia(2)
        __cria_materia(3)


def test_init_banco_dados(setup):
    conn = setup
    alunos = Alunos(conn)

    temp = subprocess.Popen(
        ["python", "cli.py", "init-bd"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    assert len(alunos.lista_tudo()) == 0
    assert "Banco de dados inicializado" in output


def __cria_curso():
    nome_aleatorio = str(uuid.uuid4())

    subprocess.Popen(
        ["python", "cli.py", "curso", "cria", "--nome", f"{nome_aleatorio}"],
        stdout=subprocess.PIPE,
    ).communicate()


def __cria_materia(curso_id):
    nome_aleatorio = str(uuid.uuid4())
    subprocess.Popen(
        [
            "python",
            "cli.py",
            "materia",
            "cria",
            "--nome",
            f"{nome_aleatorio}",
            "--curso",
            f"{curso_id}",
        ],
        stdout=subprocess.PIPE,
    ).communicate()


def test_alunos_deve_inscreve_3_materias_no_minimo(setup, popula_banco_dados):
    conn = setup
    alunos = Alunos(conn)
    alunos.cria("any")
    alunos.inscreve_curso(1, 1)

    temp = subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "inscreve-materia",
            "--aluno-id",
            "1",
            "--materia-id",
            "1",
        ],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())

    aluno = alunos.lista(1)
    # verifica pela API
    assert aluno.materias_id == [1]
    # verifica pelo banco
    assert conn.lista(Aluno, 1).materias_id == [1]
    assert f"Aluno deve se inscrever em 3 materias no minimo" in output


def test_nao_inscreve_em_curso_aluno_nao_existente(setup, popula_banco_dados):
    conn = setup
    Cursos(conn).cria("other")

    temp = subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "inscreve-curso",
            "--aluno-id",
            "1",
            "--curso-id",
            "4",
        ],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())

    assert f"Aluno 1 nao existe" in output


def test_alunos_pode_se_inscrever_em_apenas_um_curso(setup, popula_banco_dados):
    conn = setup
    Cursos(conn).cria("other")
    alunos = Alunos(conn)
    alunos.cria("any")

    subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "inscreve-curso",
            "--aluno-id",
            "1",
            "--curso-id",
            "4",
        ],
        stdout=subprocess.PIPE,
    )

    for _ in range(3):
        if alunos.lista(1).curso_id is not None:
            break
        sleep(1)

    temp = subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "inscreve-curso",
            "--aluno-id",
            "1",
            "--curso-id",
            "3",
        ],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())

    assert f"Aluno esta inscrito em outro curso" in output
    aluno = alunos.lista(1)
    # verifica pela API
    assert aluno.curso_id == 4


def test_alunos_pode_se_inscrever_em_curso(setup, popula_banco_dados):
    conn = setup
    Cursos(conn).cria("other")
    alunos = Alunos(conn)
    alunos.cria("any")

    temp = subprocess.Popen(
        [
            "python",
            "cli.py",
            "aluno",
            "inscreve-curso",
            "--aluno-id",
            "1",
            "--curso-id",
            "4",
        ],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())

    aluno = alunos.lista(1)
    # verifica pela API
    assert aluno.curso_id == 4
    # verifica pelo banco
    assert conn.lista(Aluno, 1).curso_id == 4
    assert f"Aluno inscrito no curso 4" in output


def test_cli_tres_cursos_com_tres_materias_cada(setup):
    conn = setup
    cursos = Cursos(conn)
    materias = Materias(conn)
    __cria_curso()
    __cria_curso()
    __cria_curso()
    for _ in range(3):
        __cria_materia(1)
        __cria_materia(2)
        __cria_materia(3)

    # verifica pela API
    assert len(cursos.lista_tudo()) == 3
    assert len(materias.lista_tudo()) == 9


def test_cli_materia_nome_igual_mas_id_diferente(setup):
    conn = setup
    __cria_curso()
    __cria_curso()
    __cria_curso()
    materias = Materias(conn)
    subprocess.Popen(
        ["python", "cli.py", "materia", "cria", "--nome", "any", "--curso", "1"],
        stdout=subprocess.PIPE,
    ).communicate()
    temp = subprocess.Popen(
        ["python", "cli.py", "materia", "cria", "--nome", "other", "--curso", "1"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    # verifica pela API
    assert len(materias.lista_tudo()) == 2
    assert materias.lista(1).nome == "any"
    assert materias.lista(2).nome == "other"
    assert materias.lista(2).curso == 1
    # verifica banco de dados
    assert len(conn.lista_tudo(Materia)) == 2
    assert conn.lista(Materia, 1).nome == "any"
    assert conn.lista(Materia, 2).nome == "other"
    assert f"Materia definida: id 2, nome other" in output


def test_cli_aluno_deve_ter_nome(setup):
    conn = setup
    alunos = Alunos(conn)
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
    assert len(conn.lista_tudo(Aluno)) == 2
    assert conn.lista(Aluno, 1).nome == "any"
    assert conn.lista(Aluno, 2).nome == "other"
    assert f"Aluno definido: id 2, nome other" in output


def test_cli_curso_com_nome_e_id(setup):
    conn = SqlClient(NOME_BANCO)
    cursos = Cursos(conn)
    subprocess.Popen(
        ["python", "cli.py", "curso", "cria", "--nome", "any"],
        stdout=subprocess.PIPE,
    ).communicate()
    temp = subprocess.Popen(
        ["python", "cli.py", "curso", "cria", "--nome", "other"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    # verifica pela API
    assert len(cursos.lista_tudo()) == 2
    assert cursos.lista(1).nome == "any"
    assert cursos.lista(2).nome == "other"
    # verifica banco de dados
    assert len(conn.lista_tudo(Curso)) == 2
    assert conn.lista(Curso, 1).nome == "any"
    assert conn.lista(Curso, 2).nome == "other"
    assert f"Curso definido: id 2, nome other" in output
