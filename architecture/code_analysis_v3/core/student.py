from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject
from architecture.code_analysis_v3.core.common import IState
from architecture.code_analysis_v3.core.course import NoneCourse

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.gss import IGSS
    from architecture.code_analysis_v3.core.course import ICourse
    from architecture.code_analysis_v3.core.subject import ISubject


class IStudent(AbstractCoreObject):
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

    def has_course(self):
        raise NotImplementedError

    def has_minimum_subjects(self):
        raise NotImplementedError

    def calculate_missing_subjects(self) -> None:
        raise NotImplementedError

    def create_student_with_basic_informtion(self, basic_information: "BasicInformation") -> None:
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

    def has_minimum_grade(self) -> bool:
        raise NotImplementedError

    def are_all_subjects_approved(self) -> bool:
        raise NotImplementedError


class ConcretStudent(IStudent):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._course: "ICourse" = NoneCourse()
        self._gpa: int = 0
        self._grade: int = 0
        self._grades: list[int] = []
        self._missing_subjects: list["ISubject"] = []
        self._subjects: list["ISubject"] = []
        self._state: IState = InitialState()

    def _calculate_gpa(self) -> None:
        raise NotImplementedError

    def _calculate_state(self) -> None:
        self._state = self._state.get_next_state(self)

    def _has_missing_subjects(self) -> bool:
        return False

    @property
    def missing_subjects(self) -> list["ISubject"]:
        return self._missing_subjects

    @property
    def state(self) -> IState:
        return self._state

    @property
    def course(self) -> "ICourse":
        return self._course

    @course.setter
    def course(self, course: "ICourse") -> None:
        if isinstance(self._course, NoneCourse):
            self._course = course
            self._calculate_state()

    def subscribe_to_subject(self, subject):
        if subject.course != self._course:
            raise InvalidSubject("Subject is not in student course")
        self._subjects.append(subject)
        self._calculate_state()

    def notify_me_about_gss(self, gss):
        self._state = InProgress()
        self._missing_subjects = ["", ""]
        self._calculate_state()

    def has_course(self):
        return not isinstance(self._course, NoneCourse)

    def has_minimum_subjects(self):
        return len(self._subjects) >= 3

    def calculate_missing_subjects(self) -> None:
        pass

    def has_minimum_grade(self) -> bool:
        return True

    def are_all_subjects_approved(self) -> bool:
        return True


class NoneStudent(IStudent):
    def __init__(self, name=""):
        super().__init__(name)


class BasicInformation:
    def __init__(self, name, age) -> None:
        self._age: int
        self._name: str


class InvalidSubject(Exception):
    pass


class InvalidStateTransition(Exception):
    pass


class Approved(IState):
    def get_next_state(self, context: IStudent) -> IState:
        raise InvalidStateTransition("Studend is already approved in the course")


class InProgress(IState):
    def get_next_state(self, context: IStudent) -> IState:
        if context.has_minimum_grade() and context.are_all_subjects_approved():
            return Approved()
        return self


class InitialState(IState):
    def get_next_state(self, context: IStudent) -> IState:
        if context.has_course() and context.has_minimum_subjects():
            return InProgress()
        return self
