import subprocess
from src.cursos import Cursos
from src.banco_dados import BancoDados as bd
from src.config import NOME_BANCO


def test_cli_curso_com_nome_e_id():
    nome = "any"
    id_ = "1"
    conn = bd(NOME_BANCO)
    cursos = Cursos(conn)
    temp = subprocess.Popen(
        ["python", "cli.py", "define_curso", id_, nome], stdout=subprocess.PIPE
    )
    output = str(temp.communicate())
    assert f"Curso definido: id {id_}, nome {nome}" in output
    # verifica pela API
    assert len(cursos.lista_tudo()) == 1
    assert nome == cursos.lista(id_).nome
    # verifica banco de dados
    assert len(conn.lista_tudo(Cursos)) == 1
    assert conn.lista(Cursos, 1) == [(1, "any")]
