import pytest
from src.services.student_handler import StudentHandler, NonValidGrade
from src.services.course_handler import CourseHandler
from src.services.subject_handler import SubjectHandler
from src.services.semester_monitor import SemesterMonitor


def test_semester_model(set_in_memory_database):
    semester = SemesterMonitor(set_in_memory_database, "2024-1")

    assert semester.identifier == "2024-1"
    assert semester.state == "open"


def test_subject_model(set_in_memory_database):
    database = set_in_memory_database
    subject_handler = SubjectHandler(database)
    subject_handler.name = "any_name"
    subject_handler.course = "any"

    assert subject_handler.name == "any_name"
    assert subject_handler.identifier is not -1
    assert subject_handler.state == None
    assert subject_handler.enrolled_students == []
    assert subject_handler.max_enrollment == 0
    assert subject_handler.course == "any"


def test_course_model(set_in_memory_database):
    course = "any"
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.name = course
    course_handler.save()

    assert course_handler.name == course
    assert course_handler.identifier is not None
    assert course_handler.state == "inactive"
    assert course_handler.enrolled_students == []
    assert course_handler.max_enrollment == 0
    assert course_handler.subjects == []

    course_handler.load_from_database(course)
    assert database.course.name == course
    assert database.course.identifier is not None
    assert database.course.state == "inactive"
    assert database.course.enrolled_students == []
    assert database.course.max_enrollment == 0
    assert database.course.subjects == []


def test_student_model(set_in_memory_database):
    database = set_in_memory_database
    student = StudentHandler(database)
    student.name = "any"
    student.cpf = "123.456.789-10"

    assert student.name == "any"
    assert student.cpf == "123.456.789-10"
    assert student.identifier is None
    assert student.state == None
    assert student.subjects == []
