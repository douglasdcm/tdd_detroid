import pytest
from src.services.course_handler import (
    CourseHandler,
    NonValidCourse,
    NonMinimunSubjects,
)
from src.services.student_handler import StudentHandler
from src import utils


def test_add_subject_to_new_course(set_in_memory_database):
    course = "newcourse"
    max_enrollment = 9
    subject = "newsubject"
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.create(course, max_enrollment)
    assert course_handler.add_subject(subject) is True

    # post conditions
    course_handler.load_from_database(course)
    assert (
        utils.generate_subject_identifier(course, subject) in database.course.subjects
    )
    assert database.course.max_enrollment == max_enrollment


def test_create_courses_without_subjects(set_in_memory_database):
    name = "newcourse"
    max_enrollment = 9
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    assert course_handler.create(name, max_enrollment) is True

    # post conditions
    course_handler.load_from_database(name)
    assert database.course.name == name
    assert database.course.max_enrollment == max_enrollment


def test_list_all_courses(set_in_memory_database):
    name = "any"
    cpf = "123.456.789-10"
    course = "any"
    student_handler = StudentHandler(set_in_memory_database)
    student_handler.name = name
    student_handler.cpf = cpf
    student_handler.enroll_to_course(course)
    course_handler = CourseHandler(set_in_memory_database)

    actual = course_handler.list_all_courses_with_details()

    assert len(actual) > 0
    assert "mat" in actual


def test_list_empty_when_no_enrolled_students(set_in_memory_database):
    course_handler = CourseHandler(set_in_memory_database)
    course_handler.name = "any"

    actual = course_handler.list_student_details()

    assert len(actual) == 0


def test_list_enrolled_students_in_specific_course(set_in_memory_database):
    name = "any"
    cpf = "123.456.789-10"
    course = "any"
    student_handler = StudentHandler(set_in_memory_database)
    student_handler.name = name
    student_handler.cpf = cpf
    student_handler.enroll_to_course(course)
    course_handler = CourseHandler(set_in_memory_database)
    course_handler.name = course

    actual = course_handler.list_student_details()

    assert utils.generate_student_identifier(name, cpf, course) in actual
    assert len(actual) == 1


def test_enroll_student_to_cancelled_course_return_error(set_in_memory_database):
    course_handler = CourseHandler(set_in_memory_database)
    course_handler.name = "adm"
    course_handler.add_subject("any1")
    course_handler.add_subject("any2")
    course_handler.add_subject("any3")
    course_handler.activate()
    course_handler.cancel()

    with pytest.raises(NonValidCourse):
        course_handler.enroll_student("any")


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

    course_handler.load_from_database("adm")
    assert database.course.enrolled_students == ["any"]


def test_cancel_inactive_course(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.name = "adm"
    course_handler.add_subject("any1")
    course_handler.add_subject("any2")
    course_handler.add_subject("any3")
    course_handler.deactivate()
    assert course_handler.cancel() == "cancelled"

    course_handler.load_from_database("adm")
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
    course_handler.load_from_database("adm")
    assert database.course.state == "cancelled"


def test_deactivate_non_active_course_return_error(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    with pytest.raises(NonValidCourse):
        course_handler.deactivate()

    course_handler.load_from_database("adm")
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

    course_handler.load_from_database("adm")
    assert database.course.state == "inactive"


def test_activate_course_without_minimum_subjects_return_error(set_in_memory_database):
    database = set_in_memory_database
    name = "nosubjects"
    course_handler = CourseHandler(database)
    course_handler.name = name
    with pytest.raises(NonMinimunSubjects):
        course_handler.activate()

    course_handler.load_from_database(name)
    assert database.course.state != "active"


def test_activate_course_without_name_return_error(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    with pytest.raises(NonValidCourse):
        course_handler.activate()


def test_activate_course(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.name = "adm"
    course_handler.add_subject("any1")
    course_handler.add_subject("any2")
    course_handler.add_subject("any3")
    assert course_handler.activate() == "active"

    assert database.course.state == "active"
