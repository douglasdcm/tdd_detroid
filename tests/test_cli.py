import subprocess
from src.cursos import Cursos
from src.banco_dados import BancoDados as bd
from src.config import NOME_BANCO
from pytest import fixture
from src.alunos import Alunos


@fixture
def setup():
    conn = bd(NOME_BANCO)
    try:
        conn.deleta_tabela(Cursos)
        conn.deleta_tabela(Alunos)
    except:
        pass


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
    assert len(conn.lista_tudo(Alunos)) == 2
    assert conn.lista(Alunos, 1) == [(1, "any")]
    assert conn.lista(Alunos, 2) == [(2, "other")]
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
    assert len(conn.lista_tudo(Cursos)) == 2
    assert conn.lista(Cursos, 1) == [(1, "any")]
    assert conn.lista(Cursos, 2) == [(2, "other")]
    assert f"Curso definido: id 2, nome other" in output
