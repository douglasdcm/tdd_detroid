from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from typing import Match
from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.curso import Curso
from src.model.banco_dados import BancoDados
from src.controller.controller import Controller
from src.model.banco_dados import BancoDados
from src.model.materia import Materia
from src.model.aluno import Aluno
from tests.massa_dados import curso_nome_1, materia_nome_1, aluno_nome_1

class TestControllerCursoMateria:

    def test_curso_associado_materia_criado_banco_dados(self, cria_banco):
        associacao_id = 1
        curso_id = 1
        materia_id = 1
        expected = [tuple((associacao_id, curso_id, materia_id))]
        Controller(Curso(curso_nome_1), cria_banco).salva()
        Controller(Materia(materia_nome_1), cria_banco).salva()
        controller = Controller(AssociaCursoMateria(curso_id, materia_id), cria_banco)
        controller.salva()
        actual = controller.pega_registro_por_id(associacao_id)
        assert actual == expected
