import logging
from typing import TYPE_CHECKING
from architecture.code_analysis.core.common import IState

if TYPE_CHECKING:
    from architecture.code_analysis.core.subject import Subject
    from architecture.code_analysis.core.subject import Student
    from architecture.code_analysis.core.teacher import Teacher
LOGGER = logging.getLogger(__name__)


class GSS:
    # Grade, Subject, Student
    def __init__(self):
        self._grade: int = 0
        self._subject: "Subject" = None
        self._student: "Student" = None
        self._state: IState = NoneObject

    def set_(self, grade: int, subject: "Subject", student: "Student")-> None:
        # TODO set the values and notify the student
        # notify subject state (approved, failed)
        pass

    def _calculate_subject_state(self) -> int:
        # TODO Approved if grade >= 7, otherwise failed
        # This instance is created at the end of the semester
        pass

    def _notify_subject(self, student: "Student") -> None:
        # TODO send itself to student
        pass


class Aproved(IState):
    def get_next_state(context: "Teacher")-> IState:
        return Aproved


class Failed(IState):
    def get_next_state(context: "Teacher")-> IState:
        return Failed


class NoneObject(IState):
    # Starting point
    def get_next_state(context: "Teacher")-> IState:
        return NoneObject
