from typing import TYPE_CHECKING
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject, NoneCoreObject
from architecture.code_analysis_v3.core.common import AbstractState, NoneState
from architecture.code_analysis_v3.core.constants import (
    MAXIMUM_STUDENTS_IN_SUBJECT,
    MINIMUM_STUDENTS_IN_SUBJECT,
)
from architecture.code_analysis_v3.core.course import NoneCourse
from architecture.code_analysis_v3.core.exceptions import InvalidCourse

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

    def is_subject(self):
        return True

    def has_maximum_students(self) -> bool:
        raise NotImplementedError

    def has_minimum_inprogress_students(self) -> bool:
        raise NotImplementedError

    def has_teacher(self) -> bool:
        raise NotImplementedError

    def is_inprogress(self) -> bool:
        raise NotImplementedError

    def subscribe_teacher(self, teacher: "AbstractTeacher") -> None:
        raise NotImplementedError

    def subscribe_student(self, student: "AbstractStudent") -> None:
        raise NotImplementedError

    def accept_student(self, student: "AbstractStudent") -> None:
        raise NotImplementedError

    def has_course(self) -> bool:
        raise NotImplementedError

    def list_all_students(self) -> list["AbstractStudent"]:
        raise NotImplementedError

    def list_all_inprogress_students(self) -> list["AbstractStudent"]:
        raise NotImplementedError


class Subject(AbstractSubject):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._course: "AbstractCourse" = NoneCourse()
        self._students: list["AbstractStudent"] = []
        self._subjects: list["AbstractSubject"] = []
        self._teacher: "AbstractCoreObject" = NoneCoreObject()
        self._state: "AbstractState" = SubjectInitialState()

    def __str__(self):
        return f"{self.__class__.__name__} '{self._name}'"

    def __repr__(self):
        return f"{self.__class__.__name__} '{self._name}'"

    def _calculate_state(self) -> None:
        self._state = self._state.get_next_state(self)

    @property
    def course(self) -> "AbstractCourse":
        return self._course

    @course.setter
    def course(self, course: "AbstractCourse") -> None:
        course.is_course()
        if isinstance(self._course, NoneCourse):
            self._course = course
        else:
            raise InvalidCourse("Subject in other course")
        self._calculate_state()
        if self not in course.list_all_subjects():
            course.accept_subject(self)

    @property
    def state(self) -> "AbstractState":
        self._calculate_state()
        return self._state

    def subscribe_teacher(self, teacher: "AbstractTeacher") -> None:
        self._teacher = teacher

    def has_minimum_inprogress_students(self) -> bool:
        return len(self._students) >= MINIMUM_STUDENTS_IN_SUBJECT

    def has_maximum_students(self) -> bool:
        return len(self._students) >= MAXIMUM_STUDENTS_IN_SUBJECT

    def has_teacher(self) -> bool:
        return not isinstance(self._teacher, NoneCoreObject)

    def has_course(self) -> bool:
        return not isinstance(self.course, NoneCourse)

    def is_inprogress(self) -> bool:
        return isinstance(self.state, SubjectInProgress)

    def list_all_students(self) -> list["AbstractStudent"]:
        return self._students

    def list_all_inprogress_students(self) -> list["AbstractStudent"]:
        return [s for s in self._students if s.is_inprogress()]

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
    def get_next_state(self, context: AbstractSubject):
        if (
            context.has_course()
            and context.has_teacher()
            and context.has_minimum_inprogress_students()
        ):
            return SubjectInProgress()
        return self


class SubjectInProgress(AbstractState):
    def get_next_state(self, context: AbstractSubject):
        return self
