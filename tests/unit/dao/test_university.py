from pytest import fixture
from src.dao.university import UniversityDao
from sqlite3 import connect


class TestUniversityDao:
    @fixture
    def setup(self, setup_valid_univertity, setup_database_in_memory):
        id_ = 1
        university = setup_valid_univertity
        dao = UniversityDao(connect(":memory:"))
        dao.create(university)
        yield dao.read(id_)

    def test_should_create_university_with_courses_when_has_valid_courses(self, setup):
        expected = 3
        university = setup
        actual = len(university.get_courses())
        assert actual == expected

    def test_should_create_university_with_status_open_when_has_valid_courses(
        self, setup_valid_univertity, setup_database_in_memory
    ):
        id_ = 1
        expected = "open"
        university = setup_valid_univertity
        dao = UniversityDao(connect(":memory:"))
        dao.create(university)
        university = dao.read(id_)
        actual = university.get_status()
        assert actual == expected
