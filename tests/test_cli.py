from src import cli_helper
from src import mocks


def test_enroll_student_to_invalid_course():
    name = "any"
    cpf = "123.456.789-10"
    course_identifier = "invalid"
    database = mocks.Database()
    assert cli_helper.enroll_student(database, name, cpf, course_identifier) == False


def test_enroll_student_to_invalid_course():
    name = "any"
    cpf = "123.456.789-10"
    course_identifier = "invalid"
    database = mocks.Database()
    assert cli_helper.enroll_student(database, name, cpf, course_identifier) == False


def test_enroll_student_to_course():
    name = "any"
    cpf = "123.456.789-10"
    course_identifier = "any"
    database = mocks.Database()
    assert cli_helper.enroll_student(database, name, cpf, course_identifier) == True
