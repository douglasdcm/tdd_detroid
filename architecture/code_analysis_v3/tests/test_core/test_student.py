from pytest import fixture
from architecture.code_analysis_v3.core.course import Cancelled, ConcreteCourse, NoneCourse
from architecture.code_analysis_v3.core.gss import NoneGSS
from architecture.code_analysis_v3.core.student import (
    Approved,
    IStudent,
    ConcretStudent,
    InProgress,
    InitialState,
    Locked,
)
from architecture.code_analysis_v3.core.subject import NoneSubject

ANY_NAME = "any"


@fixture
def student():
    yield ConcretStudent(ANY_NAME)


class TestStudentMissingSubjects:
    def test_student_calculate_missing_subjects_return_empty_list_when_state_in_progress(
        self, student: IStudent
    ):
        student.calculate_missing_subjects()
        assert student.missing_subjects == []

    def test_student_calculate_missing_subjects_return_full_list_when_state_in_progress(
        self, student: IStudent
    ):
        student.notify_me_about_gss(NoneGSS())
        student.calculate_missing_subjects()
        assert len(student.missing_subjects) > 0


class TestStudentState:
    @fixture
    def student_in_progress(self, student):
        student.course = ConcreteCourse("")
        student.subscribe_to_subject(NoneSubject())
        student.subscribe_to_subject(NoneSubject())
        student.subscribe_to_subject(NoneSubject())
        yield student

    def test_student_inprogress_when_has_course_and_minimum_subjects(
        self, student_in_progress: IStudent
    ):
        assert isinstance(student_in_progress.state, InProgress)

    def test_student_has_initial_state_when_has_course_and_no_subjects(self, student: IStudent):
        student.course = ConcreteCourse("")
        assert isinstance(student.state, InitialState)

    def test_student_has_initial_state_when_no_course_and_has_subjects(self, student: IStudent):
        student.subscribe_to_subject(NoneSubject())
        assert isinstance(student.state, InitialState)

    def test_student_has_initial_state_when_no_course_and_no_subjects(self, student: IStudent):
        assert isinstance(student.state, InitialState)

    def test_student_approved_when_minimum_grade_and_subjects_approved(
        self, student_in_progress: IStudent
    ):
        student_in_progress.notify_me_about_gss(NoneGSS())
        assert isinstance(student_in_progress.state, Approved)

    def test_student_locked_when_couse_cancelled(self, student_in_progress: IStudent):
        course = ConcreteCourse(ANY_NAME)
        course.state = Cancelled()
        student_in_progress.notify_me_about_course(course)
        assert isinstance(student_in_progress.state, Locked)
