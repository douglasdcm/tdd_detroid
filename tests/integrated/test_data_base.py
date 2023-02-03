from tests.config import conn
from src.schemes.course import CursoBd


def test_create_roles():
    conn.grant_permissions()


def test_lista_maximo_retorna_vazio_quando_nao_ha_registros():
    conn.init_table(CursoBd)
    assert conn.lista_maximo(CursoBd) == []
