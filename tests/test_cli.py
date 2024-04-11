from src import cli_helper
from src import mocks


def test_cancel_course_by_cli():
    name = "any"
    database = mocks.Database()
    assert cli_helper.cancel_course(database, name) == True


def test_deactivate_course_by_cli():
    name = "act"
    database = mocks.Database()
    assert cli_helper.deactivate_course(database, name) == True


def test_activate_course_cli():
    name = "deact"
    database = mocks.Database()
    assert cli_helper.activate_course(database, name) == True


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
