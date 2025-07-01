from core.course import AbstractCourse
from core.gss import IGSS
from core.student import AbstractStudent
from core.subject import AbstractSubject
from core.teacher import AbstractTeacher

EMPTY_NAME = ""


def test_student():
    student = AbstractStudent(EMPTY_NAME)
    assert student is not None


def test_subject():
    student = AbstractSubject(EMPTY_NAME)
    assert student is not None


def test_course():
    student = AbstractCourse(EMPTY_NAME)
    assert student is not None


def test_gss():
    student = IGSS(EMPTY_NAME)
    assert student is not None


def test_teacher():
    student = AbstractTeacher(EMPTY_NAME)
    assert student is not None
