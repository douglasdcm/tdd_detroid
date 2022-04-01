from src.model.student import Student
from src.model.discipline import Discipline


class TestStudent:
    def test_should_score_of_student_be_main_of_grades_when_many_disciplines(self):
        grade_1 = 7
        grade_2 = 3
        discipline_1 = Discipline()
        discipline_2 = Discipline()
        discipline_1.set_id(id_=1)
        discipline_2.set_id(id_=2)
        discipline_1.set_grade(grade_1)
        discipline_2.set_grade(grade_2)
        student = Student()
        student.update_discipline(discipline_1)
        student.update_discipline(discipline_2)
        expected = 5
        actual = student.get_score()
        assert actual == expected

    def test_should_score_be_grade_when_one_discipline(self):
        grade = 9
        discipline = Discipline()
        discipline.set_grade(grade)
        student = Student()
        student.update_discipline(discipline)
        expected = grade
        actual = student.get_score()
        assert actual == expected

    def test_should_student_has_score_when_it_exists(self):
        assert Student().set_score(7)
