from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from typing import Match
from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.curso import Curso
from src.model.banco_dados import BancoDados
from src.controller.controller import Controller
from src.model.banco_dados import BancoDados
from src.model.materia import Materia
from tests.massa_dados import (
    curso_nome_1,
    materia_nome_1,
    materia_nome_2,
    materia_nome_3,
)


class TestControllerCursoMateria:
    def test_curso_associado_materia_criado_banco_dados(self, setup_database_in_memory):
        curso_id = 2
        expected = curso_id
        for id_ in [1, 2, 3]:
            Controller(
                AssociaCursoMateria(
                    Curso().define_id(curso_id), Materia().define_id(id_)
                ),
                setup_database_in_memory,
            ).salva()
        actual = (
            Controller(
                AssociaCursoMateria(Curso(), Materia()),
                setup_database_in_memory,
            )
            .get_by_biggest_id()
            .get_course_id()
        )
        assert actual == expected
