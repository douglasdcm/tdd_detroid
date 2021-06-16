from src.model.curso import Curso
from src.controller.controller import Controller
from src.model.banco_dados import BancoDados
from tests.massa_dados import curso_nome_1, materia_nome_1, aluno_nome_1

class TestControllerCurso:

    def test_curso_criado_banco_dados(self, cria_banco):
        curso_id = 1
        expected = [tuple((1, curso_nome_1))]
        controller = Controller(Curso(curso_nome_1), cria_banco)
        controller.salva()
        actual = controller.pega_registro_por_id(curso_id)
        assert actual == expected
