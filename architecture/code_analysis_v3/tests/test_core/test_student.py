from pytest import fixture, raises
from architecture.code_analysis_v3.core.course import ConcreteCourse
from architecture.code_analysis_v3.core.gss import ConcreteGSS, NoneGSS
from architecture.code_analysis_v3.core.student import (
    Approved,
    IStudent,
    ConcretStudent,
    InProgress,
    InitialState,
    InvalidStateTransition,
    InvalidSubject,
)
from architecture.code_analysis_v3.core.subject import ConcreteSubject

ANY_NAME = "any"


@fixture
def student():
    yield ConcretStudent(ANY_NAME)


@fixture
def student_in_progress(student: IStudent):
    student.course = ConcreteCourse(ANY_NAME)
    for _ in range(3):
        subject = ConcreteSubject(ANY_NAME)
        subject.course = student.course
        student.subscribe_to_subject(subject)
    yield student


@fixture
def student_approved(student_in_progress: IStudent):
    subjects = student_in_progress.subjects_in_progress
    for subject in subjects:
        gss = ConcreteGSS()
        gss.set_(9, subject, student_in_progress)
        student_in_progress.notify_me_about_gss(gss)
    yield student_in_progress


class TestStudentMissingSubjects:
    def test_student_calculate_missing_subjects_return_empty_list_when_state_approved(
        self, student_approved: IStudent
    ):
        student_approved.calculate_missing_subjects()
        assert student_approved.missing_subjects == []

    def test_student_calculate_missing_subjects_return_full_list_when_state_in_progress(
        self, student_in_progress: IStudent
    ):
        student_in_progress.calculate_missing_subjects()
        assert len(student_in_progress.missing_subjects) > 0


class TestStudentState:
    def test_student_inprogress_when_has_course_and_minimum_subjects(
        self, student_in_progress: IStudent
    ):
        assert isinstance(student_in_progress.state, InProgress)

    def test_student_has_initial_state_when_has_course_and_no_subjects(self, student: IStudent):
        student.course = ConcreteCourse("")
        assert isinstance(student.state, InitialState)

    def test_student_has_initial_state_when_no_course_and_no_subjects(self, student: IStudent):
        assert isinstance(student.state, InitialState)

    def test_student_approved_when_minimum_grade_and_subjects_approved(
        self, student_approved: IStudent
    ):
        assert isinstance(student_approved.state, Approved)

    def test_student_approved_does_not_change_state(self, student_approved: IStudent):
        with raises(InvalidStateTransition):
            subject = ConcreteSubject(ANY_NAME)
            subject.course = student_approved.course
            student_approved.subscribe_to_subject(subject)


class TestSubscribeToSubject:
    def test_student_can_subscribe_to_subjects_in_their_course_only(self, student: IStudent):
        with raises(InvalidSubject):
            student.subscribe_to_subject(ConcreteSubject(ANY_NAME))

    def test_student_cannot_have_subject_when_no_course(self, student: IStudent):
        with raises(InvalidSubject):
            student.subscribe_to_subject(ConcreteSubject(ANY_NAME))


class TestNotifyGSS:
    def test_student_gss_notification_set_state_to_approved_when_all_subjects_approved(
        self, student_approved: IStudent
    ):
        assert isinstance(student_approved.state, Approved)

    def test_student_gss_notification_keep_state_inprogress_when_any_subject_failed(
        self, student_in_progress: IStudent
    ):
        first_subject = student_in_progress.subjects_in_progress[0]
        gss = ConcreteGSS()
        gss.set_(3, first_subject, student_in_progress)
        student_in_progress.notify_me_about_gss(gss)
        assert isinstance(student_in_progress.state, InProgress)
