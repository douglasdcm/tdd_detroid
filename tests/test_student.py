import pytest
from src.services.student_handler import (
    StudentHandler,
    NonValidStudent,
    NonValidSubject,
)
from src.utils import generate_subject_identifier


def test_unlock_course(set_in_memory_database):
    student = StudentHandler(set_in_memory_database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    student.enroll_to_course("any")

    student.unlock_course()
    assert student.state == None


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
    subject = "any"

    student.enroll_to_course("any")
    student.lock_course()
    with pytest.raises(NonValidStudent):
        student.take_subject(subject)


def test_take_full_subject_from_course_return_error(set_in_memory_database):
    student = StudentHandler(set_in_memory_database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    subject = generate_subject_identifier("course1", "subject_full")

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
    student.enroll_to_course("any")
    subject_identifier = generate_subject_identifier(course, "any1")

    student.enroll_to_course(course)
    assert student.take_subject(subject_identifier) is True


def test_enroll_invalid_student_to_course_retunr_error(set_in_memory_database):
    student = StudentHandler(set_in_memory_database)
    student.name = "invalid"
    student.cpf = "123.456.789-10"

    with pytest.raises(NonValidStudent):
        student.enroll_to_course("any")


def test_enroll_student_to_course_x(set_in_memory_database):
    student = StudentHandler(set_in_memory_database)
    student.name = "any"
    student.cpf = "123.456.789-10"

    assert student.enroll_to_course("any") is True
