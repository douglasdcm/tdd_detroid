from architecture.code_analysis_v3.core.course import ICourse
from architecture.code_analysis_v3.core.gss import IGSS
from architecture.code_analysis_v3.core.student import IStudent
from architecture.code_analysis_v3.core.subject import ISubject
from architecture.code_analysis_v3.core.teacher import AbstractTeacher

EMPTY_NAME = ""


def test_student():
    student = IStudent(EMPTY_NAME)
    assert student is not None


def test_subject():
    student = ISubject(EMPTY_NAME)
    assert student is not None


def test_course():
    student = ICourse(EMPTY_NAME)
    assert student is not None


def test_gss():
    student = IGSS(EMPTY_NAME)
    assert student is not None


def test_teacher():
    student = AbstractTeacher(EMPTY_NAME)
    assert student is not None
