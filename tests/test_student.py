import pytest
from src.services.student_handler import (
    StudentHandler,
    NonValidStudent,
    NonValidSubject,
    NonValidGrade,
)
from src import utils
from src.services.grade_calculator import GradeCalculator


@pytest.mark.parametrize(
    "grade, expected",
    [
        (6.99, "failed"),
        (7.01, "passed"),
    ],
)
def test_subject_situation_after_upgrade_grades(
    set_in_memory_database, grade, expected
):
    course_name = "any"
    subject_name = "any1"
    database = set_in_memory_database
    student_handler = StudentHandler(database)
    student_handler.name = "any"
    student_handler.cpf = "123.456.789-10"
    student_handler.enroll_to_course(course_name)
    student_handler.take_subject(subject_name)
    student_handler.update_grade_to_subject(grade=grade, subject_name=subject_name)

    # post condition
    grade_calculator = GradeCalculator(database)
    subject_identifier = utils.generate_subject_identifier(course_name, subject_name)
    grade_calculator.load_from_database(student_handler.identifier, subject_identifier)
    assert grade_calculator.student_identifier == student_handler.identifier
    assert grade_calculator.subject_identifier in student_handler.subjects
    assert grade_calculator.grade == grade
    assert grade_calculator.subject_situation == expected


@pytest.mark.parametrize(
    "grade",
    [
        (-1),
        (11),
    ],
)
def test_calculate_student_gpa_when_subjects_have_invalid_grades(
    set_in_memory_database, grade
):
    course_name = "any"
    database = set_in_memory_database
    student_handler = StudentHandler(database)
    student_handler.name = "any"
    student_handler.cpf = "123.456.789-10"
    student_handler.enroll_to_course(course_name)

    subject_name = "any1"

    student_handler.take_subject(subject_name)

    with pytest.raises(NonValidGrade):
        student_handler.update_grade_to_subject(grade=grade, subject_name=subject_name)


def test_unlock_course(set_in_memory_database):
    student = StudentHandler(set_in_memory_database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    student.enroll_to_course("any")

    student.unlock_course()
    assert student.state == "enrolled"


def test_lock_course(set_in_memory_database):
    database = set_in_memory_database
    student = StudentHandler(database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    student.enroll_to_course("any")

    assert student.lock_course() == "locked"
    assert database.student.state == "locked"


def test_take_subject_from_course_when_locked_student_return_error(
    set_in_memory_database,
):
    student = StudentHandler(set_in_memory_database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    subject = "any1"

    student.enroll_to_course("any")
    student.lock_course()
    with pytest.raises(NonValidStudent):
        student.take_subject(subject)


def test_take_full_subject_from_course_return_error(set_in_memory_database):
    student = StudentHandler(set_in_memory_database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    subject = utils.generate_subject_identifier("course1", "subject_full")

    student.enroll_to_course("any")
    with pytest.raises(NonValidSubject):
        student.take_subject(subject)


def test_take_invalid_subject_from_course_return_error(set_in_memory_database):
    student = StudentHandler(set_in_memory_database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    subject = "invalid"

    student.enroll_to_course("any")
    with pytest.raises(NonValidSubject):
        student.take_subject(subject)


def test_take_subject_from_course(set_in_memory_database):
    student = StudentHandler(set_in_memory_database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    course = "any"
    student.enroll_to_course(course)

    assert student.take_subject("any1") is True


def test_enroll_invalid_student_to_course_return_error(set_in_memory_database):
    student = StudentHandler(set_in_memory_database)
    student.name = "invalid"
    student.cpf = "123.456.789-10"

    with pytest.raises(NonValidStudent):
        student.enroll_to_course("any")


def test_enroll_student_to_course_x(set_in_memory_database):
    student = StudentHandler(set_in_memory_database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    course_name = "any"
    identifier = utils.generate_student_identifier(
        student.name, student.cpf, course_name
    )

    assert student.enroll_to_course(course_name) == identifier
