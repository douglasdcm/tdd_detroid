import pytest
from .core.course import Course, InProgress, NotStarted
from .core.subject import Subject
from .core.exceptions import InvalidStateTransitionError


def set_course_to_in_progress(c: Course):
    c._students = [n for n in range(100)]
    for _ in range(10):
        c.add_subject(Subject(""))


def test_not_started_to_in_progress():
    c = Course("")
    assert c.state == NotStarted
    set_course_to_in_progress(c)
    assert c.state == InProgress


def test_in_progress_to_not_started():
    c = Course("")
    set_course_to_in_progress(c)
    assert c.state == InProgress
    with pytest.raises(InvalidStateTransitionError):
        c.state = NotStarted
