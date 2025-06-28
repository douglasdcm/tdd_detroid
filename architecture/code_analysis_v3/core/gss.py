from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject, NoneCoreObject
from architecture.code_analysis_v3.core.common import AbstractState
from architecture.code_analysis_v3.core.constants import MINIMUM_STUDENT_GRADE

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.student import AbstractStudent
    from architecture.code_analysis_v3.core.subject import AbstractSubject


class IGSS(AbstractCoreObject):
    @property
    def state(self) -> "AbstractState":
        raise NotImplementedError

    @property
    def student(self) -> "AbstractCoreObject":
        raise NotImplementedError

    @property
    def subject(self) -> "AbstractCoreObject":
        raise NotImplementedError

    @property
    def grade(self) -> int:
        raise NotImplementedError

    def set_(self, grade: int, subject: "AbstractSubject", student: "AbstractStudent") -> None:
        raise NotImplementedError


class GSS(IGSS):
    def __init__(self, name="") -> None:
        self._grade: int = 0
        self._subject: "AbstractCoreObject" = NoneCoreObject()
        self._student: "AbstractCoreObject" = NoneCoreObject()
        self._state: "AbstractState" = InitialState()
        name = f"{self._subject.name}_{self._student.name}_{str(self._grade)}"
        super().__init__(name)

    def _notify_subject(self, student: "AbstractStudent") -> None:
        pass

    def _calculate_state(self):
        self._state = self._state.get_next_state(self)

    @property
    def state(self) -> "AbstractState":
        return self._state

    @property
    def student(self) -> "AbstractCoreObject":
        return self._student

    @property
    def subject(self) -> "AbstractCoreObject":
        return self._subject

    @property
    def grade(self) -> int:
        return self._grade

    def set_(self, grade, subject, student):
        self._grade = grade
        self._subject = subject
        self._student = student
        self._calculate_state()


class NoneGSS(IGSS):
    def __init__(self, name=""):
        super().__init__(name)


class GSSApproved(AbstractState):
    def get_next_state(self, context: GSS):
        return self


class GSSFailed(AbstractState):
    def get_next_state(self, context: GSS):
        return self


class InitialState(AbstractState):
    def get_next_state(self, context: IGSS):
        if context.grade >= MINIMUM_STUDENT_GRADE:
            return GSSApproved()
        return GSSFailed()
