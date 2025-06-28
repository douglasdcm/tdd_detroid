from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject
from architecture.code_analysis_v3.core.common import AbstractState, NoneState

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.student import AbstractStudent
    from architecture.code_analysis_v3.core.subject import AbstractSubject


MESSAGE = "=== No valid course ==="


class AbstractCourse(AbstractCoreObject):
    def __init__(self, name) -> None:
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

    def notify_me_about_subject(self, subject: "AbstractSubject") -> None:
        print(MESSAGE)


class Course(AbstractCourse):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._students: list["AbstractStudent"]
        self._subject: list["AbstractSubject"]
        self._state: "AbstractState" = NotStarted()

    @property
    def state(self) -> "AbstractState":
        return self._state

    @state.setter
    def state(self, value: "AbstractState") -> None:
        pass

    def _has_minium_students(self) -> bool:
        raise NotImplementedError

    def _has_minimum_subjects(self) -> bool:
        raise NotImplementedError

    def notify_me_about_subject(self, subject: "AbstractSubject") -> None:
        raise NotImplementedError

    def list_all_subjects(self) -> list["AbstractSubject"]:
        return []


class NoneCourse(AbstractCourse):
    def __init__(self, name="None"):
        super().__init__(name)


class NotStarted(AbstractState):
    pass


class CourseInProgress(AbstractState):
    pass
