import logging
from typing import TYPE_CHECKING
from architecture.code_analysis.core.common import IState
from architecture.code_analysis.core.exceptions import InvalidStudentError, InvalidSubjectError

if TYPE_CHECKING:
    from architecture.code_analysis.core.teacher import Teacher
    from architecture.code_analysis.core.student import Student
    from architecture.code_analysis.core.course import Course

LOGGER = logging.getLogger(__name__)


class Subject:
    def __init__(self, name:str):
        self._teacher: "Teacher" = None
        # TODO 7. The system must calculate the student's situation taking into account the subjects taken and the total number of subjects in each course.
        self._state: IState = Locked
        self._students: list["Student"] = []
        self._course: "Course" = None
        # TODO 21. Course and subject names must have a maximum of 10 letters.
        # can truncate in case of big names?
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

    def _has_enrolled_students_over_the_maximum_value(self):
        # 29. Each subject can have a maximum of 30 enrolled students.
        result = len(self._students) >= 30
        if not result:
            LOGGER.warning(f"{self} does not have the maximum students")
        else:
            InvalidSubjectError(f"{self} has the maximum students")
        return result

    def subscribe_student(self, student: "Student"):
        self._has_enrolled_students_over_the_maximum_value()
        if not self._course:
            raise InvalidSubjectError(f"{self} not in a course")
        if not student.course == self._course:
            # 8. The student can only take subjects from their course.
            raise InvalidStudentError(f"{student} not in {self._course}")
        # TODO 4. If a student takes the same subject more than once, the highest grade will be considered in the GPA calculation.
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
