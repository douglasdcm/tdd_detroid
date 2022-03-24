from src.model.curso import Curso
from src.controller.controller import Controller
from src.model.banco_dados import BancoDados
from tests.massa_dados import curso_nome_1, materia_nome_1, aluno_nome_1


class TestControllerCurso:
    def test_curso_criado_banco_dados(self, setup_database_in_memory):
        curso_id = 1
        expected = Curso(curso_nome_1).pega_nome()
        controller = Controller(Curso(curso_nome_1), setup_database_in_memory)
        controller.salva()
        curso = controller.pega_registro_por_id(curso_id)
        actual = curso.pega_nome()
        assert actual == expected
