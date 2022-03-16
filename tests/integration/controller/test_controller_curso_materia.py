from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from typing import Match
from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.curso import Curso
from src.model.banco_dados import BancoDados
from src.controller.controller import Controller
from src.model.banco_dados import BancoDados
from src.model.materia import Materia
from tests.massa_dados import curso_nome_1, materia_nome_1, materia_nome_2, materia_nome_3


class TestControllerCursoMateria:

    def test_curso_associado_materia_criado_banco_dados(self, cria_banco):
        associacao_id = 1
        curso_id = 1
        materia_1_id = 1
        materia_2_id = 2
        materia_3_id = 3
        curso = Curso(curso_nome_1).define_id(curso_id)
        materia_1 = Materia(materia_nome_1)
        materia_1.define_id(materia_1_id)
        materia_2 = Materia(materia_nome_2)
        materia_2.define_id(materia_2_id)
        materia_3 = Materia(materia_nome_3)
        materia_3.define_id(materia_3_id)
        expected = [tuple((associacao_id, curso_id, materia_1_id))]
        Controller(curso, cria_banco).salva()
        Controller(materia_1, cria_banco).salva()
        Controller(materia_2, cria_banco).salva()
        Controller(materia_3, cria_banco).salva()   
        controller = Controller(AssociaCursoMateria(curso, materia_1), cria_banco)
        controller.salva()
        controller = Controller(AssociaCursoMateria(curso, materia_2), cria_banco)
        controller.salva()
        controller = Controller(AssociaCursoMateria(curso, materia_3), cria_banco)
        controller.salva()
        actual = controller.pega_registro_por_id(associacao_id)
        assert actual == expected
