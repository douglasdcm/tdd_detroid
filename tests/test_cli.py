import pytest
from src import cli_helper
from src import utils


@pytest.mark.parametrize(
    "identifier,expected",
    [
        ("2024-1", True),
        ("invalid", False),
    ],
)
def test_close_semester_by_cli(set_in_memory_database, identifier, expected):
    assert cli_helper.close_semester(set_in_memory_database, identifier) == expected


@pytest.mark.parametrize(
    "course_name,subject_name,expected",
    [
        ("any", "any1", True),
        ("invalid", "any1", False),
        ("any", "invalid", False),
    ],
)
def test_remove_subject_by_cli(
    set_in_memory_database, course_name, subject_name, expected
):
    assert (
        cli_helper.remove_subject(set_in_memory_database, course_name, subject_name)
        == expected
    )


@pytest.mark.parametrize(
    "name,max_enrollment,expected",
    [
        ("new", 1, True),
        ("any", 1, False),  # duplicated
        ("new", -1, False),
    ],
)
def test_create_course_by_cli(set_in_memory_database, name, max_enrollment, expected):
    assert (
        cli_helper.create_course(set_in_memory_database, name, max_enrollment)
        == expected
    )


@pytest.mark.parametrize(
    "couse_name,subject_name,expected",
    [
        ("any", "new", True),
        ("any", "any1", False),  # duplicated
        ("invalid", "new", False),
    ],
)
def test_add_subject_to_course_by_cli(
    set_in_memory_database, couse_name, subject_name, expected
):
    assert (
        cli_helper.add_subject_to_course(
            set_in_memory_database, couse_name, subject_name
        )
        == expected
    )


@pytest.mark.parametrize(
    "name,cpf,course_name,expected",
    [
        ("any", "123.456.789-10", "any", True),
        ("invalid", "123.456.789-10", "any", False),
    ],
)
def test_calculate_student_gpa_by_cli(
    set_in_memory_database, name, cpf, course_name, expected
):
    database = set_in_memory_database
    student_identifier = utils.generate_student_identifier(name, cpf, course_name)
    cli_helper.enroll_student(database, name, cpf, course_name)

    assert cli_helper.calculate_student_gpa(database, student_identifier) == expected


def test_calculate_student_gpa_by_cli_when_student_is_valid_but_not_enrolled(
    set_in_memory_database,
):
    database = set_in_memory_database
    student_identifier = utils.generate_student_identifier(
        "any", "123.456.789-10", "any"
    )

    assert cli_helper.calculate_student_gpa(database, student_identifier) == False


@pytest.mark.parametrize(
    "name,cpf,course_name,subject_name,expected",
    [
        ("any", "123.456.789-10", "any", "any1", True),
        ("any", "123.456.789-10", "any", "invalid", False),
    ],
)
def test_take_subject_by_cli(
    set_in_memory_database, name, cpf, course_name, subject_name, expected
):
    database = set_in_memory_database
    student_identifier = utils.generate_student_identifier(name, cpf, course_name)
    cli_helper.enroll_student(database, name, cpf, course_name)

    assert (
        cli_helper.take_subject(database, student_identifier, subject_name) == expected
    )


def test_take_subject_by_cli_when_student_is_valid_but_not_enrolled(
    set_in_memory_database,
):
    database = set_in_memory_database
    student_identifier = utils.generate_student_identifier(
        "any", "123.456.789-10", "any"
    )

    assert cli_helper.take_subject(database, student_identifier, "any1") == False


@pytest.mark.parametrize(
    "course_name,expected",
    [
        ("any", True),
        ("invalid", False),
    ],
)
def test_list_student_details_by_cli(set_in_memory_database, course_name, expected):
    assert (
        cli_helper.list_student_details(set_in_memory_database, course_name) == expected
    )


def test_list_all_course_details_by_cli(set_in_memory_database):
    assert cli_helper.list_all_course_details(set_in_memory_database) is not False


@pytest.mark.parametrize(
    "name,expected",
    [
        ("act", True),
        ("invalid", False),
    ],
)
def test_cancel_course_by_cli(set_in_memory_database, name, expected):
    assert cli_helper.cancel_course(set_in_memory_database, name) == expected


@pytest.mark.parametrize(
    "name,expected",
    [
        ("act", True),
        ("invalid", False),
    ],
)
def test_deactivate_course_by_cli(set_in_memory_database, name, expected):
    assert cli_helper.deactivate_course(set_in_memory_database, name) == expected


@pytest.mark.parametrize(
    "name,expected",
    [
        ("deact", True),
        ("invalid", False),
    ],
)
def test_activate_course_cli(set_in_memory_database, name, expected):
    assert cli_helper.activate_course(set_in_memory_database, name) == expected


@pytest.mark.parametrize(
    "name,cpf,course_name, expected",
    [
        ("any", "123.456.789-10", "any", True),
        ("invalid", "123.456.789-10", "any", False),
        ("any", "invalid", "any", False),
        ("any", "123.456.789-10", "invalid", False),
    ],
)
def test_enroll_student_to_course_by_cli(
    set_in_memory_database, name, cpf, course_name, expected
):
    assert (
        cli_helper.enroll_student(set_in_memory_database, name, cpf, course_name)
        == expected
    )
