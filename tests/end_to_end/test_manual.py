from tests.utils import popula_banco_dados, cria_aluno_completo
from src.utils.utils import inicializa_tabelas
from src.config import conn
from pytest import mark
from src.controllers.student import AlunoBd


# @mark.skip(reason="Teste manual")
def test_popula_banco_para_test_manual():
    res = conn.lista_tudo(AlunoBd)
    print(res)
    # inicializa_tabelas(conn)
    # popula_banco_dados()
    # cria_aluno_completo(conn)


if __name__ == "__main__":
    test_popula_banco_para_test_manual()
