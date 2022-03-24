from tests.massa_dados import aluno_nome_1
from src.controller.controller import Controller


class TestBdAlunos:
    def test_aluno_criado_foi_salvo_banco_dados(
        self, setup_database_in_memory, cria_aluno
    ):
        expected = aluno_nome_1
        controller = Controller(cria_aluno, setup_database_in_memory)
        controller.salva()
        actual = controller.get_all()
        assert actual[0].pega_nome() == expected
