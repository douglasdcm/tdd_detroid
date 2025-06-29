import logging
from typing import TYPE_CHECKING
from architecture.code_analysis.core.common import IState
if TYPE_CHECKING:
    from architecture.code_analysis.core.course import Course
    from architecture.code_analysis.core.student import Student
    from architecture.code_analysis.core.subject import Subject
    from architecture.code_analysis.core.gss import GSS
LOGGER = logging.getLogger(__name__)


class Teacher:
    def __init__(self, name):
        self._course :"Course" = None
        self._name :str= name
        self._state: IState = NotWorking
        self._sub_state: IState = NotFull
        # TODO Teacher list of subscribed subjects
        self._subjects :list["Subject"]= []

    def __str__(self):
        return f"'{self._name}'"

    def subscribe_to(self, subject: "Subject")-> None:
        # TODO 52. Each teacher may teach in 3 subjects at maximum
        # update the internal list of subjects
        # is it possible to unsubscribe from the subject?
        # what happens with the course if no new teacher replaces the old one?
        # how the new teacher gets the information from the old one?
        # what happens with the students subscribed to the subject if no new teacher replaces the old one?
        # The teacher can subscribe to any subject or just the ones of their course?
        # How does the teacher subscribe to a course?
        LOGGER.info(f"{self} added to {subject}")
        subject.subcribe_teacher(self)

    def set_the_grade_of_students_in_their_subject(self, grade: int, student:"Student", subject:"Subject") -> "GSS":
        # rules
        # the student must be in the subject, not locked
        # the subject must be in progress
        # TODO 51. The teacher sets the grade for all students of his/her subjects
        pass

    def has_maximum_subjecs():
        pass


class Working(IState):
    def get_next_state(context: Teacher):
        return Working


class NotWorking(IState):
    def get_next_state(context: Teacher):
        return NotWorking


class Full(IState):
    # It is a sub-state allowed when the state is Working
    def get_next_state(context: Teacher):
        return Full


class NotFull(IState):
    # It is a sub-state allowed when the state is Working
    def get_next_state(context: Teacher):
        return NotFull
