from src.banco_dados import BancoDados as bd
from src.cursos import Cursos
from tests.config import NOME_BANCO


def test_lista_tudo_bd():
    item = {"nome": "any"}
    bd(NOME_BANCO).cria(Cursos, item)
    assert len(bd(NOME_BANCO).lista_tudo(Cursos)) == 1


def test_cria_item_bd():
    item = {"nome": "any"}
    assert bd(NOME_BANCO).cria(Cursos, item) == True


def test_lista_por_id_bd():
    assert len(bd(NOME_BANCO).lista(Cursos, 1)) == 0
