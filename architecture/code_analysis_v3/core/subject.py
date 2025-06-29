from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject
from architecture.code_analysis_v3.core.common import AbstractState, NoneState
from architecture.code_analysis_v3.core.course import NoneCourse

if TYPE_CHECKING:
    from architecture.code_analysis_v3.core.student import AbstractStudent
    from architecture.code_analysis_v3.core.teacher import AbstractTeacher
    from architecture.code_analysis_v3.core.course import AbstractCourse

MESSAGE = "=== No valid subject ==="


class AbstractSubject(AbstractCoreObject):
    @property
    def course(self) -> "AbstractCourse":
        raise NotImplementedError

    @course.setter
    def course(self, value: "AbstractCourse") -> None:
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

    def is_inprogress(self) -> bool:
        raise NotImplementedError

    def subscribe_teacher(self, teacher: "AbstractTeacher") -> None:
        raise NotImplementedError

    def subscribe_student(self, student: "AbstractStudent") -> None:
        raise NotImplementedError

    def list_all_students(self) -> list["AbstractSubject"]:
        raise NotImplementedError

    def accept_student(self, student: "AbstractStudent") -> None:
        raise NotImplementedError


class Subject(AbstractSubject):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._course: "AbstractCourse" = NoneCourse()
        self._students: list["AbstractStudent"] = []
        self._subjects: list["AbstractSubject"] = []
        self._teacher: "AbstractTeacher"
        self._state: "AbstractState" = SubjectInitialState()

    def __str__(self):
        return f"{self.__class__.__name__} '{self._name}'"

    def __repr__(self):
        return f"{self.__class__.__name__} '{self._name}'"

    def _calculate_state(self) -> None:
        self._state = self._state.get_next_state(self)

    def _has_enrolled_students_over_the_maximum_value(self) -> bool:
        return False

    def _has_minimum_students(self) -> bool:
        return False

    def _has_teacher(self) -> bool:
        return False

    @property
    def course(self) -> "AbstractCourse":
        return self._course

    @course.setter
    def course(self, value: "AbstractCourse") -> None:
        self._course = value
        self._calculate_state()
        if self not in value.list_all_subjects():
            value.accept_subject(self)

    @property
    def state(self) -> "AbstractState":
        self._calculate_state()
        return self._state

    def is_inprogress(self) -> bool:
        return True

    def list_all_students(self) -> list["AbstractSubject"]:
        return self._subjects

    def accept_student(self, student: "AbstractStudent") -> None:
        self._students.append(student)


class NoneSubject(AbstractSubject):
    def __init__(self, name="") -> None:
        super().__init__(name)

    @property
    def course(self) -> "AbstractCourse":
        return NoneCourse()

    @course.setter
    def course(self, value: "AbstractCourse") -> None:
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


class SubjectInitialState(AbstractState):
    def get_next_state(self, context: AbstractState):
        return SubjectInProgress()


class SubjectInProgress(AbstractState):
    def get_next_state(self, context: AbstractState):
        return self
