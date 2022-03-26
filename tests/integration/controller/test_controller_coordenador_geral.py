from src.model.materia import Materia
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.controller.controller import Controller
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.coordenador_geral import CoordenadorGeral
from tests.massa_dados import (
    aluno_nome_1,
    curso_nome_1,
    materia_nome_1,
    materia_nome_2,
    materia_nome_3,
)
from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.catalogo_curso import CatalogoCurso
from pytest import fixture


class TestControllerCoordenadorGeral:
    def test_popula_banco(self, setup_database_in_memory):
        CatalogoCurso().limpa_catalogo()
        controller_coordenador_geral = Controller(
            CoordenadorGeral(), setup_database_in_memory
        )
        controller_coordenador_geral.salva()
        coordenador_geral = controller_coordenador_geral.pega_registro_por_id(id_=1)

        expected = {
            "alunos": [
                {
                    "nome": "student_name_1",
                    "coeficiente rendimento": 0,
                    "materias": {},
                    "curso": "course_1",
                },
                {
                    "nome": "student_name_2",
                    "coeficiente rendimento": 0,
                    "materias": {},
                    "curso": "course_1",
                },
                {
                    "nome": "student_name_3",
                    "coeficiente rendimento": 0,
                    "materias": {},
                    "curso": "course_1",
                },
                {
                    "nome": "student_name_4",
                    "coeficiente rendimento": 0,
                    "materias": {},
                    "curso": "course_1",
                },
                {
                    "nome": "student_name_5",
                    "coeficiente rendimento": 0,
                    "materias": {},
                    "curso": "course_1",
                },
            ]
        }
        actual = coordenador_geral.listar_detalhe_alunos()
        assert actual == expected
