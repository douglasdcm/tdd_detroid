from src.model.banco_dados import BancoDados
from src.controller.controller import Controller
from src.model.aluno import Aluno
from src.model.banco_dados import BancoDados
from tests.massa_dados import aluno_nome_1

class TestControllerAluno:

    def test_aluno_criado_banco_dados(self, cria_banco):
        expected = {1: aluno_nome_1}
        controller = Controller(Aluno(aluno_nome_1), cria_banco)
        controller.salva()
        actual = controller.pega_registros()
        assert actual == expected
