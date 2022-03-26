from pytest import fixture
from src.controller.controller import Controller
from src.model.aluno import Aluno
from tests.massa_dados import aluno_nome_1


class TestControllerAluno:
    @fixture(scope="function")
    def setup(self, setup_database_in_memory):
        self.controller = Controller(
            Aluno("student_new_name"), setup_database_in_memory
        )

    def test_aluno_pode_ser_deletado_do_banco(self, setup):
        aluno_id = 1
        expected = 4
        self.controller.deleta(aluno_id)
        actual = len(self.controller.get_all())
        assert actual == expected

    def test_aluno_criado_banco_dados_controller(self, setup):
        expected = "student_new_name"
        self.controller.salva()
        actual = self.controller.get_by_biggest_id().pega_nome()
        assert actual == expected
