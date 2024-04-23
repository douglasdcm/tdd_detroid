import pytest
from src.services.grade_calculator import GradeCalculator
from src.services.student_handler import StudentHandler


@pytest.mark.parametrize(
    "grade1,grade2,grade3,expected",
    [
        (7, 7, 7, 7),
        (5, 5, 5, 5),
        (5.1, 5.1, 5.1, 5.1),
    ],
)
def test_calculate_student_gpa_when_subjects_have_grades(
    set_in_memory_database, grade1, grade2, grade3, expected
):
    course_name = "any"
    database = set_in_memory_database
    grade_calculator = GradeCalculator(database)
    student_handler = StudentHandler(database)
    student_handler.name = "any"
    student_handler.cpf = "123.456.789-10"
    student_handler.enroll_to_course(course_name)

    subject_name1 = "any1"
    subject_name2 = "any2"
    subject_name3 = "any3"

    student_handler.take_subject("any1")
    student_handler.take_subject("any2")
    student_handler.take_subject("any3")

    student_handler.update_grade_to_subject(grade=grade1, subject_name=subject_name1)
    student_handler.update_grade_to_subject(grade=grade2, subject_name=subject_name2)
    student_handler.update_grade_to_subject(grade=grade3, subject_name=subject_name3)

    assert (
        grade_calculator.calculate_gpa_for_student(student_handler.identifier)
        == expected
    )


def test_calculate_student_gpa_when_no_grades(set_in_memory_database):
    course_name = "any"
    database = set_in_memory_database
    grade_calculator = GradeCalculator(database)
    student_handler = StudentHandler(database)
    student_handler.name = "any"
    student_handler.cpf = "123.456.789-10"
    student_handler.enroll_to_course(course_name)

    student_handler.take_subject("any1")
    student_handler.take_subject("any2")
    assert grade_calculator.calculate_gpa_for_student(student_handler.identifier) == 0