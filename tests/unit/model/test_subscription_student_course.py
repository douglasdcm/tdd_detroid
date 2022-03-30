from src.model.curso import Curso
from src.model.aluno import Aluno
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from pytest import raises
from src.exceptions.exceptions import InvalidStatus


class TestSubscriptionStudentCourse:
    def test_should_change_student_status_to_in_progress_when_subscribed(
        self, setup_available_course
    ):
        student = Aluno()
        expected = "in progress"
        InscricaoAlunoCurso().subscribe(student, setup_available_course)
        actual = student.get_status()
        assert actual == expected

    def test_should_add_students_to_course_list_when_subscribed(
        self, setup_available_course
    ):
        student_1 = Aluno()
        student_2 = Aluno()
        course = setup_available_course
        expected = [student_1, student_2]
        InscricaoAlunoCurso().subscribe(student_1, course)
        InscricaoAlunoCurso().subscribe(student_2, course)
        actual = course.get_students()
        assert actual == expected

    def test_should_add_student_to_course_list_when_subscribed(
        self, setup_available_course
    ):
        student = Aluno()
        course = setup_available_course
        expected = [student]
        InscricaoAlunoCurso().subscribe(student, course)
        actual = course.get_students()
        assert actual == expected

    def test_shouldnt_subscribe_student_when_student_status_not__unsuscribed__(
        self, setup_available_course
    ):
        student = Aluno().define_situacao("locked")
        subscription = InscricaoAlunoCurso()
        with raises(
            InvalidStatus,
            match="The student status must be 'unsubscribed' and the course status must be 'available' to subscribe.",
        ):
            subscription.subscribe(student, setup_available_course)

    def test_should_remove_student_when_unsubscribed(self, setup_available_course):
        student = Aluno()
        expected = student
        subscription = InscricaoAlunoCurso()
        subscription.subscribe(student, setup_available_course)
        subscription.unsubscribe(student, setup_available_course)
        actual = subscription.get_student()
        assert actual == expected

    def test_should_unsubcribe_student_from_course_when_available_course(
        self, setup_available_course
    ):
        expected = True
        student = Aluno()
        subscription = InscricaoAlunoCurso()
        subscription.subscribe(student, setup_available_course)
        actual = subscription.unsubscribe(student, setup_available_course)
        assert actual == expected

    def test_should_update_couser_when_subscribed(self, setup_available_course):
        course = setup_available_course
        expected = course
        subscription = InscricaoAlunoCurso()
        subscription.subscribe(Aluno(), setup_available_course)
        actual = subscription.get_course()
        assert actual == expected

    def test_should_update_student_when_subscribed(self, setup_available_course):
        student = Aluno()
        expected = student
        subscription = InscricaoAlunoCurso()
        subscription.subscribe(student, setup_available_course)
        actual = subscription.get_student()
        assert actual == expected

    def test_shouldnt_subscribe_student_to_course_when_pending_course(self):
        with raises(
            InvalidStatus,
            match="The student status must be 'unsubscribed' and the course status must be 'available' to subscribe.",
        ):
            InscricaoAlunoCurso().subscribe(Aluno(), Curso())

    def test_should_subcribe_student_to_course_when_available_course(
        self, setup_available_course
    ):
        expected = True
        actual = InscricaoAlunoCurso().subscribe(Aluno(), setup_available_course)
        assert actual == expected
