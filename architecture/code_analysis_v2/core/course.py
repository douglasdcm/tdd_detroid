import logging
from typing import TYPE_CHECKING
from architecture.code_analysis_v2.core.common import IState
from architecture.code_analysis_v2.core.base_object import BaseCoreObject

if TYPE_CHECKING:
    from architecture.code_analysis_v2.core.subject import Subject
    from architecture.code_analysis_v2.core.student import Student

LOGGER = logging.getLogger(__name__)


class Course(BaseCoreObject):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._students: list[Student] = []
        self._subjects: list[Subject] = []
        self._state: IState = NotStarted()
        # TODO 21. Course and subject names must have a maximum of 10 letters.
        # can truncate if bigger than 10?
        self._name: str = name
        # 9. Courses must have a unique identifier and name.

    def _has_minimum_students(self) -> bool:
        raise NotImplementedError

    def _has_minimun_subjects(self) -> bool:
        raise NotImplementedError

    def add_subject(self, subject: "Subject") -> None:
        raise NotImplementedError

    def subject_notify_minimun_students(self, subject: "Subject") -> None:
        raise NotImplementedError

    def accept_student(self, student: "Student") -> None:
        raise NotImplementedError

    def list_subjects_by(self, student) -> list["Subject"]:
        raise NotImplementedError

    def list_all_subjects_by(self, student) -> list["Subject"]:
        raise NotImplementedError

    def list_all_subjects(self) -> list["Subject"]:
        raise NotImplementedError


class NoneCourse(Course):
    def __init__(self, name=""):
        super().__init__(name)


class NotStarted(IState):
    @staticmethod
    def get_next_state(context: Course):
        raise NotImplementedError


class InProgress(IState):
    @staticmethod
    def get_next_state(context: Course):
        raise NotImplementedError
