import subprocess
from src.cursos import Cursos
from src.banco_dados import BancoDados as bd
from src.config import NOME_BANCO
from pytest import fixture, raises
from src.alunos import Alunos
from src.materias import Materias
from src.manager import Tipos


@fixture
def setup():
    subprocess.Popen(
        ["python", "cli.py", "init-bd"],
        stdout=subprocess.PIPE,
    ).communicate()


def test_init_banco_dados():
    conn = bd(NOME_BANCO)
    alunos = Alunos(conn)

    temp = subprocess.Popen(
        ["python", "cli.py", "init-bd"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    assert len(alunos.lista_tudo()) == 0
    assert "Banco de dados inicializado" in output


def __cria_curso():
    subprocess.Popen(
        ["python", "cli.py", "define-curso", "--nome", f"any"],
        stdout=subprocess.PIPE,
    ).communicate()


def __cria_materia(curso):
    subprocess.Popen(
        [
            "python",
            "cli.py",
            "define-materia",
            "--nome",
            f"any",
            "--curso",
            f"{curso}",
        ],
        stdout=subprocess.PIPE,
    ).communicate()


def test_cli_tres_cursos_com_tres_materias_cada(setup):
    conn = bd(NOME_BANCO)
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
    conn = bd(NOME_BANCO)
    __cria_curso()
    __cria_curso()
    __cria_curso()
    materias = Materias(conn)
    subprocess.Popen(
        ["python", "cli.py", "define-curso", "--nome", "any"],
        stdout=subprocess.PIPE,
    ).communicate()
    subprocess.Popen(
        ["python", "cli.py", "define-materia", "--nome", "any", "--curso", "1"],
        stdout=subprocess.PIPE,
    ).communicate()
    temp = subprocess.Popen(
        ["python", "cli.py", "define-materia", "--nome", "other", "--curso", "1"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    # verifica pela API
    assert len(materias.lista_tudo()) == 2
    assert materias.lista(1).nome == "any"
    assert materias.lista(2).nome == "other"
    assert materias.lista(2).curso == 1
    # verifica banco de dados
    assert len(conn.lista_tudo(Tipos.MATERIAS.value)) == 2
    assert conn.lista(Tipos.MATERIAS.value, 1) == [(1, "any", 1)]
    assert conn.lista(Tipos.MATERIAS.value, 2) == [(2, "other", 1)]
    assert f"Materia definida: id 2, nome other" in output


def test_cli_aluno_deve_ter_nome(setup):
    conn = bd(NOME_BANCO)
    alunos = Alunos(conn)
    subprocess.Popen(
        ["python", "cli.py", "define-aluno", "--nome", "any"],
        stdout=subprocess.PIPE,
    ).communicate()
    temp = subprocess.Popen(
        ["python", "cli.py", "define-aluno", "--nome", "other"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    # verifica pela API
    assert len(alunos.lista_tudo()) == 2
    assert alunos.lista(1).nome == "any"
    assert alunos.lista(2).nome == "other"
    # verifica banco de dados
    assert len(conn.lista_tudo(Tipos.ALUNOS.value)) == 2
    assert conn.lista(Tipos.ALUNOS.value, 1) == [(1, "any")]
    assert conn.lista(Tipos.ALUNOS.value, 2) == [(2, "other")]
    assert f"Aluno definido: id 2, nome other" in output


def test_cli_curso_com_nome_e_id(setup):
    conn = bd(NOME_BANCO)
    cursos = Cursos(conn)
    subprocess.Popen(
        ["python", "cli.py", "define-curso", "--nome", "any"],
        stdout=subprocess.PIPE,
    ).communicate()
    temp = subprocess.Popen(
        ["python", "cli.py", "define-curso", "--nome", "other"],
        stdout=subprocess.PIPE,
    )
    output = str(temp.communicate())
    # verifica pela API
    assert len(cursos.lista_tudo()) == 2
    assert cursos.lista(1).nome == "any"
    assert cursos.lista(2).nome == "other"
    # verifica banco de dados
    assert len(conn.lista_tudo(Tipos.CURSOS.value)) == 2
    assert conn.lista(Tipos.CURSOS.value, 1) == [(1, "any")]
    assert conn.lista(Tipos.CURSOS.value, 2) == [(2, "other")]
    assert f"Curso definido: id 2, nome other" in output
