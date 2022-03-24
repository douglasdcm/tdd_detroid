from tests.massa_dados import materia_nome_1
from tests.helper import executa_comando
from src.model.materia import Materia
from src.controller.controller import Controller
from pytest import fixture
from src.tabelas import materias


class TestMateriaCli:
    def test_cria_materia_por_cli(self, setup_database_in_real_db):
        nome = materia_nome_1
        expected = nome
        parametros = ["cria-materia", "--nome", nome]
        executa_comando(parametros)
        materia = Materia(nome)
        registro = Controller(materia, setup_database_in_real_db).get_all()[0]
        actual = registro.pega_nome()
        assert actual == expected
