import logging
from typing import TYPE_CHECKING
from core.common import IState
from core.exceptions import InvalidStateTransitionError
from core import subject

if TYPE_CHECKING:
    from subject import Subject
    from student import Student

LOGGER = logging.getLogger(__name__)


class Course:
    locked: None
    unlocked: None
    cancelled: None
    not_cancelled: None
    has_Coordinator: None
    does_not_have_Coordinator: None
    does_not_have_minumum_Subjects: None
    does_not_have_minimum_Students: None

    def __init__(self, name):
        self._students: list["Student"] = []  # to be implemented
        self._subjects: list["Subject"] = []
        self._state = NotStarted
        self._name = name

    def __str__(self):
        return f"'{self._name}'"

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: IState):
        self._state = value.get_next_state(self)

    def add_subject(self, subject: "Subject"):
        # TODO check if subject in list
        subject.add_to_course(self)
        self._subjects.append(subject)
        LOGGER.info(f"{subject} added to {self}")
        self._state = self.state.get_next_state(self)

    def has_minimum_students(self):
        result = len(self._students) >= 9
        if not result:
            LOGGER.warning(f"{self} does not have the minimum students")
        else:
            LOGGER.info(f"{self} has the minimum students")
        return result

    def subject_notify_minimun_students(self, subject: "Subject"):
        LOGGER.info(f"{subject} notify minimum students to {self}")
        self._state = self.state.get_next_state(self)

    def has_minimun_subjects(self):
        result = len(self._subjects) >= 3
        if not result:
            LOGGER.warning(f"{self} does not have the minimum subjects")
        else:
            LOGGER.info(f"{self} has the minimum subjects")
        return result

    def has_minimun_students(self):
        result = len(self._students) >= 3
        if not result:
            LOGGER.warning(f"{self} does not have the minimum students")
        else:
            LOGGER.info(f"{self} has the minimum students")
        return result

    def accept_student(self, student):
        self._students.append(student)

    def list_subjects_by(self, student):
        return [s for s in self._subjects if student in self._students]

    def list_all_subjects_by(self, student):
        return [s for s in self._subjects if student in self._students]

    def list_all_subjects(self):
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
    def get_next_state(context: Course):
        LOGGER.info(f"{context} state changed to 'in progress'")
        return InProgress
