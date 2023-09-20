# feature: 1. Each student will have a grade control called "grade point average" (GPA).
from src.student import Student
from src.processor import grade_students_in_parallel


def test_grade_in_parallel():
    gpa_1 = 3
    gpa_2 = 6
    gpa_3 = 9
    student_1 = Student()
    student_2 = Student()
    student_3 = Student()
    students = []
    students = [student_1, student_2, student_3]
    grades = [gpa_1, gpa_2, gpa_3]

    assert grade_students_in_parallel(
        students,
        grades,
    )
    assert student_1.get_grade() == gpa_1
    assert student_2.get_grade() == gpa_2
    assert student_3.get_grade() == gpa_3


def test_grade_controll_for_each_student():
    gpa_1 = 3
    gpa_2 = 6
    gpa_3 = 9
    student_1 = Student()
    student_2 = Student()
    student_3 = Student()
    student_1.grade_course(gpa_1)
    student_2.grade_course(gpa_2)
    student_3.grade_course(gpa_3)
    assert student_1.get_grade() == gpa_1
    assert student_2.get_grade() == gpa_2
    assert student_3.get_grade() == gpa_3
