from tests.massa_dados import materia_nome_1
from tests.helper import executa_comando
from src.model.materia import Materia
from src.controller.controller import Controller
from pytest import fixture
from src.tabelas import materias


class TestMateriaCli:
    def test_should_create_discipline_by_cli_when_asked_for(
        self, setup_database_in_real_db
    ):
        nome = materia_nome_1
        expected = nome
        parametros = ["cria-materia", "--nome", nome]
        executa_comando(parametros)
        materia = Materia(nome)
        actual = (
            Controller(materia, setup_database_in_real_db)
            .get_by_biggest_id()
            .pega_nome()
        )
        assert actual == expected
