from src.core.course import AbstractCourse
from src.core.gss import IGSS
from src.core.student import AbstractStudent
from src.core.subject import AbstractSubject
from src.core.teacher import AbstractTeacher

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
