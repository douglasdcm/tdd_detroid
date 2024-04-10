import pytest
from src.services.student_handler import (
    StudentHandler,
    NonValidStudent,
    NonValidSubject,
)
from src import mock_database


@pytest.fixture(autouse=True)
def restart_database():
    mock_database.SUBJECT = "any"
    mock_database.SUBJECT_MAX_ENROLL = 10


# def test_lock_course():
#     student = Student()
#     student.name = "any"
#     student.cpf = "123.456.789-10"
#     subject = "any"

#     student.enroll_to_course("any")
#     student.take_subject(subject)
#     assert subject in student.subjects


def test_take_full_subject_from_course_return_error():
    student = StudentHandler()
    student.name = "any"
    student.cpf = "123.456.789-10"
    subject = "invalid"
    mock_database.SUBJECT = "invalid"
    mock_database.SUBJECT_MAX_ENROLL = -1

    student.enroll_to_course("any")
    with pytest.raises(NonValidSubject):
        student.take_subject(subject)


def test_take_invalid_subject_from_course_return_error():
    student = StudentHandler()
    student.name = "any"
    student.cpf = "123.456.789-10"
    subject = "invalid"
    mock_database.SUBJECT = "invalid"

    student.enroll_to_course("any")
    with pytest.raises(NonValidSubject):
        student.take_subject(subject)


def test_take_subject_from_course():
    student = StudentHandler()
    student.name = "any"
    student.cpf = "123.456.789-10"
    subject = "any"

    student.enroll_to_course("any")
    student.take_subject(subject)
    assert subject in student.subjects


def test_enroll_invalid_student_to_course_retunr_error():
    student = StudentHandler()
    student.name = "invalid"
    student.cpf = "123.456.789-10"

    with pytest.raises(NonValidStudent):
        student.enroll_to_course("any")


def test_enroll_student_to_course():
    student = StudentHandler()
    student.name = "any"
    student.cpf = "123.456.789-10"

    student.enroll_to_course("any")

    # generate using student name, cpf and course
    assert student.identifier == "290f2113c2e6579c8bb6ec395ea56572"
