from pytest import fixture, raises, mark
from architecture.code_analysis_v3.core.course import Course
from architecture.code_analysis_v3.core.gss import GSS
from architecture.code_analysis_v3.core.student import (
    StudentApproved,
    BasicInformation,
    AbstractStudent,
    Student,
    StudentInProgress,
    StudentInitialState,
    InvalidStateTransition,
    InvalidSubject,
)
from architecture.code_analysis_v3.core.subject import Subject
from architecture.code_analysis_v3.tests.test_core.test_constants import ANY_NAME, OTHER_NAME


@fixture
def student():
    yield Student(ANY_NAME)


@fixture
def student_approved(student_in_progress: AbstractStudent):
    subjects = student_in_progress.subjects_in_progress
    for subject in subjects:
        gss = GSS()
        gss.set_(9, subject, student_in_progress)
        student_in_progress.notify_me_about_gss(gss)
    yield student_in_progress


class TestStudentState:
    def test_student_inprogress_when_has_course_and_minimum_subjects(
        self, student_in_progress: AbstractStudent
    ):
        assert isinstance(student_in_progress.state, StudentInProgress)

    def test_student_has_initial_state_when_has_course_and_no_subjects(
        self, student: AbstractStudent
    ):
        student.course = Course("")
        assert isinstance(student.state, StudentInitialState)

    def test_student_has_initial_state_when_no_course_and_no_subjects(
        self, student: AbstractStudent
    ):
        assert isinstance(student.state, StudentInitialState)

    def test_student_approved_when_minimum_grade_and_subjects_approved(
        self, student_approved: AbstractStudent
    ):
        assert isinstance(student_approved.state, StudentApproved)

    def test_student_approved_does_not_change_state(self, student_approved: AbstractStudent):
        with raises(InvalidStateTransition):
            subject = Subject(ANY_NAME)
            subject.course = student_approved.course
            student_approved.subscribe_to_subject(subject)


class TestSubscribeToSubject:
    def test_student_can_subscribe_to_subjects_in_their_course_only(self, student: AbstractStudent):
        with raises(InvalidSubject):
            student.subscribe_to_subject(Subject(ANY_NAME))

    def test_student_cannot_have_subject_when_no_course(self, student: AbstractStudent):
        with raises(InvalidSubject):
            student.subscribe_to_subject(Subject(ANY_NAME))


class TestNotifyGSS:
    def test_student_gss_notification_set_state_to_approved_when_all_subjects_approved(
        self, student_approved: AbstractStudent
    ):
        assert isinstance(student_approved.state, StudentApproved)
        assert student_approved.gpa == 9

    def test_student_gss_notification_keep_state_inprogress_when_any_subject_failed(
        self, student_in_progress: AbstractStudent
    ):
        first_subject = student_in_progress.subjects_in_progress[0]
        gss = GSS()
        # grade < 7 is failed
        gss.set_(3, first_subject, student_in_progress)
        student_in_progress.notify_me_about_gss(gss)
        assert isinstance(student_in_progress.state, StudentInProgress)


class TestGpaCalculation:
    @mark.parametrize(
        "grade1,grade2,grade3,expected",
        [
            (9, 0, 0, 3),
            (9, 9, 0, 6),
            (9, 9, 9, 9),
        ],
    )
    def test_student_grade_calculation_when_all_subjects_graded(
        self, grade1, grade2, grade3, expected, student_in_progress: AbstractStudent
    ):
        subjects = student_in_progress.subjects_in_progress
        assert len(subjects) == 3
        gss1 = GSS()
        gss1.set_(grade1, subjects[0], student_in_progress)
        gss2 = GSS()
        gss2.set_(grade2, subjects[1], student_in_progress)
        gss3 = GSS()
        gss3.set_(grade3, subjects[2], student_in_progress)

        student_in_progress.notify_me_about_gss(gss1)
        student_in_progress.notify_me_about_gss(gss2)
        student_in_progress.notify_me_about_gss(gss3)
        assert student_in_progress.gpa == expected

    @mark.parametrize(
        "grade,expected",
        [
            (6, 6),
            (7, 7),
            (8, 8),
        ],
    )
    def test_student_grade_calculation_when_one_subject_graded(
        self, grade, expected, student_in_progress: AbstractStudent
    ):
        subjects = student_in_progress.subjects_in_progress
        assert len(subjects) == 3
        gss = GSS()
        gss.set_(grade, subjects[0], student_in_progress)
        student_in_progress.notify_me_about_gss(gss)
        assert student_in_progress.gpa == expected


class TestAddBasicInformation:
    def test_add_basic_information(self, student: AbstractStudent):
        AGE = 42
        information = BasicInformation(ANY_NAME, 42)
        student.add_basic_information(information)
        assert student.name == ANY_NAME
        assert student.age == AGE

    def test_change_basic_information(self, student: AbstractStudent):
        AGE = 42
        OTHER_AGE = 24
        information = BasicInformation(ANY_NAME, AGE)
        student.add_basic_information(information)
        information = BasicInformation(OTHER_NAME, OTHER_AGE)
        student.add_basic_information(information)
        assert student.name == OTHER_NAME
        assert student.age == OTHER_AGE


class TestListMissingSubjects:
    def test_list_empty_missing_subjects_when_student_approved(
        self, student_approved: AbstractStudent
    ):
        assert len(student_approved.missing_subjects) == 0

    def test_list_full_missing_subjects_when_student_inprogress(
        self, student_in_progress: AbstractStudent
    ):
        assert len(student_in_progress.missing_subjects) > 0


class TestListSubjectsInProgress:
    def test_list_empty_subjects_in_progress_when_student_approved(
        self, student_approved: AbstractStudent
    ):
        assert len(student_approved.subjects_in_progress) == 0

    def test_list_full_missing_subjects_when_student_inprogress(
        self, student_in_progress: AbstractStudent
    ):
        assert len(student_in_progress.subjects_in_progress) > 0
