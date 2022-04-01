from pytest import fixture
from src.model.discipline import Discipline
from src.model.course import Course
from src.model.university import University


class TestCourse:
    @fixture
    def setup_big_valid_univertity(self):
        quantity_courses = quantity_disciplines = 10
        university = University()
        for i in range(quantity_courses):
            course = Course()
            for j in range(quantity_disciplines):
                course.add_discipline(Discipline())
            university.add_course(course)
        university.create()
        yield university

    @fixture
    def setup_invalid_univertity(self):
        quantity_courses = 2
        quantity_disciplines = 3
        university = University()
        for i in range(quantity_courses):
            course = Course()
            for j in range(quantity_disciplines):
                course.add_discipline(Discipline())
            university.add_course(course)
        university.create()
        yield university

    def test_should_university_status_be_open_when_has_many_valid_courses(
        self, setup_big_valid_univertity
    ):
        university = setup_big_valid_univertity
        actual = university.get_status()
        expected = "open"
        assert actual == expected

    def test_should_university_status_be_open_when_created(
        self, setup_valid_univertity
    ):
        university = setup_valid_univertity
        actual = university.get_status()
        expected = "open"
        assert actual == expected

    def test_should_university_status_be_pending_when_not_created(
        self, setup_invalid_univertity
    ):
        university = setup_invalid_univertity
        actual = university.get_status()
        expected = "pending"
        assert actual == expected

    def test_should_courses_have_3_disciplines_each_when_university_created(
        self, setup_valid_univertity
    ):
        university = setup_valid_univertity
        actual = len(university.get_courses())
        expected = 3
        assert actual == expected

    def test_shouldnt_create_university_when_bot_enough_courses(
        self, setup_invalid_univertity
    ):
        university = setup_invalid_univertity
        actual = len(university.get_courses())
        expected = 0
        assert actual == expected

    def test_shouldnt_create_university_when_courses_without_enough_discipiles(
        self,
    ):
        university = University()
        university.add_course(Course())
        university.add_course(Course())
        university.add_course(Course())
        university.create()
        actual = len(university.get_courses())
        expected = 0
        assert actual == expected
