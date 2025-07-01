from pytest import fixture, raises
from core.exceptions import InvalidStateTransition
from core.gss import (
    GSS,
    IGSS,
    GSSApproved,
    GSSFailed,
    GSSInitialState,
)
from tests.test_core.validator_classes import (
    ValidatorCourse,
    ValidatorStudent,
    ValidatorSubject,
)


@fixture
def gss():
    yield GSS()


class TestGSSStateTransition:
    def test_gss_in_initial_state_when_created(self, gss: IGSS):
        assert isinstance(gss.state, GSSInitialState)

    def test_gss_approved_when_grade_greater_than_minimum(self, gss: IGSS):
        gss.set_(8, ValidatorSubject(), ValidatorStudent())
        assert isinstance(gss.state, GSSApproved)

    def test_gss_approved_when_grade_equals_to_minimum(self, gss: IGSS):
        gss.set_(7, ValidatorSubject(), ValidatorStudent())
        assert isinstance(gss.state, GSSApproved)

    def test_gss_failed_when_grade_less_than_minimum(self, gss: IGSS):
        gss.set_(6, ValidatorSubject(), ValidatorStudent())
        assert isinstance(gss.state, GSSFailed)

    def test_gss_state_no_change_when_approved(self, gss: IGSS):
        subject, student = ValidatorSubject(), ValidatorStudent()
        gss.set_(8, subject, student)
        with raises(InvalidStateTransition):
            gss.set_(0, subject, student)

    def test_gss_state_no_change_when_failed(self, gss: IGSS):
        subject, student = ValidatorSubject(), ValidatorStudent()
        gss.set_(0, subject, student)
        with raises(InvalidStateTransition):
            gss.set_(8, subject, student)


class TestGSSNotifyStudent:
    def test_student_gss_notify_student_when_student_and_subject_related(self, gss: IGSS):
        grade = 9
        course = ValidatorCourse()
        subject = ValidatorSubject()
        subject.force_course(course)
        student = ValidatorStudent()
        student.course = course
        student.subscribe_to_subject(subject)
        gss.set_(
            grade,
            subject,
            student,
        )
        assert student.gpa == grade
