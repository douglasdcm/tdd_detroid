from src.schemes.course import CourseDB
from src.utils import sql_client


def test_create_roles():
    sql_client.grant_permissions()


def test_lista_maximo_retorna_vazio_quando_nao_ha_registros():
    sql_client.init_table()
    assert sql_client.get_maximum(CourseDB) == []
