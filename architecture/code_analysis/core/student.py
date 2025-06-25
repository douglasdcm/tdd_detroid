import logging
from typing import TYPE_CHECKING

from architecture.code_analysis.core.exceptions import InvalidStateTransitionError
from architecture.code_analysis.core.common import IState

if TYPE_CHECKING:
    from architecture.code_analysis.core.gss import GSS
    from architecture.code_analysis.core.subject import Subject
    from architecture.code_analysis.core.course import Course

LOGGER = logging.getLogger(__name__)


class BasicInformation:
    def __init__(self):
        name:str = None
        age:int=None

class Student:
    def __init__(self, name):
        self._course: Course = None
        self._state: IState = InProgress
        self._grades : list[int]= []
        # TODO 12. The maximum grade for a student in a subject is 10.
        # TODO 13. The minimum grade for a student in a subject is 0.
        self._grade:int = 0
        self._subjects :list["Subject"]= []
        # TODO all subjects of the course minus the ones finished
        self._missing_subjects :list["Subject"]= []
        # 17. Students must have names.
        self._name :str= name
        # 1. Each student will have a grade control called "grade point average" (GPA).
        self._gpa :int= 0
        # 6. Subjects in each course may have the same names but will be differentiated by a unique identifier (niu).
        self._niu :int= self.__hash__()

    def __str__(self):
        return f"{self._niu} '{self._name}'"

    @property
    def subjects(self)-> list["Subject"]:
        return self._subjects

    @property
    def course(self)-> "Course":
        return self._course

    @course.setter
    def course(self, value: "Course")->None:
        # 23. The student can only enroll in one course.
        if self._course:
            return
        value.accept_student(self)
        self._course = value

    @property
    def grade(self)->int:
        return self._grade

    @grade.setter
    def grade(self, value:int)->None:
        # it should be private
        self._grade = value
        self._state = self.state.get_next_state(self)
        # TODO 14. The student can lock the course, and in this case, they cannot update their grades or the subjects taken.
        # TODO 20. Students can only update their grades in the subjects they are enrolled in.

    @property
    def state(self)->IState:
        return self._state

    @state.setter
    def state(self, value: IState)->None:
        self._state = value.get_next_state(self)

    def _calculate_gpa(self)->None:
        # TODO 2. The GPA is the average of the student's grades in the ~~courses~~ subjects already taken.
        # calculated when new grade notified
        pass

    def _calculate_missing_subjects(self)->None:
        # TODO update the list of missing subjects when notified about the subject state 'Approved'
        pass

    def notify_about_subject(self, gss: "GSS", grade: int) -> None:
        # Entrypoint to notify the state, grade (and other data) of a subject
        # used to update the missing_subjects and the GPA
        pass

    def subscribe_subject(self, subject: "Subject")->None:
        # TODO 14. The student can lock the course, and in this case, they cannot update their grades or the subjects taken.
        # TODO 30. The student must enroll in a minimum of 3 subjects.
        # what happens if enrolled in less than 10? what is the state? Are operations is restricted?
        subject.subscribe_student(self)
        self._subjects.append(subject)
        LOGGER.info(f"{self} added to {subject}")

    def has_missing_subjects(self)->bool:
        # TODO 31. If the number of subjects missing for a student is less than 3, they can enroll in 1 subject.
        # TODO To be implemented
        return False

    def create_student_with_basic_information(self, basic_information: BasicInformation)->None:
        # TODO 36. The student (person) must be able to create students with basic information.
        # Is it possible to create more then one? Shouldn't be responsibility of the admin to create and the person adds more data?
        pass

    def list_all_their_subjects_by_course(self)-> list["Subject"]:
        # TODO 43. The students must be able to list all subjects only from their course.
        # need to test
        # which data is necessary to show about the subject?
        self.course.list_subjects_by(self)

    def list_all_subcribed_subjects(self)-> list["Subject"]:
        # TODO 44. The students must be able to list all subjects they have taken.
        # 'taken' was replaced by 'subcribed' to be consistent with other requirements
        # It is not clear the purpose of the method
        self.course.list_all_subjects_by(self)

    def list_missing_subjects(self)-> list["Subject"]:
        # TODO 45. The students must be able to list the missing subjects.
        # need to test
        subject_by_student = set(self.course.list_subjects_by(self))
        all_subjects = set(self.course.list_all_subjects(self))
        return list(all_subjects.difference(subject_by_student))


class Approved(IState):
    def get_next_state(context):
        raise InvalidStateTransitionError(f"{context.state} to {Approved}")


class InProgress(IState):
    def get_next_state(context: Student):
        if context.state == Approved:
            raise InvalidStateTransitionError(f"{context.state} to {InProgress}")
        # 3. The student is considered approved at the university if their GPA is above or equal to 7 (seven) at the end of the course.
        # 35. The students are only approved if they achieve the minimum grade in all course subjects, even if their GPA is above the minimum.
        if all([context.grade >= 7, not context.has_missing_subjects()]):
            return Approved
        return InProgress


class Locked(IState):
    def get_next_state(context: Student):
        if context.state == Approved:
            raise InvalidStateTransitionError(f"{context.state} to {Locked}")
        return Locked
