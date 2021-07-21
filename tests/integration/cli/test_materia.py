from tests.massa_dados import materia_nome_1
from tests.helper import executa_comando
from src.model.materia import Materia
from src.controller.controller import Controller
from pytest import fixture
from src.tabelas import materias


class TestMateriaCli:

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco_real):
        cria_banco_real.deleta_tabela(materias)

    def test_cria_materia_por_cli(self, cria_banco_real):
        nome = materia_nome_1
        expected = nome
        parametros = ["cria-materia", "--nome", nome]
        executa_comando(parametros)
        materia = Materia(nome)
        registro = Controller(materia, cria_banco_real).pega_registros()[0]
        actual = registro.pega_nome()
        assert actual == expected
