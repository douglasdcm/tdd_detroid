import pytest
from src.services.student_handler import (
    StudentHandler,
    NonValidStudent,
    NonValidSubject,
)
from src import mocks
from src import database as db


@pytest.fixture(autouse=True)
def restart_database():
    mocks.SUBJECT = "any"
    mocks.SUBJECT_MAX_ENROLL = 10
    mocks.COURSE = "any"


def test_unlock_course():
    database = db.Database()
    student = StudentHandler(database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    student.enroll_to_course("any")

    student.unlock_course()
    assert student.state == None


def test_lock_course():
    database = db.Database()
    student = StudentHandler(database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    student.enroll_to_course("any")

    assert student.lock_course() == "locked"
    assert database.student.state == "locked"


def test_take_subject_from_course_when_locked_student_return_error():
    database = db.Database()
    student = StudentHandler(database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    subject = "any"

    student.enroll_to_course("any")
    student.lock_course()
    with pytest.raises(NonValidStudent):
        student.take_subject(subject)


def test_take_full_subject_from_course_return_error():
    database = db.Database()
    student = StudentHandler(database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    subject = "ef15a071407953bd858cfca59ad99056"
    mocks.SUBJECT_MAX_ENROLL = -1

    student.enroll_to_course("any")
    with pytest.raises(NonValidSubject):
        student.take_subject(subject)


def test_take_invalid_subject_from_course_return_error():
    database = db.Database()
    student = StudentHandler(database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    subject = "invalid"
    mocks.SUBJECT = "invalid"
    mocks.COURSE = "other"

    student.enroll_to_course("any")
    with pytest.raises(NonValidSubject):
        student.take_subject(subject)


def test_take_subject_from_course():
    database = db.Database()
    student = StudentHandler(database)
    student.name = "any"
    student.cpf = "123.456.789-10"
    student.enroll_to_course("any")
    subject_identifier = "e4c858cd917f518194c9d93c9d13def8"

    student.enroll_to_course("any")
    student.take_subject(subject_identifier)
    assert subject_identifier in student.subjects


def test_enroll_invalid_student_to_course_retunr_error():
    database = db.Database()
    student = StudentHandler(database)
    student.name = "invalid"
    student.cpf = "123.456.789-10"

    with pytest.raises(NonValidStudent):
        student.enroll_to_course("any")


def test_enroll_student_to_course_x():
    database = db.Database()
    student = StudentHandler(database)
    student.name = "any"
    student.cpf = "123.456.789-10"

    assert student.enroll_to_course("any") is True
