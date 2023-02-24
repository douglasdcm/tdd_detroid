from src.controllers import disciplines
from src.schemes.discipline import MateriaBd
from src.utils import sql_client


def test_materia_create(popula_banco_dados):
    disciplines.create(nome="any", curso_id=1)
    materia_id = sql_client.get_maximum(MateriaBd).id
    assert sql_client.get(MateriaBd, materia_id).nome == "any"
