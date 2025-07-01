from statistics import mean
from typing import TYPE_CHECKING
from core.base_object import AbstractCoreObject
from core.common import AbstractState
from core.constants import (
    MINIMUM_STUDENT_GRADE,
    MINIMUN_SUBJECTS_IN_STUDENT,
)
from core.course import NoneCourse
from core.gss import GSSApproved

if TYPE_CHECKING:
    from core.gss import IGSS
    from core.course import AbstractCourse
    from core.subject import AbstractSubject

MESSAGE = "=== No valid student ==="


class AbstractStudent(AbstractCoreObject):
    @property
    def subjects_in_progress(self) -> list["AbstractSubject"]:
        raise NotImplementedError

    @property
    def missing_subjects(self) -> list["AbstractSubject"]:
        raise NotImplementedError

    @property
    def state(self) -> AbstractState:
        raise NotImplementedError

    @property
    def course(self) -> "AbstractCourse":
        raise NotImplementedError

    @course.setter
    def course(self, course: "AbstractCourse") -> None:
        raise NotImplementedError

    @property
    def age(self) -> int:
        raise NotImplementedError

    @property
    def gpa(self) -> int:
        raise NotImplementedError

    def is_student(self):
        return True

    def add_basic_information(self, basic_information: "BasicInformation") -> None:
        raise NotImplementedError

    def list_all_subscribed_subjects(self) -> list["AbstractSubject"]:
        raise NotImplementedError

    def list_missing_subjects(self) -> list["AbstractSubject"]:
        raise NotImplementedError

    def list_all_subjects(self) -> list["AbstractSubject"]:
        raise NotImplementedError

    def notify_me_about_gss(self, gss: "IGSS") -> None:
        raise NotImplementedError

    def notify_me_about_course(self, course: "AbstractCourse") -> None:
        raise NotImplementedError

    def subscribe_to_subject(self, subject: "AbstractSubject") -> None:
        raise NotImplementedError

    def has_minimum_gpa(self) -> bool:
        raise NotImplementedError

    def are_all_subjects_approved(self) -> bool:
        raise NotImplementedError

    def has_course(self):
        raise NotImplementedError

    def has_minimum_subjects(self):
        raise NotImplementedError

    def is_inprogress(self) -> bool:
        raise NotImplementedError


class Student(AbstractStudent):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._course: "AbstractCourse" = NoneCourse()
        self._gpa: int = 0
        self._missing_subjects: list["AbstractSubject"] = []
        self._subjects_in_progress: list["AbstractSubject"] = []
        self._subjects_in_progress_internal_copy: list["AbstractSubject"] = []
        self._grades_subjects: list[int] = []
        self._state: AbstractState = StudentInitialState()
        self._age: int = -1

    def __str__(self):
        return f"Name: '{self.name}', Age: {self.age}"

    def _calculate_gpa(self) -> None:
        if self._grades_subjects:
            self._gpa = int(mean(self._grades_subjects))

    def _calculate_state(self) -> None:
        self._state = self._state.get_next_state(self)

    def _add_to_subject_lists(self, subject: "AbstractSubject") -> None:
        self._subjects_in_progress.append(subject)
        self._subjects_in_progress_internal_copy.append(subject)
        self._missing_subjects.append(subject)
        if self not in subject.list_all_students():
            subject.accept_student(self)

    def _remove_from_subject_lists(self, subject: "AbstractSubject") -> None:
        self._subjects_in_progress_internal_copy.remove(subject)
        self._missing_subjects.remove(subject)
        # Clear the list of subjects in progress when all subject's
        # state (Approved, Failed) set
        # It is necessary because the user indireclty  uses the variable
        # _subjects_in_progress_internal_copy, so it can not be updated on the fly
        if not self._subjects_in_progress_internal_copy:
            self._subjects_in_progress.clear()

    @property
    def subjects_in_progress(self) -> list["AbstractSubject"]:
        return self._subjects_in_progress

    @property
    def missing_subjects(self) -> list["AbstractSubject"]:
        return self._missing_subjects

    @property
    def state(self) -> AbstractState:
        self._calculate_state()
        return self._state

    @property
    def gpa(self) -> int:
        self._calculate_gpa()
        return self._gpa

    @property
    def age(self) -> int:
        return self._age

    @property
    def course(self) -> "AbstractCourse":
        return self._course

    @course.setter
    def course(self, course: "AbstractCourse") -> None:
        self._course = course
        self._missing_subjects = course.list_all_subjects()
        self._calculate_state()
        if self not in course.list_all_students():
            course.accept_student(self)

    @property
    def grades(self) -> list[int]:
        return self._grades_subjects

    def is_inprogress(self) -> bool:
        return isinstance(self._state, StudentInProgress)

    def has_course(self):
        return not isinstance(self._course, NoneCourse)

    def has_minimum_subjects(self):
        return len(self._subjects_in_progress) >= MINIMUN_SUBJECTS_IN_STUDENT

    def has_minimum_gpa(self) -> bool:
        return self._gpa >= MINIMUM_STUDENT_GRADE

    def are_all_subjects_approved(self) -> bool:
        return len(self._missing_subjects) == 0

    def subscribe_to_subject(self, subject):
        subject.is_subject()
        if subject.course != self._course:
            raise InvalidSubject("Subject is not in student course")
        self._add_to_subject_lists(subject)
        self._calculate_state()

    def notify_me_about_gss(self, gss):
        gss.is_gss()
        if isinstance(gss.state, GSSApproved):
            self._remove_from_subject_lists(gss.subject)
        self._grades_subjects.append(gss.grade)
        self._calculate_gpa()
        self._calculate_state()

    def add_basic_information(self, basic_information: "BasicInformation") -> None:
        self._name = basic_information.name
        self._age = basic_information.age

    def list_all_subjects(self) -> list["AbstractSubject"]:
        result = []
        result.extend(self.missing_subjects)
        result.extend(self.subjects_in_progress)
        return result


class NoneStudent(AbstractStudent):
    def __init__(self, name=""):
        super().__init__(name)


class BasicInformation:
    def __init__(self, name, age) -> None:
        self._name: str = name
        self._age: int = age

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age


class InvalidSubject(Exception):
    pass


class InvalidStateTransition(Exception):
    pass


class InvalidStudent(Exception):
    pass


class StudentApproved(AbstractState):
    def get_next_state(self, context: AbstractStudent) -> AbstractState:
        raise InvalidStateTransition("Studend is already approved in the course")


class StudentInProgress(AbstractState):
    def get_next_state(self, context: AbstractStudent) -> AbstractState:
        if context.has_minimum_gpa() and context.are_all_subjects_approved():
            return StudentApproved()
        return self


class StudentInitialState(AbstractState):
    def get_next_state(self, context: AbstractStudent) -> AbstractState:
        if context.has_course() and context.has_minimum_subjects():
            return StudentInProgress()
        return self
