from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject
from architecture.code_analysis_v3.core.common import IState

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.student import IStudent
    from architecture.code_analysis_v3.core.subject import ISubject


class ICourse(AbstractCoreObject):
    def __init__(self, name) -> None:
        super().__init__(name)

    @property
    def state(self) -> "IState":
        raise NotImplementedError

    @state.setter
    def state(self, value: "IState") -> None:
        raise NotImplementedError

    def accept_student(self, student: "IStudent") -> None:
        raise NotImplementedError

    def list_all_subjects(self) -> list["ISubject"]:
        raise NotImplementedError

    def list_all_subjects_by(self, student: "IStudent") -> list["IStudent"]:
        raise NotImplementedError

    def subject_notify_me_minimun_students(self, subject: "ISubject") -> None:
        raise NotImplementedError


class ConcreteCourse(ICourse):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._students: list["IStudent"]
        self._subject: list["ISubject"]
        self._state: "IState" = NotStarted()

    @property
    def state(self) -> "IState":
        return self._state

    @state.setter
    def state(self, value: "IState") -> None:
        if isinstance(value, Cancelled):
            self._state = Cancelled()

    def _has_minium_students(self) -> bool:
        raise NotImplementedError

    def _has_minimum_subjects(self) -> bool:
        raise NotImplementedError


class NoneCourse(ICourse):
    def __init__(self, name=""):
        super().__init__(name)


class Cancelled(IState):
    pass


class NotStarted(IState):
    pass


class InProgress(IState):
    pass
