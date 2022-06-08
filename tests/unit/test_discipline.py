from src.student import Student
from src.discipline import Discipline


class TestDiscipline:

    def test_has_student_enrolled(self):
        student = Student()
        discipline = Discipline()
        discipline.set_enrollment(student)

        actual = discipline.get_enrollments()[0]

        assert actual == student
