from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject
from architecture.code_analysis_v3.core.common import IState

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.student import IStudent
    from architecture.code_analysis_v3.core.subject import ISubject


class IGSS(AbstractCoreObject):
    def __init__(self, name) -> None:
        self._grade: int
        self._subject: "ISubject"

    def _calculate_subject_state(self) -> int:
        return 0

    def _notify_subject(self, student: "IStudent") -> None:
        pass

    def set_(self, grade: int, subject: "ISubject", student: "IStudent") -> None:
        pass


class NoneGSS(IGSS):
    def __init__(self, name=""):
        super().__init__(name)


class Approved(IState):
    pass


class Failed(IState):
    pass
