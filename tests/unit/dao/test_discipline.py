from pytest import fixture
from src.dao.discipline import DisciplineDao
from src.model import discipline
from src.model.discipline import Discipline
from sqlite3 import connect


class TestDisciplieDao:
    __connection = connect(":memory:")

    @fixture
    def setup(self, setup_database_in_memory):
        dao = DisciplineDao(self.__connection)
        dao.create(Discipline())
        yield dao

    @fixture
    def setup_two_disciplines(self, setup_database_in_memory):
        name_1 = "test_1"
        name_2 = "test_2"
        discipline_1 = Discipline()
        discipline_2 = Discipline()
        dao = DisciplineDao(self.__connection)
        dao.create(discipline_1)
        dao.create(discipline_2)
        discipline_1 = dao.read(id_=1)
        discipline_2 = dao.read(id_=2)
        discipline_1.set_name(name_1)
        discipline_2.set_name(name_2)
        yield discipline_1, discipline_2

    def test_should_discipline_have_unique_id_when_created_with_same_name(
        self, setup_database_in_memory, setup_two_disciplines
    ):
        discipline_1, discipline_2 = setup_two_disciplines
        id_1 = discipline_1.get_id()
        id_2 = discipline_2.get_id()
        assert id_1 != id_2

    def test_should_read_latest_discipline_grade_when_created(self, setup):
        grade = 9
        expected = grade
        discipline = Discipline()
        discipline.set_grade(grade)
        dao = DisciplineDao(self.__connection)
        dao.create(discipline)
        dao.create(discipline)
        discipline = dao.read(id_=3)
        actual = discipline.get_grade()
        assert actual == expected

    def test_should_grade_be_updated_when_specified(self, setup_database_in_memory):
        grade = 4
        expected = grade
        discipline = Discipline()
        discipline.set_grade(grade)
        dao = DisciplineDao(self.__connection)
        dao.create(discipline)
        discipline = dao.read(id_=1)
        actual = discipline.get_grade()
        assert actual == expected

    def test_should_grade_be_zero_when_not_specified(self, setup):
        grade = 0
        expected = grade
        dao = setup
        discipline = dao.read(id_=1)
        actual = discipline.get_grade()
        assert actual == expected

    def test_should_get_disciplines_from_database_when_asked_for(self, setup):
        id_ = 2
        dao = setup
        dao.create(Discipline())
        actual = dao.read(id_)
        assert isinstance(actual, Discipline)

    def test_should_update_discipline_in_database_when_asked_for(self, setup):
        id_ = 1
        dao = setup
        assert dao.update(Discipline(), id_)

    def test_should_read_discipline_from_database_when_asked_for(self, setup):
        id_ = 1
        dao = setup
        actual = dao.read(id_)
        assert isinstance(actual, Discipline)

    def test_should_create_the_discipline_in_database_when_asked_for(
        self, setup_database_in_memory
    ):
        assert DisciplineDao(self.__connection).create(Discipline())
