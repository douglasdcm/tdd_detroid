from src.cursos import Cursos
from src.banco_dados import BancoDados as bd
from tests.config import NOME_BANCO


def test_salva_cursos_no_banco():
    conn = bd(NOME_BANCO)
    cursos = Cursos(conn)
    cursos.cria("any")
    assert len(cursos.lista_tudo()) == 1
    assert cursos.lista(1).nome == "any"
    assert len(conn.lista(Cursos, 1)) == 1
