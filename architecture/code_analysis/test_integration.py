from .core.teacher import Teacher
from .core import course
from .core.subject import Subject
from .core.student import Student
import logging

LOGGER = logging.getLogger(__name__)


def test_integration():
    """Simulates the sequence diagram from [architecture.(./components.drawio)"""
    # 5. Initially, the university will have 3 courses with 3 subjects each.
    # admin responsability
    a_course = course.Course("TheCourse")
    assert a_course.state == course.NotStarted

    # admin responsability
    # add minimum subjects
    for i in range(3):
        a_course.add_subject(Subject(f"Subject{i}"))

    # teacher responsability
    # subscribe teacher
    for subject in a_course.list_all_subjects():
        Teacher("The Teacher").subscribe_to(subject)

    # add minimun students to subject
    for subject in a_course.list_all_subjects():
        for i in range(3):
            # student responsability
            a_student = Student(f"Student{i}")
            a_student.course = a_course
            a_student.subscribe_subject(subject)
    assert a_course.state == course.InProgress
