from src.model.banco_dados import BancoDados
from src.controller.controller_aluno import ControllerAluno
from src.model.aluno import Aluno
from src.model.banco_dados import BancoDados
from sqlite3 import connect

class TestControllerAluno:

    def test_aluno_criado_banco_dados(self, cria_banco):
        nome = "José"
        expected = [tuple((1, nome))]
        controller = ControllerAluno(Aluno(nome), cria_banco)
        controller.salva()
        actual = controller.pega_registro()
        assert actual == expected
