import logging
from typing import TYPE_CHECKING
from core.exceptions import InvalidStateTransitionError
from core.common import IState

if TYPE_CHECKING:
    from subject import Subject
    from course import Course

LOGGER = logging.getLogger(__name__)




class StudentGrade:
    def __init__(self):
        self.student = None
        self.subject = None
        self.grade = None


class Student:
    is_not_enrolled_in_maximum_Subject: None
    enrolled_in_maximum_Subject: None
    approved: None
    reproved_failed: None
    enrolled: None
    not_enrolled: None
    does_not_have_missing_Subjects: None
    has_maximum_Semester: None
    does_not_have_maximum_Semeter: None

    def __init__(self, name):
        self._course :"Course"= None
        self._state = InProgress
        self.grades = []
        self._grade = 0
        self._subjects = []
        self._name = name

    def __str__(self):
        return f"'{self._name}'"

    @property
    def subjects(self):
        return self._subjects

    @property
    def course(self):
        return self._course

    @course.setter
    def course(self, value:"Course"):
        if self._course:
            return
        value.accept_student(self)
        self._course = value

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        self._grade = value
        self._state = self.state.get_next_state(self)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: IState):
        self._state = value.get_next_state(self)

    def subscribe_subject(self, subject: "Subject"):
        subject.subscribe_student(self)
        self._subjects.append(subject)
        LOGGER.info(f"{self} added to {subject}")

    def has_missing_subjects(self):
        # To be implemented
        return False

    def update_Grades(self, subject: "Subject", grade):
        student_grade = StudentGrade()
        student_grade.student = self
        student_grade.grade = grade
        student_grade.subject = subject
        self.grades.append(student_grade)

    def create_Student():
        pass

    def list_all_their_Subjects_by_Course(self):
        self.course.list_subjects_by(self)

    def list_all_taken_Subjects(self):
        # It is not clear the purpose of the method
        self.course.list_all_subjects_by(self)

    def take_Subject():  # (do not take) ... ?
        # it is not clear if this method is necessary
        pass

    def list_missing_Subjects(self):
        subject_by_student = set(self.course.list_subjects_by(self))
        all_subjects = set(self.course.list_all_subjects(self))
        return list(all_subjects.difference(subject_by_student))

    def authenticate():
        pass


class StudentSituation:
    pass


class StudentDocumentation:
    pass


class StudentCredential:
    pass


class StudentHistory:
    pass



class Approved(IState):
    def get_next_state(context):
        raise InvalidStateTransitionError(f"{context.state} to {Approved}")


class InProgress(IState):
    def get_next_state(context: Student):
        if context.state == Approved:
            raise InvalidStateTransitionError(f"{context.state} to {InProgress}")
        if all([context.grade >= 7, not context.has_missing_subjects()]):
            return Approved
        return InProgress


class Locked(IState):
    def get_next_state(context: Student):
        if context.state == Approved:
            raise InvalidStateTransitionError(f"{context.state} to {Locked}")
        return Locked