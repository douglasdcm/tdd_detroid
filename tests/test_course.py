import pytest
from src.services.course_handler import CourseHandler, NonValidCourse


def test_enroll_student_to_inactive_course_return_error(set_in_memory_database):
    course_handler = CourseHandler(set_in_memory_database)
    course_handler.name = "adm"
    course_handler.add_subject("any1")
    course_handler.add_subject("any2")
    course_handler.add_subject("any3")
    course_handler.deactivate()

    with pytest.raises(NonValidCourse):
        course_handler.enroll_student("any")


def test_enroll_student_to_active_course(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.name = "adm"
    course_handler.add_subject("any1")
    course_handler.add_subject("any2")
    course_handler.add_subject("any3")
    course_handler.activate()

    assert course_handler.enroll_student("any") == True

    assert database.course.enrolled_students == "any"


def test_cancel_inactive_course(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.name = "adm"
    course_handler.add_subject("any1")
    course_handler.add_subject("any2")
    course_handler.add_subject("any3")
    course_handler.deactivate()
    assert course_handler.cancel() == "cancelled"

    assert database.course.state == "cancelled"


def test_cancel_active_course(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.name = "adm"
    course_handler.add_subject("any1")
    course_handler.add_subject("any2")
    course_handler.add_subject("any3")
    course_handler.activate()
    assert course_handler.cancel() == "cancelled"

    assert database.course.state == "cancelled"


def test_deactivate_non_active_course_return_error(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    with pytest.raises(NonValidCourse):
        course_handler.deactivate()

    assert database.course.state != "inactive"


def test_deactivate_course(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.name = "adm"
    course_handler.add_subject("any1")
    course_handler.add_subject("any2")
    course_handler.add_subject("any3")
    course_handler.activate()
    assert course_handler.deactivate() == "inactive"

    assert database.course.state == "inactive"


def test_activate_course_without_minimum_subjects_return_error(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.name = "any"
    with pytest.raises(NonValidCourse):
        course_handler.activate()
    assert database.course.state != "active"


def test_activate_course_without_name_return_error(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    with pytest.raises(NonValidCourse):
        course_handler.activate()
    assert database.course.state != "active"


def test_activate_course(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.name = "adm"
    course_handler.add_subject("any1")
    course_handler.add_subject("any2")
    course_handler.add_subject("any3")
    assert course_handler.activate() == "active"

    assert database.course.state == "active"
