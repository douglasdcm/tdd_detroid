from tests.utils import popula_banco_dados, cria_aluno_completo
from src.utils.utils import inicializa_tabelas
from config import conn
from pytest import mark


# @mark.skip(reason="Teste manual")
def test_popula_banco_para_test_manual():
    inicializa_tabelas(conn)
    popula_banco_dados()
    cria_aluno_completo(conn)
