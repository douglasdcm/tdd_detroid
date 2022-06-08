from src.student import Student
from src.discipline import Discipline
from src.persister import Persister
from pytest import fixture


class TestDisciplinePersistence:

    @fixture
    def setup(self):
        persister = Persister()
        persister.save_discipline(1000, Discipline())
        persister.save_discipline(1000, Discipline())
        persister.save_discipline(1000, Discipline())
        persister.save_discipline(1000, Discipline())
        persister.save_discipline(1000, Discipline())

        yield persister

    def test_save_enrollment_when_many_students(self, setup):
        id_ = 2
        persister = setup
        discipline = persister.get_discipline(id_)
        discipline.set_enrollment(Student())
        discipline.set_enrollment(Student())
        discipline.set_enrollment(Student())
        persister.save_discipline(id_, discipline)

        actual = len(discipline.get_enrollments())

        assert actual == 3

    def test_save_enrollment(self, setup):
        student = Student()
        id_ = 1
        persister = setup
        discipline = persister.get_discipline(id_)
        discipline.set_enrollment(student)
        persister.save_discipline(id_, discipline)
        discipline_updated = persister.get_discipline(id_)

        actual = discipline_updated.get_enrollments()[0]

        assert actual == student

    def test_save_discipline(self):
        id_ = 0
        discipline = Discipline()
        persister = Persister()
        persister.save_discipline(1000, discipline)

        actual = persister.get_discipline(id_)

        assert actual == discipline
