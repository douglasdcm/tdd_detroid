from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject, NoneCoreObject
from architecture.code_analysis_v3.core.common import IState

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.student import IStudent
    from architecture.code_analysis_v3.core.teacher import AbstractTeacher
    from architecture.code_analysis_v3.core.course import ICourse


class ISubject(AbstractCoreObject):
    @property
    def course(self) -> "AbstractCoreObject":
        raise NotImplementedError

    @course.setter
    def course(self, value: "AbstractCoreObject") -> None:
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
        self._course: "AbstractCoreObject" = NoneCoreObject()
        self._students: list["IStudent"]
        self._teacher: "AbstractTeacher"

    @property
    def course(self) -> "AbstractCoreObject":
        return self._course

    @course.setter
    def course(self, value: "AbstractCoreObject") -> None:
        self._course = value


class NoneSubject(ISubject):
    def __init__(self, name=""):
        super().__init__(name)


class InProgress(IState):
    pass


class Locked(IState):
    pass
