from src.services.student_handler import StudentHandler
from src.services.course_handler import CourseHandler
from src.services.subject_handler import SubjectHandler
from src.services.semester_monitor import SemesterHandler
from src import mocks


def test_semester_model():
    semester = SemesterHandler()

    assert semester.identifier == "2024-1"
    assert semester.state == "open"


def test_subject_model():
    database = mocks.Database()
    subject = SubjectHandler(database)
    subject.name = "any_name"
    subject.save()

    assert subject.name == "any_name"
    assert subject.identifier is not None
    assert subject.state == None
    assert subject.enrolled_students == []
    assert subject.max_enrollment == 0
    assert subject.course == None

    assert database.subject.name == "any_name"
    assert database.subject.identifier is not None
    assert database.subject.state == None
    assert database.subject.enrolled_students == []
    assert database.subject.max_enrollment == 0
    assert database.subject.course == None


def test_course_model():
    database = mocks.Database()
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


def test_student_model():
    database = mocks.Database()
    student = StudentHandler(database)
    student.name = "any_name"
    student.cpf = "123.456.789-10"
    student.save()

    assert student.name == "any_name"
    assert student.cpf == "123.456.789-10"
    assert student.identifier is None
    assert student.state == None
    assert student.gpa == 0
    assert student.subjects == []

    assert database.student.name == "any_name"
    assert database.student.cpf == "123.456.789-10"
    assert database.student.identifier is None
    assert database.student.state == None
    assert database.student.gpa == 0
    assert database.student.subjects == []
