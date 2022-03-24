from pytest import fixture
from src.controller.controller import Controller
from src.model.aluno import Aluno
from tests.massa_dados import aluno_nome_1


class TestControllerAluno:
    @fixture(autouse=True, scope="function")
    def setup(self, setup_database_in_memory):
        self.controller = Controller(Aluno(aluno_nome_1), setup_database_in_memory)
        self.controller.salva()

    def test_aluno_pode_ser_deletado_do_banco(self):
        expected = []
        aluno_id = 1
        self.controller.deleta(aluno_id)
        actual = self.controller.get_all()
        assert actual == expected

    def test_aluno_criado_banco_dados_controller(self):
        expected = aluno_nome_1
        actual = self.controller.get_all()
        assert actual[0].pega_nome() == expected
