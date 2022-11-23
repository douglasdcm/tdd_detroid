from src.modelos.materia import MateriaModelo
from src.esquemas.materia import MateriaBd
from tests.config import conn


def test_materia_cria(popula_banco_dados):
    materia = MateriaModelo(conn)
    materia.cria(nome="any", curso_id=1)
    assert conn.lista(MateriaBd, 4).nome == "any"
