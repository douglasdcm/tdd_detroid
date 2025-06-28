from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject, NoneCoreObject
from architecture.code_analysis_v3.core.common import AbstractState, NoneState
from architecture.code_analysis_v3.core.course import NoneCourse

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.student import AbstractStudent
    from architecture.code_analysis_v3.core.teacher import AbstractTeacher
    from architecture.code_analysis_v3.core.course import AbstractCourse

MESSAGE = "=== No valid subject ==="


class AbstractSubject(AbstractCoreObject):
    @property
    def course(self) -> "AbstractCoreObject":
        raise NotImplementedError

    @course.setter
    def course(self, value: "AbstractCoreObject") -> None:
        raise NotImplementedError

    @property
    def state(self) -> "AbstractState":
        raise NotImplementedError

    @state.setter
    def state(self, value: "AbstractState") -> None:
        raise NotImplementedError

    def _has_enrolled_students_over_the_maximum_value(self) -> bool:
        raise NotImplementedError

    def _has_minimum_students(self) -> bool:
        raise NotImplementedError

    def _has_teacher(self) -> bool:
        raise NotImplementedError

    def subscribe_teacher(self, teacher: "AbstractTeacher") -> None:
        raise NotImplementedError

    def subscribe_student(self, student: "AbstractStudent") -> None:
        raise NotImplementedError


class Subject(AbstractSubject):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._course: "AbstractCoreObject" = NoneCoreObject()
        self._students: list["AbstractStudent"]
        self._teacher: "AbstractTeacher"

    def __str__(self):
        return f"{self.__class__.__name__} '{self._name}'"

    def __repr__(self):
        return f"{self.__class__.__name__} '{self._name}'"

    @property
    def course(self) -> "AbstractCoreObject":
        return self._course

    @course.setter
    def course(self, value: "AbstractCoreObject") -> None:
        self._course = value

    @property
    def state(self) -> "AbstractState":
        return SubjectInProgress()

    def _has_enrolled_students_over_the_maximum_value(self) -> bool:
        return False

    def _has_minimum_students(self) -> bool:
        return False

    def _has_teacher(self) -> bool:
        return False


class NoneSubject(AbstractSubject):
    def __init__(self, name="") -> None:
        super().__init__(name)

    @property
    def course(self) -> "AbstractCoreObject":
        return NoneCourse()

    @course.setter
    def course(self, value: "AbstractCoreObject") -> None:
        print(MESSAGE)

    @property
    def state(self) -> "AbstractState":
        return NoneState()

    @state.setter
    def state(self, value: "AbstractState") -> None:
        print(MESSAGE)

    def subscribe_teacher(self, teacher: "AbstractTeacher") -> None:
        print(MESSAGE)

    def subscribe_student(self, student: "AbstractStudent") -> None:
        print(MESSAGE)


class SubjectInProgress(AbstractState):
    pass


class Locked(AbstractState):
    pass
