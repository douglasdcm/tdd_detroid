import logging
from typing import TYPE_CHECKING
from architecture.code_analysis_v2.core.common import IState

if TYPE_CHECKING:
    from architecture.code_analysis_v2.core.subject import Subject, NoneSubject
    from architecture.code_analysis_v2.core.student import Student, NoneStudent
    from architecture.code_analysis_v2.core.teacher import Teacher
LOGGER = logging.getLogger(__name__)


class GSS:
    # Grade, Subject, Student
    def __init__(self) -> None:
        self._grade: int = 0
        self._subject: Subject = NoneSubject()
        self._student: Student = NoneStudent()
        self._state: IState = NoneObject()

    def set_(self, grade: int, subject: "Subject", student: "Student") -> None:
        # TODO set the values and notify the student
        # notify subject state (approved, failed)
        raise NotImplementedError

    def _calculate_subject_state(self) -> int:
        # TODO Approved if grade >= 7, otherwise failed
        # This instance is created at the end of the semester
        raise NotImplementedError

    def _notify_subject(self, student: "Student") -> None:
        # TODO send itself to student
        raise NotImplementedError


class Aproved(IState):
    @staticmethod
    def get_next_state(context: "Teacher") -> IState:
        raise NotImplementedError


class Failed(IState):
    @staticmethod
    def get_next_state(context: "Teacher") -> IState:
        raise NotImplementedError


class NoneObject(IState):
    # Starting state
    @staticmethod
    def get_next_state(context: "Teacher") -> IState:
        raise NotImplementedError
