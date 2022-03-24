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
    def test_popula_banco(self, _setup_objetos):
        expected = {
            "alunos": [
                {
                    "nome": "aluno_nome_1",
                    "coeficiente rendimento": 0,
                    "materias": {},
                    "curso": "curso_novo",
                }
            ]
        }
        coordenador_geral = _setup_objetos
        actual = coordenador_geral.listar_detalhe_alunos()
        assert actual == expected

    @fixture
    def _setup_objetos(self, setup_database_in_memory):
        CatalogoCurso().limpa_catalogo()
        controller_aluno = Controller(Aluno("aluno_nome_1"), setup_database_in_memory)
        controller_aluno.salva()
        aluno_obj = controller_aluno.pega_registro_por_id(id_=1)
        controller_curso = Controller(Curso("curso_novo"), setup_database_in_memory)
        controller_curso.salva()
        curso_obj = controller_curso.pega_registro_por_id(id_=1)
        controller_materia = Controller(
            Materia(materia_nome_1), setup_database_in_memory
        )
        controller_materia.salva()
        materia_1_obj = controller_materia.pega_registro_por_id(id_=1)
        controller_materia = Controller(
            Materia(materia_nome_2), setup_database_in_memory
        )
        controller_materia.salva()
        materia_2_obj = controller_materia.pega_registro_por_id(id_=2)
        controller_materia = Controller(
            Materia(materia_nome_3), setup_database_in_memory
        )
        controller_materia.salva()
        materia_3_obj = controller_materia.pega_registro_por_id(id_=3)
        Controller(
            AssociaCursoMateria(curso_obj, materia_1_obj), setup_database_in_memory
        ).salva()
        Controller(
            AssociaCursoMateria(curso_obj, materia_2_obj), setup_database_in_memory
        ).salva()
        Controller(
            AssociaCursoMateria(curso_obj, materia_3_obj), setup_database_in_memory
        ).salva()
        Controller(
            InscricaoAlunoCurso(aluno_obj, curso_obj), setup_database_in_memory
        ).salva()
        controller_coordenador_geral = Controller(
            CoordenadorGeral(), setup_database_in_memory
        )
        controller_coordenador_geral.salva()
        coordenador_geral = controller_coordenador_geral.pega_registro_por_id(id_=1)
        yield coordenador_geral
