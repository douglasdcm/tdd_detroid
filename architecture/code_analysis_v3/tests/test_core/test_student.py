from pytest import fixture, raises
from architecture.code_analysis_v3.core.course import ConcreteCourse
from architecture.code_analysis_v3.core.gss import ConcreteGSS, NoneGSS
from architecture.code_analysis_v3.core.student import (
    Approved,
    BasicInformation,
    IStudent,
    ConcretStudent,
    InProgress,
    InitialState,
    InvalidStateTransition,
    InvalidSubject,
)
from architecture.code_analysis_v3.core.subject import ConcreteSubject

ANY_NAME = "any"
OTHER_NAME = "any"


@fixture
def student():
    yield ConcretStudent(ANY_NAME)


@fixture
def student_in_progress(student: IStudent):
    student.course = ConcreteCourse(ANY_NAME)
    for i in range(3):

        subject = ConcreteSubject(f"{ANY_NAME}{i}")
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
        # grade < 7 is failed
        gss.set_(3, first_subject, student_in_progress)
        student_in_progress.notify_me_about_gss(gss)
        assert isinstance(student_in_progress.state, InProgress)


class TestAddBasicInformation:
    def test_add_basic_information(self, student: IStudent):
        AGE = 42
        information = BasicInformation(ANY_NAME, 42)
        student.add_basic_information(information)
        assert student.name == ANY_NAME
        assert student.age == AGE

    def test_change_basic_information(self, student: IStudent):
        AGE = 42
        OTHER_AGE = 24
        information = BasicInformation(ANY_NAME, AGE)
        student.add_basic_information(information)
        information = BasicInformation(OTHER_NAME, OTHER_AGE)
        student.add_basic_information(information)
        assert student.name == OTHER_NAME
        assert student.age == OTHER_AGE


class TestListMissingSubjects:
    def test_list_empty_missing_subjects_when_student_approved(self, student_approved: IStudent):
        assert len(student_approved.missing_subjects) == 0

    def test_list_full_missing_subjects_when_student_inprogress(
        self, student_in_progress: IStudent
    ):
        assert len(student_in_progress.missing_subjects) > 0


class TestListSubjectsInProgress:
    def test_list_empty_subjects_in_progress_when_student_approved(
        self, student_approved: IStudent
    ):
        assert len(student_approved.subjects_in_progress) == 0

    def test_list_full_missing_subjects_when_student_inprogress(
        self, student_in_progress: IStudent
    ):
        assert len(student_in_progress.subjects_in_progress) > 0
