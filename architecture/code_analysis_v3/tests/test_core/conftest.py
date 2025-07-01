from pytest import fixture
from core.student import (
    StudentApproved,
    StudentInProgress,
)
from tests.test_core.validator_classes import (
    ValidatorStudent,
)


@fixture
def student():
    yield ValidatorStudent()


@fixture
def student_in_progress(student: ValidatorStudent):
    student.force_state(StudentInProgress())
    yield student


@fixture
def student_approved(student: ValidatorStudent):
    student.force_state(StudentApproved())
    yield student
