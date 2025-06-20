import pytest
from core.student import Locked, Student, Approved, InProgress
from core.exceptions import InvalidStateTransitionError


def test_in_progress_to_approved():
    s = Student("")
    assert s.state == InProgress
    s.grade = 10
    assert s.state == Approved


def test_in_progress_to_locked():
    s = Student("")
    s.state = Locked
    assert s.state == Locked


def test_locked_to_in_progress():
    s = Student("")
    s.state = Locked
    s.state = InProgress
    assert s.state == InProgress


def test_locked_to_approved():
    s = Student("")
    s.state = Locked
    with pytest.raises(InvalidStateTransitionError):
        s.state = Approved


def test_approved_to_in_progress():
    s = Student("")
    s.grade = 10
    assert s.state == Approved
    with pytest.raises(InvalidStateTransitionError):
        s.state = InProgress


def test_approved_to_locked():
    s = Student("")
    s.grade = 10
    assert s.state == Approved
    with pytest.raises(InvalidStateTransitionError):
        s.state = Locked
