from src.services.student_handler import StudentHandler
from src.services.course_handler import CourseHandler
from src.services.subject_handler import SubjectHandler
from src.services.semester_monitor import SemesterHandler
from src import mock_database


def test_semester_model():
    semester = SemesterHandler()

    assert semester.identifier == "2024-1"
    assert semester.state == "open"


def test_subject_model():
    subject = SubjectHandler()
    subject.name = "any_name"

    assert subject.name == "any_name"
    assert subject.identifier is not None
    assert subject.state == None
    assert subject.enrolled_students == []
    assert subject.max_enrollment == 0
    assert subject.course == None


def test_course_model():
    course = CourseHandler()
    course.name = "any_name"

    assert course.name == "any_name"
    assert course.identifier is not None
    assert course.state == "inactive"
    assert course.enrolled_students == []
    assert course.max_enrollment == 0
    assert course.subjects == []


def test_student_model():
    database = mock_database.Database()
    student = StudentHandler(database)
    student.name = "any_name"
    student.cpf = "123.456.789-10"

    assert student.name == "any_name"
    assert student.cpf == "123.456.789-10"
    assert student.identifier is None
    assert student.state == None
    assert student.gpa == 0
    assert student.subjects == []
