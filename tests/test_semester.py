import pytest
from src.services.semester_monitor import (
    SemesterMonitor,
    NonValidOperation,
)
from src.services.student_handler import StudentHandler


def test_calculate_gpa_of_all_enrolled_students_when_semester_closes(
    set_in_memory_database,
):
    student = "any"
    cpf = "123.456.789-10"
    course = "any"
    semester = "2024-1"
    database = set_in_memory_database
    student_handler = StudentHandler(database)
    student_handler.name = student
    student_handler.cpf = cpf
    student_handler.enroll_to_course(course)
    student_handler.take_subject("any1")
    student_handler.take_subject("any2")
    student_handler.take_subject("any3")
    student_handler.update_grade_to_subject(9, "any1")

    semester_monitor = SemesterMonitor(database, semester)
    semester_monitor.close()

    student_handler.load_from_database(student_handler.identifier)
    assert student_handler.gpa > 0
    assert student_handler.semester_counter > 0


def test_return_error_when_close_invalid_semester(set_in_memory_database):
    identifier = "3024-1"
    semester_monitor = SemesterMonitor(set_in_memory_database, identifier)
    with pytest.raises(NonValidOperation):
        semester_monitor.close()


def test_return_error_when_open_invalid_semester(set_in_memory_database):
    identifier = "3024-1"
    semester_monitor = SemesterMonitor(set_in_memory_database, identifier)
    with pytest.raises(NonValidOperation):
        semester_monitor.open()


def test_open_closed_semester_return_error(set_in_memory_database):
    identifier = "2024-1"
    semester_monitor = SemesterMonitor(set_in_memory_database, identifier)
    semester_monitor.close()
    with pytest.raises(NonValidOperation):
        semester_monitor.open()


def test_open_semester(set_in_memory_database):
    identifier = "2024-1"
    semester_monitor = SemesterMonitor(set_in_memory_database, identifier)
    assert semester_monitor.open() == "open"


def test_close_semester_when_no_students(set_in_memory_database):
    identifier = "2024-1"
    database = set_in_memory_database
    semester_monitor = SemesterMonitor(set_in_memory_database, identifier)

    assert semester_monitor.close() == "closed"

    # post conditions
    database.semester.load_by_identifier()

    assert identifier == database.semester.identifier
    assert semester_monitor.state == database.semester.state
