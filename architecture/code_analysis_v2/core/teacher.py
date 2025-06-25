import logging
from typing import TYPE_CHECKING

from architecture.code_analysis_v2.core.common import IState
from architecture.code_analysis_v2.core.base_object import BaseCoreObject

if TYPE_CHECKING:
    from architecture.code_analysis_v2.core.course import Course, NoneCourse
    from architecture.code_analysis_v2.core.student import Student
    from architecture.code_analysis_v2.core.subject import Subject
    from architecture.code_analysis_v2.core.gss import GSS
LOGGER = logging.getLogger(__name__)


class Teacher(BaseCoreObject):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._course: Course = NoneCourse()
        self._name: str = name
        self._state: IState = NotWorking()
        self._sub_state: IState = NotFull()
        # TODO Teacher list of subscribed subjects
        self._subjects: list["Subject"] = []

    def subscribe_to(self, subject: "Subject") -> None:
        # TODO 52. Each teacher may teach in 3 subjects at maximum
        # update the internal list of subjects
        # is it possible to unsubscribe from the subject?
        # what happens with the course if no new teacher replaces the old one?
        # how the new teacher gets the information from the old one?
        # what happens with the students subscribed to the subject if no new teacher replaces the old one?
        # The teacher can subscribe to any subject or just the ones of their course?
        # How does the teacher subscribe to a course?
        raise NotImplementedError

    def set_the_grade_of_students_in_their_subject(
        self, grade: int, student: "Student", subject: "Subject"
    ) -> "GSS":
        # rules
        # the student must be in the subject, not locked
        # the subject must be in progress
        # TODO 51. The teacher sets the grade for all students of his/her subjects
        raise NotImplementedError

    def _has_maximum_subjecs(self) -> bool:
        raise NotImplementedError


class NoneTeacher(Teacher):
    def __init__(self, name=""):
        super().__init__(name)


class Working(IState):
    @staticmethod
    def get_next_state(context: Teacher):
        return Working


class NotWorking(IState):
    @staticmethod
    def get_next_state(context: Teacher):
        raise NotImplementedError


class Full(IState):
    # It is a sub-state allowed when the state is Working
    @staticmethod
    def get_next_state(context: Teacher):
        raise NotImplementedError


class NotFull(IState):
    # It is a sub-state allowed when the state is Working
    @staticmethod
    def get_next_state(context: Teacher):
        raise NotImplementedError
