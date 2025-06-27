from statistics import mean
from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject, NoneCoreObject
from architecture.code_analysis_v3.core.common import IState
from architecture.code_analysis_v3.core.constants import MINIMUM_GRADE, MINIMUN_SUBJECTS
from architecture.code_analysis_v3.core.course import NoneCourse
from architecture.code_analysis_v3.core.gss import GSSApproved
from architecture.code_analysis_v3.core.subject import NoneSubject

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.gss import IGSS
    from architecture.code_analysis_v3.core.course import ICourse
    from architecture.code_analysis_v3.core.subject import ISubject


class IStudent(AbstractCoreObject):
    @property
    def subjects_in_progress(self) -> list["ISubject"]:
        raise NotImplementedError

    @property
    def missing_subjects(self) -> list["ISubject"]:
        raise NotImplementedError

    @property
    def state(self) -> IState:
        raise NotImplementedError

    @property
    def course(self) -> "ICourse":
        raise NotImplementedError

    @course.setter
    def course(self, course: "ICourse") -> None:
        raise NotImplementedError

    @property
    def age(self) -> int:
        raise NotImplementedError

    def add_basic_information(self, basic_information: "BasicInformation") -> None:
        raise NotImplementedError

    def list_all_subscribed_subjects(self) -> list["ISubject"]:
        raise NotImplementedError

    def list_all_their_subjects_by_course(self) -> list["ISubject"]:
        raise NotImplementedError

    def list_missing_subjects(self) -> list["ISubject"]:
        raise NotImplementedError

    def notify_me_about_gss(self, gss: "IGSS") -> None:
        raise NotImplementedError

    def notify_me_about_course(self, course: "ICourse") -> None:
        raise NotImplementedError

    def subscribe_to_subject(self, subject: "ISubject") -> None:
        raise NotImplementedError

    def has_minimum_gpa(self) -> bool:
        raise NotImplementedError

    def are_all_subjects_approved(self) -> bool:
        raise NotImplementedError

    def has_course(self):
        raise NotImplementedError

    def has_minimum_subjects(self):
        raise NotImplementedError


class ConcretStudent(IStudent):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._course: "ICourse" = NoneCourse()
        self._gpa: int = 0
        self._grades: list[int] = []
        self._missing_subjects: list["ISubject"] = []
        self._subjects_in_progress: list["ISubject"] = []
        self._subjects_in_progress_internal_copy: list["ISubject"] = []
        self._grades_subjects_approved: list[int] = []
        self._state: IState = InitialState()

    def _calculate_gpa(self) -> None:
        self._gpa = int(mean(self._grades_subjects_approved))

    def _calculate_state(self) -> None:
        self._state = self._state.get_next_state(self)

    def _add_to_subject_lists(self, subject: "ISubject") -> None:
        self._subjects_in_progress.append(subject)
        self._subjects_in_progress_internal_copy.append(subject)
        self._missing_subjects.append(subject)

    def _remove_from_subject_lists(self, subject: "ISubject") -> None:
        self._subjects_in_progress_internal_copy.remove(subject)
        self._missing_subjects.remove(subject)
        # Clear the list of subjects in progress when all subject's
        # state (Approved, Failed) set
        # It is necessary because the user indireclty  uses the variable
        # _subjects_in_progress_internal_copy, so it can not be update on the fly
        if not self._subjects_in_progress_internal_copy:
            self._subjects_in_progress.clear()

    @property
    def subjects_in_progress(self) -> list["ISubject"]:
        return self._subjects_in_progress

    @property
    def missing_subjects(self) -> list["ISubject"]:
        return self._missing_subjects

    @property
    def state(self) -> IState:
        return self._state

    @property
    def age(self) -> int:
        return self._age

    @property
    def course(self) -> "ICourse":
        return self._course

    @course.setter
    def course(self, course: "ICourse") -> None:
        self._course = course
        self._missing_subjects = course.list_all_subjects()
        self._calculate_state()

    def has_course(self):
        return not isinstance(self._course, NoneCourse)

    def has_minimum_subjects(self):
        return len(self._subjects_in_progress) >= MINIMUN_SUBJECTS

    def has_minimum_gpa(self) -> bool:
        return self._gpa >= MINIMUM_GRADE

    def are_all_subjects_approved(self) -> bool:
        return len(self._missing_subjects) == 0

    def subscribe_to_subject(self, subject):
        if subject.course != self._course:
            raise InvalidSubject("Subject is not in student course")
        self._add_to_subject_lists(subject)
        self._calculate_state()

    def notify_me_about_gss(self, gss):
        if gss.student != self:
            raise InvalidStudent("Student reported is not the current one")
        if gss.subject not in self._subjects_in_progress:
            raise InvalidSubject("Subject reported is not in student list")
        if isinstance(gss.state, GSSApproved):
            self._remove_from_subject_lists(gss.subject)
            self._grades_subjects_approved.append(gss.grade)
            self._calculate_gpa()
        self._calculate_state()

    def add_basic_information(self, basic_information: "BasicInformation") -> None:
        self._name = basic_information.name
        self._age = basic_information.age


class NoneStudent(IStudent):
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


class Approved(IState):
    def get_next_state(self, context: IStudent) -> IState:
        raise InvalidStateTransition("Studend is already approved in the course")


class InProgress(IState):
    def get_next_state(self, context: IStudent) -> IState:
        if context.has_minimum_gpa() and context.are_all_subjects_approved():
            return Approved()
        return self


class InitialState(IState):
    def get_next_state(self, context: IStudent) -> IState:
        if context.has_course() and context.has_minimum_subjects():
            return InProgress()
        return self
