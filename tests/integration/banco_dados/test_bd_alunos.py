from tests.massa_dados import aluno_nome_1
from src.controller.controller import Controller


class TestBdAlunos:

    def test_aluno_criado_foi_salvo_banco_dados(self, cria_banco, cria_aluno):
        expected = aluno_nome_1
        controller = Controller(cria_aluno, cria_banco)
        controller.salva()
        actual = controller.pega_registros()
        assert actual[0].pega_nome() == expected
