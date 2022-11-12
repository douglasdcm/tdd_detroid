from src.banco_dados import BancoDados as bd, Tabela
from src.cursos import Cursos
from pytest import fixture
from tests.config import NOME_BANCO
from src.alunos import Alunos


@fixture(scope="function", autouse=True)
def setup_bando_dados():
    conn = bd(NOME_BANCO)

    try:
        conn.deleta_tabela(Cursos)
        conn.deleta_tabela(Alunos)
    except:
        pass
    cursos = Tabela(Cursos)
    cursos.colunas = "nome"
    conn.cria_tabela(cursos)

    alunos = Tabela(Alunos)
    alunos.colunas = "nome"
    conn.cria_tabela(alunos)
