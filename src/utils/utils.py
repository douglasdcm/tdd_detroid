from src.utils import sql_client
from src.utils.exceptions import ErrorInvalidInteger
# import uuid


# def generate_random_value():
#     return str(uuid.uuid4())

def convert_id_to_integer(id_):
    if isinstance(id_, int):
        return id_
    try:
        id_ = int(id_)
    except Exception:
        raise ErrorInvalidInteger("Id is not a valid integer")
    return id_


def inicializa_tabelas():
    sql_client.create_schema()
    sql_client.init_table()
    sql_client.grant_permissions()
