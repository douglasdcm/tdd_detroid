from src.model.coordenador_geral import CoordenadorGeral
from src.model.curso import Curso
from src.dao.dao_coordenador_geral import DaoCoordenadorGeral
from src.model.banco_dados import BancoDados
from src.dao.dao_curso import DaoCurso


class TestDaoCoordenadorGeral:
    def test_should_list_student_details_when_one_students_in_course(
        self, setup_database_in_memory
    ):
        id_ = 1
        connection = BancoDados(setup_database_in_memory)
        expected = {
            "alunos": [
                {
                    "nome": "student_name_1",
                    "materias": [],
                    "coeficiente rendimento": 3,
                    "curso": "course_1",
                }
            ]
        }
        coord_obj = DaoCoordenadorGeral(CoordenadorGeral(), connection).get_by_id(id_)
        actual = coord_obj.listar_detalhe_alunos(
            DaoCurso(Curso(), connection).get_by_id(id_)
        )
        assert actual == expected

    def test_shouldnt_list_student_details_when_no_students_in_course(
        self, setup_database_in_memory
    ):
        expected = {"alunos": []}
        obj = DaoCoordenadorGeral(
            CoordenadorGeral(), BancoDados(setup_database_in_memory)
        ).get_by_id(1)
        actual = obj.listar_detalhe_alunos(Curso())
        assert actual == expected
