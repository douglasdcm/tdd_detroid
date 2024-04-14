import pytest
from src.services.semester_monitor import (
    SemesterMonitor,
    NonValidOperation,
)


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


def test_close_semester(set_in_memory_database):
    identifier = "2024-1"
    semester_monitor = SemesterMonitor(set_in_memory_database, identifier)

    assert semester_monitor.close() == "closed"
