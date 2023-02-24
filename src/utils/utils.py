from src.utils import sql_client


def inicializa_tabelas():
    sql_client.create_schema()
    sql_client.init_table()
    sql_client.grant_permissions()
