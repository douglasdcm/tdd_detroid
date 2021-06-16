from tests.conftest import cria_curso_com_materias
from pytest import fixture
from src.model.banco_dados import BancoDados
from src.controller.controller import Controller
from src.model.aluno import Aluno
from src.model.banco_dados import BancoDados
from tests.massa_dados import aluno_nome_1
from src.tabelas import alunos
from src.enums.enums import Situacao

class TestControllerAluno:

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco):
        self.controller = Controller(Aluno(aluno_nome_1), cria_banco)
        self.controller.salva()

    def test_aluno_pode_ser_deletado_do_banco(self):
        expected = []
        aluno_id = 1
        self.controller.deleta(aluno_id)
        actual = self.controller.pega_registros()
        assert actual == expected

    def test_aluno_criado_banco_dados(self):
        expected = aluno_nome_1
        actual = self.controller.pega_registros()
        assert actual[0].pega_nome() == expected

