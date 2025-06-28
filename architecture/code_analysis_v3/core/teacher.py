from architecture.code_analysis_v3.core.student import AbstractStudent
from architecture.code_analysis_v3.core.course import AbstractCourse, CourseInProgress, NoneCourse
from architecture.code_analysis_v3.core.gss import IGSS, GSS, NoneGSS
from architecture.code_analysis_v3.core.subject import AbstractSubject, SubjectInProgress
from architecture.code_analysis_v3.core.common import AbstractState, NoneState
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject
from architecture.code_analysis_v3.core.constants import MAXIMUM_TEACHER_SUBJECTS

MESSAGE = "=== No valid teacher ==="


class MaximumSubjectsReached(Exception):
    pass


class AbstractTeacher(AbstractCoreObject):
    def __init__(self, name) -> None:
        super().__init__(name)

    @property
    def state(self):
        raise NotImplementedError

    @property
    def sub_state(self):
        raise NotImplementedError

    def has_maximum_subjects(self) -> bool:
        raise NotImplementedError

    def set_gss(self, grade: int, student: "AbstractStudent", subject: "AbstractSubject") -> None:
        raise NotImplementedError

    def subscribe_to(self, subject: "AbstractSubject") -> None:
        raise NotImplementedError

    def has_inprogress_subject(self) -> bool:
        raise NotImplementedError


class Teacher(AbstractTeacher):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._course: AbstractCourse = NoneCourse()
        self._state: AbstractState = TeacherNotWorking()
        self._sub_state: AbstractState = TeacherNotFull()
        self._subjects: list["AbstractSubject"] = []

    def __str__(self):
        return f"{self._name}"

    def __repr__(self):
        return f"{self._name}"

    def _calculate_states(self):
        self._state = self._state.get_next_state(self)
        self._sub_state = self._sub_state.get_next_state(self)

    @property
    def state(self):
        self._calculate_states()
        return self._state

    @property
    def sub_state(self):
        self._calculate_states()
        return self._sub_state

    def subscribe_to(self, subject: "AbstractSubject") -> None:
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
        return len(self._subjects) >= MAXIMUM_TEACHER_SUBJECTS

    def set_gss(self, grade: int, student: "AbstractStudent", subject: "AbstractSubject") -> None:
        gss = GSS()
        gss.set_(grade, subject, student)
        student.notify_me_about_gss(gss)


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
        # breakpoint()
        if context.has_inprogress_subject():
            return TeacherWorking()
        return self


class TeacherWorking(AbstractState):
    def get_next_state(self, context: AbstractTeacher):
        if not context.has_inprogress_subject():
            return TeacherNotWorking()
        return self
