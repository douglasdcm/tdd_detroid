from tests.config import conn
from src.cursos import Curso


def test_lista_maximo_retorna_vazio_quando_nao_ha_registros():
    conn.inicializa_tabela(Curso)
    assert conn.lista_maximo(Curso) == []
