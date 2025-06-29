from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject
from architecture.code_analysis_v3.core.common import AbstractState, NoneState
from architecture.code_analysis_v3.core.constants import (
    MAXIMUM_STUDENTS_IN_COURSE,
    MAXIMUM_SUBJECTS_IN_COURSE,
    MINIMUM_STUDENTS_IN_COURSE,
    MINIMUN_SUBJECTS_IN_COURSE,
)
from architecture.code_analysis_v3.core.exceptions import InvalidStudent, InvalidSubject

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.student import AbstractStudent
    from architecture.code_analysis_v3.core.subject import AbstractSubject


MESSAGE = "=== No valid course ==="


class AbstractCourse(AbstractCoreObject):
    @property
    def state(self) -> "AbstractState":
        raise NotImplementedError

    def accept_student(self, student: "AbstractStudent") -> None:
        raise NotImplementedError

    def accept_subject(self, subject: "AbstractSubject") -> None:
        raise NotImplementedError

    def list_all_subjects(self) -> list["AbstractSubject"]:
        raise NotImplementedError

    def list_all_subjects_by(self, student: "AbstractStudent") -> list["AbstractStudent"]:
        raise NotImplementedError

    def list_all_students(self) -> list["AbstractStudent"]:
        raise NotImplementedError

    def subject_notify_me_minimun_students(self, subject: "AbstractSubject") -> None:
        raise NotImplementedError

    def has_minimum_inprogress_students(self) -> bool:
        raise NotImplementedError

    def has_minimum_inprogress_subjects(self) -> bool:
        raise NotImplementedError


class Course(AbstractCourse):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._students: list["AbstractStudent"] = []
        self._subjects: list["AbstractSubject"] = []
        self._state: "AbstractState" = CourseNotStarted()

    def _calculate_state(self) -> None:
        self._state = self._state.get_next_state(self)

    @property
    def state(self) -> "AbstractState":
        self._calculate_state()
        return self._state

    def accept_student(self, student: "AbstractStudent"):
        if student in self._students:
            raise InvalidStudent("Student already in course")
        if student.has_course() and self != student.course:
            raise InvalidStudent("Student in other course")
        if self.is_full_of_student():
            raise InvalidStudent("Course already full of students")
        self._students.append(student)
        self._calculate_state()
        if self != student.course:
            student.course = self

    def is_full_of_student(self):
        return len(self._students) >= MAXIMUM_STUDENTS_IN_COURSE

    def accept_subject(self, subject):
        if subject in self._subjects:
            raise InvalidSubject("Subject already in course")
        if subject.has_course() and self != subject.course:
            raise InvalidSubject("Subject in other course")
        if self.is_full_of_subjects():
            raise InvalidSubject("Course already full of subjects")
        self._subjects.append(subject)
        self._calculate_state()
        if self != subject.course:
            subject.course = self

    def is_full_of_subjects(self):
        return len(self._subjects) >= MAXIMUM_SUBJECTS_IN_COURSE

    def has_minimum_inprogress_students(self):
        inprogress = [s for s in self._students if s.is_inprogress()]
        return len(inprogress) >= MINIMUM_STUDENTS_IN_COURSE

    def has_minimum_inprogress_subjects(self):
        return len(self._subjects) >= MINIMUN_SUBJECTS_IN_COURSE

    def list_all_subjects(self) -> list["AbstractSubject"]:
        return self._subjects

    def list_all_students(self) -> list["AbstractStudent"]:
        return self._students


class NoneCourse(AbstractCourse):
    def __init__(self, name="None"):
        super().__init__(name)

    @property
    def state(self) -> "AbstractState":
        return NoneState()

    @state.setter
    def state(self, value: "AbstractState") -> None:
        print(MESSAGE)

    def accept_student(self, student: "AbstractStudent") -> None:
        print(MESSAGE)

    def list_all_subjects(self) -> list["AbstractSubject"]:
        return []

    def list_all_subjects_by(self, student: "AbstractStudent") -> list["AbstractStudent"]:
        return []

    def subject_notify_me_minimun_students(self, subject: "AbstractSubject") -> None:
        print(MESSAGE)


class CourseNotStarted(AbstractState):
    def get_next_state(self, context: AbstractCourse):
        # breakpoint()
        if context.has_minimum_inprogress_students() and context.has_minimum_inprogress_subjects():
            return CourseInProgress()
        return self


class CourseInProgress(AbstractState):
    def get_next_state(self, context: AbstractCourse):
        return self
