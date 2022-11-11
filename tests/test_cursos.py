from src.cursos import Cursos
from src.banco_dados import BancoDados as bd
from tests.config import NOME_BANCO


def test_cursos_cria():
    cursos = Cursos(conn=bd(NOME_BANCO))
    cursos.cria("any")
    assert cursos.lista(1).nome == "any"
    assert len(cursos.lista_tudo()) == 1
