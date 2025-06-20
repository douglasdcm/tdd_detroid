import logging
from typing import TYPE_CHECKING
from core.common import IState

if TYPE_CHECKING:
    from subject import Subject
    from student import Student

LOGGER = logging.getLogger(__name__)


class Teacher:
    def __init__(self, name):
        self._course = None
        self._name = name

    def __str__(self):
        return f"'{self._name}'"

    def subscribe_to(self, subject: "Subject"):
        LOGGER.info(f"{self} added to {subject}")
        subject.subcribe_teacher(self)

    def set_the_grade_of_students_in_their_subject():
        # rules
        # the student must be in the subject, not locked
        # the subject must be in progress
        pass

    def teach_maximum_Subject():
        pass

    def does_not_teach_maximum_Subject():
        pass

    def authenticate():
        pass


class TeacherCredential:
    pass


class SubjectUniqueIdentifier:
    pass


class GradeControl:
    under_minimum_value: None
    between_minimum_and_maximum_values: None
    above_maximum_value: None
    can_update: None
    can_not_upate: None


class CourseUniqueIdentifier:
    pass


class EnrollmentList:
    pass
