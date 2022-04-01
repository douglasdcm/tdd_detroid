from pytest import fixture
from src.dao.student import StudentDao
from src.model.discipline import Discipline
from src.model.student import Student
from sqlite3 import connect
from src.dao.discipline import DisciplineDao


class TestStudentDao:

    connection = connect(":memory:")

    @fixture
    def setup(self, setup_database_in_memory):
        score = 5
        dao = StudentDao(self.connection)
        student = Student()
        student.set_score(score)
        dao.create(student)
        yield dao

    @fixture
    def setup_disciplines_grade_eight(self, setup_database_in_memory):
        yield self.__create_disciplines(8, 7, 7)

    @fixture
    def setup_disciplines_grade_five(self, setup_database_in_memory):
        yield self.__create_disciplines(7, 7, 1)

    def __create_disciplines(self, grade_1, grade_2, grade_3):
        discipline_1 = Discipline()
        discipline_2 = Discipline()
        discipline_3 = Discipline()
        discipline_1.set_grade(grade_1)
        discipline_2.set_grade(grade_2)
        discipline_3.set_grade(grade_3)

        dao_discipline = DisciplineDao(self.connection)
        dao_discipline.create(discipline_1)
        dao_discipline.create(discipline_2)
        dao_discipline.create(discipline_3)

        discipline_1 = dao_discipline.read(id_=1)
        discipline_2 = dao_discipline.read(id_=2)
        discipline_3 = dao_discipline.read(id_=3)
        return discipline_1, discipline_2, discipline_3

    def test_shouldnt_increase_score_when_discipline_grade_updated_to_down(
        self, setup_disciplines_grade_five
    ):
        expected = 5
        discipline_1, discipline_2, discipline_3 = setup_disciplines_grade_five
        student = Student()
        student.update_discipline(discipline_1)
        student.update_discipline(discipline_2)
        student.update_discipline(discipline_3)

        discipline_3.set_grade(grade=0)

        dao_discipline = DisciplineDao(self.connection)
        dao_discipline.update(discipline_3, id_=3)

        discipline_3 = dao_discipline.read(id_=3)

        student.update_discipline(discipline_3)

        actual = student.get_score()
        assert actual == expected

    def test_should_increase_score_when_discipline_grade_updated_to_up(
        self, setup_disciplines_grade_five
    ):
        expected = 7
        discipline_1, discipline_2, discipline_3 = setup_disciplines_grade_five
        student = Student()
        student.update_discipline(discipline_1)
        student.update_discipline(discipline_2)
        student.update_discipline(discipline_3)

        discipline_3.set_grade(grade=7)

        dao_discipline = DisciplineDao(self.connection)
        dao_discipline.update(discipline_3, id_=3)

        discipline_3 = dao_discipline.read(id_=3)

        student.update_discipline(discipline_3)

        actual = student.get_score()
        assert actual == expected

    def test_shouldnt_status_be_approved_when_score_not_bigger_or_equal_seven(
        self, setup_disciplines_grade_five
    ):
        expected = "undefined"
        discipline_1, discipline_2, discipline_3 = setup_disciplines_grade_five
        student = Student()
        student.update_discipline(discipline_1)
        student.update_discipline(discipline_2)
        student.update_discipline(discipline_3)
        actual = student.get_status()
        assert actual == expected

    def test_should_status_be_approved_when_score_bigger_or_equal_seven(
        self, setup_disciplines_grade_eight
    ):
        expected = "approved"
        discipline_1, discipline_2, discipline_3 = setup_disciplines_grade_eight
        student = Student()
        student.update_discipline(discipline_1)
        student.update_discipline(discipline_2)
        student.update_discipline(discipline_3)
        actual = student.get_status()
        assert actual == expected

    def test_should_update_score_when_grade_in_disciplines(
        self, setup, setup_disciplines_grade_five
    ):
        id_ = 1
        expected = 5

        discipline_1, discipline_2, discipline_3 = setup_disciplines_grade_five
        student = Student()
        student.update_discipline(discipline_1)
        student.update_discipline(discipline_2)
        student.update_discipline(discipline_3)

        dao = setup
        dao.create(student)
        student = dao.read(id_)

        actual = student.get_score()
        assert actual == expected

    def test_should_update_score_in_database_when_asked_for(self, setup):
        score_1 = 5
        score_2 = 8
        id_ = 1
        expected = score_2
        student = Student()
        student.set_score(score_1)
        dao = setup
        dao.create(student)
        student.set_score(score_2)
        dao.update(student, id_)
        student = dao.read(id_)
        actual = student.get_score()
        assert actual == expected

    def test_should_get_score_from_database_when_asked_for(self, setup):
        score = 5
        id_ = 1
        expected = score
        student = Student()
        student.set_score(score)
        dao = setup
        dao.create(student)
        student = dao.read(id_)
        actual = student.get_score()
        assert actual == expected

    def test_should_get_student_from_database_when_asked_for(self, setup):
        dao = setup
        assert isinstance(dao.read(id_=1), Student)

    def test_should_save_student_to_database_when_asked_for(
        self, setup_database_in_memory
    ):
        assert StudentDao(self.connection).create(Student())
