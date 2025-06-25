import logging
from typing import TYPE_CHECKING
from architecture.code_analysis_v2.core.common import IState
from architecture.code_analysis_v2.core.base_object import BaseCoreObject

if TYPE_CHECKING:
    from architecture.code_analysis_v2.core.teacher import Teacher, NoneTeacher
    from architecture.code_analysis_v2.core.student import Student
    from architecture.code_analysis_v2.core.course import Course, NoneCourse

LOGGER = logging.getLogger(__name__)


class Subject(BaseCoreObject):
    def __init__(self, name: str):
        self._teacher: Teacher = NoneTeacher()
        # TODO 7. The system must calculate the student's situation taking into account the subjects taken and the total number of subjects in each course.
        self._state: IState = Locked()
        self._students: list["Student"] = []
        self._course: Course = NoneCourse()
        # TODO 21. Course and subject names must have a maximum of 10 letters.
        # can truncate in case of big names?
        self._name = name

    def _has_minimun_students(self) -> bool:
        raise NotImplementedError

    def _has_enrolled_students_over_the_maximum_value(self) -> bool:
        raise NotImplementedError

    def _has_teacher(self) -> bool:
        raise NotImplementedError

    def subscribe_student(self, student: "Student") -> None:
        raise NotImplementedError

    def subcribe_teacher(self, teacher: "Teacher") -> None:
        raise NotImplementedError

    def add_to_course(self, course: "Course") -> None:
        raise NotImplementedError


class NoneSubject(Subject):
    def __init__(self, name=""):
        super().__init__(name)


class Locked(IState):
    @staticmethod
    def get_next_state(context: Subject):
        raise NotImplementedError


class InProgress(IState):
    @staticmethod
    def get_next_state(context: Subject):
        raise NotImplementedError
