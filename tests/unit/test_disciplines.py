from src.controllers.materia import DisciplineController
from src.schemes.discipline import MateriaBd
from tests.config import conn


def test_materia_create(popula_banco_dados):
    materia = DisciplineController(conn)
    materia.create(nome="any", curso_id=1)
    materia_id = conn.lista_maximo(MateriaBd).id
    assert conn.get(MateriaBd, materia_id).nome == "any"
