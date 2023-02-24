from src.schemes.discipline import MateriaBd
from src.controllers import disciplines
from src.utils import sql_client


def create(nome, curso_id: int):
    """
    :nome nome da matéria
    :curso curso associado à matéria
    """
    disciplines.create(nome, curso_id)


def get_all():
    return sql_client.get_all(MateriaBd)


def lista(id_):
    return sql_client.get(MateriaBd, id_)
