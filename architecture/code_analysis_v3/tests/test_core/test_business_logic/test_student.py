from pytest import raises, mark
from core.student import (
    StudentApproved,
    BasicInformation,
    AbstractStudent,
    StudentInProgress,
    StudentInitialState,
    InvalidStateTransition,
    InvalidSubject,
)
from tests.test_core.test_business_logic.validator_classes import (
    ValidatorCourse,
    ValidatorStudent,
    ValidatorSubject,
)

ANY_NAME = "any"
OTHER_NAME = "other"


class TestStudentState:
    def test_student_in_progress_when_has_course_and_minimum_subjects(
        self, student_in_progress: ValidatorStudent
    ):
        student_in_progress.force_has_course()
        student_in_progress.force_has_minimun_subjects()
        assert isinstance(student_in_progress.state, StudentInProgress)

    def test_student_has_initial_state_when_has_course_and_no_subjects(
        self, student: AbstractStudent
    ):
        student.course = ValidatorCourse("")
        assert isinstance(student.state, StudentInitialState)

    def test_student_has_initial_state_when_no_course_and_no_subjects(
        self, student: AbstractStudent
    ):
        assert isinstance(student.state, StudentInitialState)

    def test_student_approved_when_minimum_grade_and_subjects_approved(
        self, student_in_progress: ValidatorStudent
    ):
        student_in_progress.force_gpa(7)
        assert isinstance(student_in_progress.state, StudentApproved)

    def test_student_approved_does_not_change_state(self, student_approved: ValidatorStudent):
        with raises(InvalidStateTransition):
            student_approved.state


class TestSubscribeToSubject:
    def test_student_can_subscribe_to_subjects_in_their_course_only(self, student: AbstractStudent):
        with raises(InvalidSubject):
            student.subscribe_to_subject(ValidatorSubject())

    def test_student_cannot_have_subject_when_no_course(self, student: AbstractStudent):
        with raises(InvalidSubject):
            student.subscribe_to_subject(ValidatorSubject())


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
        self, grade1, grade2, grade3, expected, student_in_progress: ValidatorStudent
    ):
        student_in_progress.force_grades([grade1, grade2, grade3])
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
        self, grade, expected, student_in_progress: ValidatorStudent
    ):
        student_in_progress.force_grades([grade])
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

    def test_list_full_missing_subjects_when_student_in_progress(self, student: ValidatorStudent):
        course = ValidatorCourse()
        course.accept_subject(ValidatorSubject())
        student.course = course
        student.force_has_minimun_subjects()
        assert isinstance(student.state, StudentInProgress)
        assert len(student.missing_subjects) > 0


class TestListSubjectsInProgress:
    def test_list_empty_subjects_in_progress_when_student_approved(
        self, student_approved: AbstractStudent
    ):
        assert len(student_approved.subjects_in_progress) == 0
