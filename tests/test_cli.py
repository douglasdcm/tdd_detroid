from src import cli_helper
from src import database as db


def test_cancel_course_by_cli():
    name = "any"
    database = db.Database()
    assert cli_helper.cancel_course(database, name) == True


def test_deactivate_course_by_cli():
    name = "act"
    database = db.Database()
    assert cli_helper.deactivate_course(database, name) == True


def test_activate_course_cli():
    name = "deact"
    database = db.Database()
    assert cli_helper.activate_course(database, name) == True


def test_enroll_student_to_invalid_course():
    name = "any"
    cpf = "123.456.789-10"
    course_identifier = "invalid"
    database = db.Database()
    assert cli_helper.enroll_student(database, name, cpf, course_identifier) == False


def test_enroll_student_to_course_by_cli():
    name = "any"
    cpf = "123.456.789-10"
    course_identifier = "any"
    database = db.Database()
    assert cli_helper.enroll_student(database, name, cpf, course_identifier) == True
