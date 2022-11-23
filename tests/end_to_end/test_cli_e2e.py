import subprocess
from src.cursos import Cursos
from src.alunos import Alunos
from src.materias import Materias
from src.esquemas.curso import CursoBd
from src.esquemas.aluno import AlunoBd
from src.esquemas.materia import MateriaBd
from src.esquemas.para_associacao import MateriaAlunoBd
from config import conn
from pytest import fixture
from time import sleep
from tests.utils import cria_materia, cria_curso


@fixture
def setup():
    subprocess.Popen(
        ["python", "cli.py", "init-bd"],
        stdout=subprocess.PIPE,
    ).communicate()


@fixture
def popula_banco_dados():
    cria_curso(conn)
    cria_curso(conn)
    cria_curso(conn)
    for _ in range(3):
        cria_materia(conn, 1)
        cria_materia(conn, 2)
        cria_materia(conn, 3)


def test_init_banco_dados():

    alunos = Alunos(conn)

    temp = subprocess.Popen(
        ["python", "cli.py", "init-bd"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    assert len(alunos.lista_tudo()) == 0
    assert "Banco de dados inicializado" in output


def test_alunos_deve_inscreve_3_materias_no_minimo(setup, popula_banco_dados):

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

    # verifica pelo banco
    ta = conn.lista_tudo(MateriaAlunoBd)
    assert len(ta) == 1
    assert f"Aluno deve se inscrever em 3 materias no minimo" in output


def test_aluno_pode_se_inscrever_em_curso(setup, popula_banco_dados):

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
    assert conn.lista(AlunoBd, 1).curso_id == 4
    assert f"Aluno inscrito no curso 4" in output


def test_cli_materia_nome_igual_mas_id_diferente(setup):

    cria_curso(conn)
    cria_curso(conn)
    cria_curso(conn)
    cursos = Cursos(conn)
    for _ in range(3):
        if len(cursos.lista_tudo()) >= 3:
            break
        sleep(1)
    materias = Materias(conn)
    materias.cria("any", 1)
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
    assert len(conn.lista_tudo(MateriaBd)) == 2
    assert conn.lista(MateriaBd, 1).nome == "any"
    assert conn.lista(MateriaBd, 2).nome == "other"
    assert f"Materia definida: id 2, nome other" in output


def test_cli_aluno_deve_ter_nome(setup):

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
    assert len(conn.lista_tudo(AlunoBd)) == 2
    assert conn.lista(AlunoBd, 1).nome == "any"
    assert conn.lista(AlunoBd, 2).nome == "other"
    assert f"Aluno definido: id 2, nome other" in output


def test_cli_curso_com_nome_e_id(setup):
    cursos = Cursos(conn)
    cursos.cria("any")
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
    assert len(conn.lista_tudo(CursoBd)) == 2
    assert conn.lista(CursoBd, 1).nome == "any"
    assert conn.lista(CursoBd, 2).nome == "other"
    assert f"Curso definido: id 2, nome other" in output
