from pytest import fixture
from architecture.code_analysis_v3.core.course import Course, CourseInProgress
from architecture.code_analysis_v3.core.student import Student, StudentInProgress
from architecture.code_analysis_v3.core.subject import Subject, SubjectInProgress
from architecture.code_analysis_v3.tests.test_core.test_constants import ANY_NAME


def _get_student_inprogress(course):
    student = Student(ANY_NAME)
    student.course = course
    for i in range(3):
        subject = Subject(f"{ANY_NAME}{i}")
        subject.course = course
        student.subscribe_to_subject(subject)
    assert isinstance(student.state, StudentInProgress)
    return student


def _get_subject_inprogress(course):
    subject = Subject(ANY_NAME)
    subject.course = course
    for _ in range(3):
        student = _get_student_inprogress(course)
        student.subscribe_to_subject(subject)
    assert isinstance(subject.state, SubjectInProgress)
    return subject


def _get_course_in_progress(course):
    for _ in range(3):
        _get_subject_inprogress(course)
    assert isinstance(course.state, CourseInProgress)
    return course


@fixture
def student_in_progress():
    course = Course(ANY_NAME)
    yield _get_student_inprogress(course)


@fixture
def subject_in_progress():
    course = Course(ANY_NAME)
    subject = _get_subject_inprogress(course)
    yield subject


@fixture
def course_in_progress():
    course = Course(ANY_NAME)
    yield _get_course_in_progress(course)
