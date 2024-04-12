from src import cli_helper


def test_cancel_course_by_cli(set_in_memory_database):
    name = "any"
    assert cli_helper.cancel_course(set_in_memory_database, name) == True


def test_deactivate_course_by_cli(set_in_memory_database):
    name = "act"
    assert cli_helper.deactivate_course(set_in_memory_database, name) == True


def test_activate_course_cli(set_in_memory_database):
    name = "deact"
    assert cli_helper.activate_course(set_in_memory_database, name) == True


def test_enroll_student_to_invalid_course(set_in_memory_database):
    name = "any"
    cpf = "123.456.789-10"
    course_identifier = "invalid"
    assert (
        cli_helper.enroll_student(set_in_memory_database, name, cpf, course_identifier)
        == False
    )


def test_enroll_student_to_course_by_cli(set_in_memory_database):
    name = "any"
    cpf = "123.456.789-10"
    course_identifier = "any"
    assert (
        cli_helper.enroll_student(set_in_memory_database, name, cpf, course_identifier)
        == True
    )
