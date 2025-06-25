import logging
from typing import TYPE_CHECKING
from architecture.code_analysis.core.common import IState
from architecture.code_analysis.core.exceptions import InvalidStateTransitionError

if TYPE_CHECKING:
    from architecture.code_analysis.core.subject import Subject
    from architecture.code_analysis.core.student import Student

LOGGER = logging.getLogger(__name__)


class Course:
    def __init__(self, name):
        self._students: list[Student] = []  # to be implemented
        self._subjects: list["Subject"] = []
        self._state: IState = NotStarted
        # TODO 21. Course and subject names must have a maximum of 10 letters.
        # can truncate if bigger than 10?
        self._name: str = name
        # 9. Courses must have a unique identifier and name.
        self._niu: int = self.__hash__()

    def __str__(self):
        return f"{self._niu} '{self._name}'"

    @property
    def state(self) -> IState:
        return self._state

    @state.setter
    def state(self, value: IState) -> None:
        self._state = value.get_next_state(self)

    def add_subject(self, subject: "Subject") -> None:
        # TODO check if subject in list and concluded
        subject.add_to_course(self)
        self._subjects.append(subject)
        LOGGER.info(f"{subject} added to {self}")
        self._state = self.state.get_next_state(self)

    def has_minimum_students(self) -> bool:
        result = len(self._students) >= 9
        if not result:
            LOGGER.warning(f"{self} does not have the minimum students")
        else:
            LOGGER.info(f"{self} has the minimum students")
        return result

    def subject_notify_minimun_students(self, subject: "Subject") -> None:
        LOGGER.info(f"{subject} notify minimum students to {self}")
        self._state = self.state.get_next_state(self)

    def has_minimun_subjects(self) -> bool:
        result = len(self._subjects) >= 3
        if not result:
            LOGGER.warning(f"{self} does not have the minimum subjects")
        else:
            LOGGER.info(f"{self} has the minimum subjects")
        return result

    def accept_student(self, student: "Student") -> None:
        self._students.append(student)

    def list_subjects_by(self, student) -> list["Subject"]:
        return [s for s in self._subjects if student in self._students]

    def list_all_subjects_by(self, student) -> list["Subject"]:
        return [s for s in self._subjects if student in self._students]

    def list_all_subjects(self) -> list["Subject"]:
        return self._subjects


class NotStarted(IState):
    def get_next_state(context: Course):
        if context.state == InProgress:
            raise InvalidStateTransitionError(f"{context.state} to {NotStarted}")
        if all([context.has_minimum_students(), context.has_minimun_subjects()]):
            LOGGER.info(f"{context} state changed to 'in progress'")
            return InProgress
        LOGGER.info(f"{context} state changed to 'not started'")
        return NotStarted


class InProgress(IState):
    def get_next_state(context: Course) -> IState:
        LOGGER.info(f"{context} state changed to 'in progress'")
        return InProgress
