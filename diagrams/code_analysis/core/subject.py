import logging
from typing import TYPE_CHECKING
from core.common import IState
from core.exceptions import InvalidStateTransitionError, InvalidStudentError, InvalidSubjectError

if TYPE_CHECKING:
    from core.student import Student
    from core.course import Course
    from core.teaching import Teacher

LOGGER = logging.getLogger(__name__)


class Subject:
    can_update: None
    can_not_update: None
    has_minimum_enrolled_Students: None
    does_not_have_minimum_enrolled_Students: None
    has_enrolled_Students_over_the_maximum_value: None
    locked: None
    unlocked: None

    def __init__(self, name):
        self._teacher: "Teacher" = None
        self._state = Locked
        self._students: list["Student"] = []
        self._course: "Course" = None
        self._name = name

    def __str__(self):
        return f"'{self._name}'"

    @property
    def state(self):
        return self._state

    @property
    def students(self):
        return self._students

    def _has_minimun_students(self):
        result = len(self._students) >= 3
        if not result:
            LOGGER.warning(f"{self} does not have the minimum students")
        else:
            LOGGER.info(f"{self} has the minimum students")
        return result

    def subscribe_student(self, student: "Student"):
        if not self._course:
            raise InvalidSubjectError(f"{self} not in a course")
        if not student.course == self._course:
            raise InvalidStudentError(f"{student} not in a {self._course}")
        if self in student.subjects:
            raise InvalidSubjectError(f"{student} already subscribed to {self}")
        self._students.append(student)
        if self._has_minimun_students():
            self._course.subject_notify_minimun_students(self)

    def subcribe_teacher(self, teacher: "Teacher"):
        self._teacher = teacher

    def has_teacher(self):
        return self._teacher is not None

    def add_to_course(self, course: "Course"):
        self._course = course


class Locked(IState):
    def get_next_state(context: Subject):
        LOGGER.info(f"{context} state changed to 'locked'")
        return Locked


class InProgress(IState):
    def get_next_state(context: Subject):
        LOGGER.info(f"{context} state changed to 'in progress'")
        return InProgress
