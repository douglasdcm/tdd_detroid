from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject
from architecture.code_analysis_v3.core.common import IState
from architecture.code_analysis_v3.core.course import NoneCourse

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.student import IStudent
    from architecture.code_analysis_v3.core.teacher import AbstractTeacher
    from architecture.code_analysis_v3.core.course import ICourse


class ISubject(AbstractCoreObject):
    @property
    def course(self) -> "ICourse":
        raise NotImplementedError

    @course.setter
    def course(self, value: "ICourse") -> None:
        raise NotImplementedError

    def _has_enrolled_students_over_the_maximum_value(self) -> bool:
        return False

    def _has_minimum_students(self) -> bool:
        return False

    def _has_teacher(self) -> bool:
        return False

    def add_to_course(self, course: "ICourse") -> None:
        pass

    def subscribe_teacher(self, teacher: "AbstractTeacher") -> None:
        pass

    def subscribe_student(self, student: "IStudent") -> None:
        pass


class ConcreteSubject(ISubject):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._course: "ICourse" = NoneCourse()
        self._students: list["IStudent"]
        self._teacher: "AbstractTeacher"

    @property
    def course(self) -> "ICourse":
        return self._course

    @course.setter
    def course(self, value: "ICourse") -> None:
        self._course = value


class NoneSubject(ISubject):
    def __init__(self, name=""):
        super().__init__(name)


class InProgress(IState):
    pass


class Locked(IState):
    pass
