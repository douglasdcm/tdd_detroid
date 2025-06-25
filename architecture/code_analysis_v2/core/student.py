import logging
from typing import TYPE_CHECKING

from architecture.code_analysis_v2.core.common import IState
from architecture.code_analysis_v2.core.base_object import BaseCoreObject

if TYPE_CHECKING:
    from architecture.code_analysis_v2.core.gss import GSS
    from architecture.code_analysis_v2.core.subject import Subject
    from architecture.code_analysis_v2.core.course import Course, NoneCourse

LOGGER = logging.getLogger(__name__)


class BasicInformation:
    def __init__(self, name, age) -> None:
        self._name: str = name
        self._age: int = age

    @property
    def name(self):
        raise NotImplementedError

    @name.setter
    def name(self, value: str):
        raise NotImplementedError

    @property
    def age(self):
        raise NotImplementedError

    @age.setter
    def age(self, value: str):
        raise NotImplementedError


class Student(BaseCoreObject):
    def __init__(self, name) -> None:
        self._course: Course = NoneCourse()
        self._state: IState = InProgress()
        self._grades: list[int] = []
        # TODO 12. The maximum grade for a student in a subject is 10.
        # TODO 13. The minimum grade for a student in a subject is 0.
        self._grade: int = 0
        self._subjects: list[Subject] = []
        # TODO all subjects of the course minus the ones finished
        self._missing_subjects: list[Subject] = []
        # 17. Students must have names.
        self._name: str = name
        # 1. Each student will have a grade control called "grade point average" (GPA).
        self._gpa: int = 0
        # 6. Subjects in each course may have the same names but will be differentiated by a unique identifier (niu).
        self._niu: int = self.__hash__()

    @property
    def course(self) -> Course:
        raise NotImplementedError

    @course.setter
    def course(self, value: Course) -> None:
        # 23. The student can only enroll in one course.
        raise NotImplementedError

    @property
    def grade(self) -> int:
        return self._grade

    @grade.setter
    def grade(self, value: int) -> None:
        # it should be private
        # TODO 14. The student can lock the course, and in this case, they cannot update their grades or the subjects taken.
        # TODO 20. Students can only update their grades in the subjects they are enrolled in.
        raise NotImplementedError

    def _calculate_state(self) -> None:
        raise NotImplementedError

    def _calculate_gpa(self) -> None:
        # TODO 2. The GPA is the average of the student's grades in the ~~courses~~ subjects already taken.
        # calculated when new grade notified
        raise NotImplementedError

    def _calculate_missing_subjects(self) -> None:
        # TODO update the list of missing subjects when notified about the subject state 'Approved'
        raise NotImplementedError

    def _has_missing_subjects(self) -> bool:
        # TODO 31. If the number of subjects missing for a student is less than 3, they can enroll in 1 subject.
        # TODO To be implemented
        raise NotImplementedError

    def notify_about_subject(self, gss: GSS, grade: int) -> None:
        # Entrypoint to notify the state, grade (and other data) of a subject
        # used to update the missing_subjects and the GPA
        raise NotImplementedError

    def subscribe_subject(self, subject: Subject) -> None:
        # TODO 14. The student can lock the course, and in this case, they cannot update their grades or the subjects taken.
        # TODO 30. The student must enroll in a minimum of 3 subjects.
        # what happens if enrolled in less than 10? what is the state? Are operations is restricted?
        raise NotImplementedError

    def create_student_with_basic_information(self, basic_information: BasicInformation) -> None:
        # TODO 36. The student (person) must be able to create students with basic information.
        # Is it possible to create more then one? Shouldn't be responsibility of the admin to create and the person adds more data?
        raise NotImplementedError

    def list_all_their_subjects_by_course(self) -> list[Subject]:
        # TODO 43. The students must be able to list all subjects only from their course.
        # need to test
        # which data is necessary to show about the subject?
        raise NotImplementedError

    def list_all_subcribed_subjects(self) -> list[Subject]:
        # TODO 44. The students must be able to list all subjects they have taken.
        # 'taken' was replaced by 'subcribed' to be consistent with other requirements
        # It is not clear the purpose of the method
        raise NotImplementedError

    def list_missing_subjects(self) -> list[Subject]:
        # TODO 45. The students must be able to list the missing subjects.
        raise NotImplementedError


class NoneStudent(Student):
    def __init__(self, name=""):
        super().__init__(name)


class Approved(IState):
    @staticmethod
    def get_next_state(context):
        raise NotImplementedError


class InProgress(IState):
    @staticmethod
    def get_next_state(context: Student):
        raise NotImplementedError


class Locked(IState):
    @staticmethod
    def get_next_state(context: Student):
        raise NotImplementedError
