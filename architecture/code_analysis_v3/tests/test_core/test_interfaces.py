from architecture.code_analysis_v3.core.course import AbstractCourse
from architecture.code_analysis_v3.core.gss import IGSS
from architecture.code_analysis_v3.core.student import AbstractStudent
from architecture.code_analysis_v3.core.subject import AbstractSubject
from architecture.code_analysis_v3.core.teacher import AbstractTeacher

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
