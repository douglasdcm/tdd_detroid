from tests.config import conn
from src.schemes.course import CourseDB


def test_create_roles():
    conn.grant_permissions()


def test_lista_maximo_retorna_vazio_quando_nao_ha_registros():
    conn.init_table(CourseDB)
    assert conn.lista_maximo(CourseDB) == []
