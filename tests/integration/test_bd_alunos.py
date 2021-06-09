from tests.massa_dados import aluno_nome_1
from src.controller.controller import Controller
from src.enums.enums import Situacao

class TestBdAlunos:

    def test_aluno_criado_foi_salvo_banco_dados(self, cria_banco, cria_aluno):
        cr = 0
        situacao = Situacao.em_curso.value
        expected = [tuple((1, aluno_nome_1, cr, situacao))]
        controller = Controller(cria_aluno, cria_banco)
        controller.salva()
        actual = controller.pega_registros()
        assert actual == expected
