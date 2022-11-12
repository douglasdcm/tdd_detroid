from src.banco_dados import BancoDados as bd, Tabela
from src.cursos import Cursos
from pytest import fixture
from tests.config import NOME_BANCO


@fixture(scope="function", autouse=True)
def setup():
    conn = bd(NOME_BANCO)
    tabela = Tabela(Cursos)
    tabela.colunas = "nome"
    try:
        conn.deleta_tabela(Cursos)
    except:
        pass
    conn.cria_tabela(tabela)
