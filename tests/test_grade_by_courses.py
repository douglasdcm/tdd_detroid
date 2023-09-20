from src.student import Student


def test_grade_student_with_average_of_course_grades():
    student = Student()
    student.grade_course(8)
    student.grade_course(2)
    assert student.get_grade() == 5


def test_no_grade_student_by_when_0_course():
    student = Student()
    assert student.get_grade() == 0
