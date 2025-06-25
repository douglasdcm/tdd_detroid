from .core import course
from .core.subject import Subject
import logging

LOGGER = logging.getLogger(__name__)


def main():
    # 5. Initially, the university will have 3 courses with 3 subjects each.
    a_course = course.Course("ACourse")
    b_course = course.Course("BCourse")
    c_course = course.Course("CCourse")
    assert a_course.state == course.NotStarted

    for i in range(3):
        a_course.add_subject(Subject(f"ASubject{i}"))
        b_course.add_subject(Subject(f"BSubject{i}"))
        c_course.add_subject(Subject(f"CSubject{i}"))
