from architecture.code_analysis_v3.core.student import IStudent
from architecture.code_analysis_v3.core.course import ICourse
from architecture.code_analysis_v3.core.gss import IGSS, NoneGSS
from architecture.code_analysis_v3.core.subject import ISubject
from architecture.code_analysis_v3.core.common import IState
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject


class AbstractTeacher(AbstractCoreObject):
    def __init__(self, name) -> None:
        self._course: ICourse
        self._sub_state: IState
        self._subjects: list["ISubject"]

    def _has_maximum_subject(self) -> bool:
        return False

    def set_the_grade_of_students_in_their_subject(
        self, grade: int, student: "IStudent", subject: "ISubject"
    ) -> "IGSS":
        return NoneGSS()

    def subscribe_to(self, subject: "ISubject") -> None:
        pass


class NoneTeacher(AbstractTeacher):
    pass


class Full(IState):
    pass


class NotFull(IState):
    pass


class NotWorking(IState):
    pass


class Working(IState):
    pass
