from tests.config import NOME_BANCO
from src.sql_client import SqlClient
from src.cursos import Curso, Cursos
from src.utils import limpa_tabelas


def test_lista_maximo_retorna_vazio_quando_nao_ha_registros():
    conn = SqlClient(NOME_BANCO)
    Cursos(conn).cria(nome="any")
    limpa_tabelas(conn)
    assert conn.lista_maximo(Curso) == []
