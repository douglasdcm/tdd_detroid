from src.model.banco_dados import BancoDados
from src.controller.controller_aluno import ControllerAluno
from src.model.aluno import Aluno
from src.model.banco_dados import BancoDados
from sqlite3 import connect

class TestControllerAluno:

    def setup_method(self, method):
        self._bd = BancoDados(connect(":memory:"))

    def test_aluno_criado_banco_dados(self):
        nome = "José"
        expected = [tuple((1, nome))]
        controller = ControllerAluno(Aluno(nome), self._bd)
        controller.salva()
        actual = controller.pega_registro()
        assert actual == expected
