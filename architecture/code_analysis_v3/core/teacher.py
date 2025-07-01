from core.exceptions import InvalidCourse
from core.student import AbstractStudent
from core.course import AbstractCourse, NoneCourse
from core.gss import GSS
from core.subject import AbstractSubject, SubjectInProgress
from core.common import AbstractState, NoneState
from core.base_object import AbstractCoreObject
from core.constants import MAXIMUM_SUBJECTS_IN_TEACHER

MESSAGE = "=== No valid teacher ==="


class MaximumSubjectsReached(Exception):
    pass


class AbstractTeacher(AbstractCoreObject):
    @property
    def state(self):
        raise NotImplementedError

    @property
    def sub_state(self):
        raise NotImplementedError

    @property
    def course(self):
        raise NotImplementedError

    @course.setter
    def course(self, value: "AbstractCourse") -> "AbstractCourse":
        raise NotImplementedError

    def is_teacher(self):
        return True

    def has_maximum_subjects(self) -> bool:
        raise NotImplementedError

    def set_gss(self, grade: int, student: "AbstractStudent", subject: "AbstractSubject") -> None:
        raise NotImplementedError

    def subscribe_to(self, subject: "AbstractSubject") -> None:
        raise NotImplementedError

    def has_inprogress_subject(self) -> bool:
        raise NotImplementedError

    def has_course(self) -> bool:
        raise NotImplementedError

    def list_all_subjects(self) -> list["AbstractSubject"]:
        raise NotImplementedError

    def list_all_subjects_inprogress(self) -> list["AbstractSubject"]:
        raise NotImplementedError


class Teacher(AbstractTeacher):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._course: AbstractCourse = NoneCourse()
        self._state: AbstractState = TeacherNotWorking()
        self._sub_state: AbstractState = TeacherNotFull()
        self._subjects: list["AbstractSubject"] = []

    def _calculate_states(self):
        self._state = self._state.get_next_state(self)
        self._sub_state = self._sub_state.get_next_state(self)

    @property
    def course(self):
        return self._course

    @course.setter
    def course(self, value):
        if self.has_course():
            raise InvalidCourse("Teacher already in other course")
        self._course = value

    @property
    def state(self):
        self._calculate_states()
        return self._state

    @property
    def sub_state(self):
        self._calculate_states()
        return self._sub_state

    def subscribe_to(self, subject: "AbstractSubject") -> None:
        subject.is_subject()
        if self.has_maximum_subjects():
            raise MaximumSubjectsReached("Teacher reached maximum subjects")
        self._subjects.append(subject)
        self._calculate_states()

    def has_inprogress_subject(self) -> bool:
        for subject in self._subjects:
            if isinstance(subject.state, SubjectInProgress):
                return True
        return False

    def has_maximum_subjects(self):
        inprogress = [s for s in self._subjects if s.is_inprogress()]
        return len(inprogress) >= MAXIMUM_SUBJECTS_IN_TEACHER

    def has_course(self):
        return not isinstance(self._course, NoneCourse)

    def set_gss(self, grade: int, student: "AbstractStudent", subject: "AbstractSubject") -> None:
        student.is_student()
        subject.is_subject()
        gss = GSS()
        gss.set_(grade, subject, student)

    def list_all_subjects(self) -> list["AbstractSubject"]:
        return self._subjects

    def list_all_subjects_inprogress(self) -> list["AbstractSubject"]:
        return [s for s in self._subjects if s.is_inprogress()]


class NoneTeacher(AbstractTeacher):
    def __init__(self, name):
        super().__init__(name="None")

    @property
    def state(self):
        return NoneState()

    @property
    def sub_state(self):
        return NoneState()

    def has_maximum_subject(self) -> bool:
        return False

    def set_gss(self, grade: int, student: "AbstractStudent", subject: "AbstractSubject") -> None:
        print(MESSAGE)

    def subscribe_to(self, subject: "AbstractSubject") -> None:
        print(MESSAGE)

    def has_inprogress_subject(self) -> bool:
        return False

    def has_maximum_subjects(self) -> bool:
        return False


class TeacherFull(AbstractState):
    def get_next_state(self, context: AbstractTeacher):
        if context.has_maximum_subjects():
            return self
        return TeacherNotFull()


class TeacherNotFull(AbstractState):
    def get_next_state(self, context: AbstractTeacher):
        if not context.has_maximum_subjects():
            return self
        return TeacherFull()


class TeacherNotWorking(AbstractState):
    def get_next_state(self, context: AbstractTeacher):
        if context.has_inprogress_subject() or context.has_maximum_subjects():
            return TeacherWorking()
        return self


class TeacherWorking(AbstractState):
    def get_next_state(self, context: AbstractTeacher):
        if not context.has_inprogress_subject():
            return TeacherNotWorking()
        return self
