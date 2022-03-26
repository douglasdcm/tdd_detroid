from src.model.aluno import Aluno
from tests.helper import executa_comando
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.controller.controller import Controller


class TestCliInscreveAlunoCurso:
    def test_should_change_student_situation_to__in_progress_when_enrolment_successed(
        self, setup_database_in_real_db
    ):
        student_id = "3"
        course_id = "1"
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            student_id,
            "--curso-id",
            course_id,
        ]
        expected = "em curso"
        executa_comando(parametros)
        actual = (
            Controller(Aluno(), setup_database_in_real_db)
            .get_by_id(student_id)
            .pega_situacao()
        )
        assert actual == expected

    def test_should_return_exception_when_course_id_does_not_exist(
        self, setup_database_in_real_db
    ):
        controller = Controller(Aluno(), setup_database_in_real_db)
        controller.salva()
        student = controller.get_by_biggest_id()
        course_id = "73"
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            str(student.pega_id()),
            "--curso-id",
            course_id,
        ]
        expected = "Curso não encontrado."
        actual = executa_comando(parametros)
        assert expected in actual

    def test_should_retunr_exception_when_student_id_does_exist(self):
        student_id = "73"
        course_id = "1"
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            student_id,
            "--curso-id",
            course_id,
        ]
        expected = "Aluno não encontrado."
        actual = executa_comando(parametros)
        assert expected in actual

    def test_aluno_pode_ser_inscrito_curso(self, setup_database_in_real_db):
        student_id = "2"
        course_id = "1"
        expected = (
            f"Aluno identificado por {student_id} inscrito no curso"
            f" identificado por {course_id}."
        )
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            student_id,
            "--curso-id",
            course_id,
        ]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_should_enrol_student_to_course_by_cli_when_asked_for(
        self, setup_database_in_real_db
    ):
        id_ = "1"
        expected = 1
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            id_,
            "--curso-id",
            id_,
        ]
        executa_comando(parametros)
        actual = (
            Controller(InscricaoAlunoCurso(), setup_database_in_real_db)
            .get_by_biggest_id()
            .get_student_id()
        )
        assert actual == expected
