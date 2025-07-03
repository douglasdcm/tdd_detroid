from core.exceptions import InvalidCourse
from core.custom_logger import none_logger, spy_logger
from core.student import AbstractStudent
from core.course import AbstractCourse, NoneCourse
from core.gss import GSS
from core.subject import AbstractSubject, SubjectInProgress
from core.common import AbstractState, NoneState
from core.base_object import AbstractCoreObject, BasicInformation
from core.constants import MAXIMUM_SUBJECTS_IN_TEACHER


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

    def add_basic_information(self, information: "BasicInformation"):
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
        self._age: int = -1

    @spy_logger
    def _calculate_states(self):
        self._state = self._state.get_next_state(self)
        self._sub_state = self._sub_state.get_next_state(self)

    @property
    def age(self) -> int:
        return self._age

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

    @spy_logger
    def add_basic_information(self, basic_information: "BasicInformation") -> None:
        self._name = basic_information.name
        self._age = basic_information.age

    @spy_logger
    def subscribe_to(self, subject: "AbstractSubject") -> None:
        subject.is_subject()
        if self.has_maximum_subjects():
            raise MaximumSubjectsReached("Teacher reached maximum subjects")
        self._subjects.append(subject)
        self._calculate_states()
        if not subject.has_teacher():
            subject.subscribe_teacher(self)

    @spy_logger
    def has_inprogress_subject(self) -> bool:
        for subject in self._subjects:
            if isinstance(subject.state, SubjectInProgress):
                return True
        return False

    @spy_logger
    def has_maximum_subjects(self):
        inprogress = [s for s in self._subjects if s.is_inprogress()]
        return len(inprogress) >= MAXIMUM_SUBJECTS_IN_TEACHER

    @spy_logger
    def has_course(self):
        return not isinstance(self._course, NoneCourse)

    @spy_logger
    def set_gss(self, grade: int, student: "AbstractStudent", subject: "AbstractSubject") -> None:
        student.is_student()
        subject.is_subject()
        gss = GSS()
        gss.set_(grade, subject, student)

    @spy_logger
    def list_all_subjects(self) -> list["AbstractSubject"]:
        return self._subjects

    @spy_logger
    def list_all_subjects_inprogress(self) -> list["AbstractSubject"]:
        return [s for s in self._subjects if s.is_inprogress()]


class NoneTeacher(AbstractTeacher):
    def __init__(self, name="None"):
        super().__init__(name)

    @property
    def state(self):
        return NoneState()

    @property
    def sub_state(self):
        return NoneState()

    @none_logger
    def has_maximum_subject(self) -> bool:
        return False

    @none_logger
    def set_gss(self, grade: int, student: "AbstractStudent", subject: "AbstractSubject") -> None:
        pass

    @none_logger
    def subscribe_to(self, subject: "AbstractSubject") -> None:
        pass

    @none_logger
    def has_inprogress_subject(self) -> bool:
        return False

    @none_logger
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
