from pytest import fixture
from architecture.code_analysis_v3.core.course import Course
from architecture.code_analysis_v3.core.gss import GSS
from architecture.code_analysis_v3.core.student import (
    AbstractStudent,
    Student,
)
from architecture.code_analysis_v3.core.subject import Subject
from architecture.code_analysis_v3.tests.test_core.test_constants import ANY_NAME


@fixture
def student():
    yield Student(ANY_NAME)


@fixture
def student_in_progress(student: AbstractStudent):
    student.course = Course(ANY_NAME)
    for i in range(3):

        subject = Subject(f"{ANY_NAME}{i}")
        subject.course = student.course
        student.subscribe_to_subject(subject)
    yield student


@fixture
def student_approved(student_in_progress: AbstractStudent):
    subjects = student_in_progress.subjects_in_progress
    for subject in subjects:
        gss = GSS()
        gss.set_(9, subject, student_in_progress)
        student_in_progress.notify_me_about_gss(gss)
    yield student_in_progress


# class TestSubjectStateTransition:
#     def test_subject_notworking_when_created(self):
#         subject = ConcreteSubject(ANY_NAME)
#         assert isinstance(subject.state, NotWorking)
