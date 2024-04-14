from src.services.student_handler import StudentHandler
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

    assert subject_handler.name == "any_name"
    assert subject_handler.identifier is -1
    assert subject_handler.state == None
    assert subject_handler.enrolled_students == []
    assert subject_handler.max_enrollment == 0
    assert subject_handler.course == None


def test_course_model(set_in_memory_database):
    database = set_in_memory_database
    course_handler = CourseHandler(database)
    course_handler.name = "any_name"
    course_handler.save()

    assert course_handler.name == "any_name"
    assert course_handler.identifier is not None
    assert course_handler.state == "inactive"
    assert course_handler.enrolled_students == []
    assert course_handler.max_enrollment == 0
    assert course_handler.subjects == []

    assert database.course.name == "any_name"
    assert database.course.identifier is not None
    assert database.course.state == "inactive"
    assert database.course.enrolled_students == ""
    assert database.course.max_enrollment == 0
    assert database.course.subjects == ""


def test_student_model(set_in_memory_database):
    database = set_in_memory_database
    student = StudentHandler(database)
    student.name = "any_name"
    student.cpf = "123.456.789-10"

    assert student.name == "any_name"
    assert student.cpf == "123.456.789-10"
    assert student.identifier is None
    assert student.state == None
    assert student.gpa == 0
    assert student.subjects == []
