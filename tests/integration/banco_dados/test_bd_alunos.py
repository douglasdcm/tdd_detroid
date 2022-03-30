from src.controller.controller import Controller
from src.model.aluno import Aluno


class TestBdAlunos:
    def test_should_create_student_in_database_when_asked_for(
        self, setup_database_in_memory
    ):
        id_ = 1
        expected = "student_name_1"
        actual = (
            Controller(Aluno(), setup_database_in_memory).get_by_id(id_).pega_nome()
        )
        assert actual == expected
