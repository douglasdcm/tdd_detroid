from src.banco_dados import BancoDados as bd
from pytest import fixture
from tests.config import NOME_BANCO
from src.utils import create_tables


def __create_tables(conn):
    try:
        create_tables(conn)
    except:
        pass


@fixture(scope="function", autouse=True)
def setup_bando_dados():
    conn = bd(NOME_BANCO)
    __create_tables(conn)
