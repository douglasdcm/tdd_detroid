from architecture.code_analysis_v2.core.base_object import BaseCoreObject
from architecture.code_analysis_v2.database import Database
from architecture.code_analysis_v2.core.student import BasicInformation, Student
from architecture.code_analysis_v2.core.teacher import Teacher
from architecture.code_analysis_v2.core.subject import Subject
from architecture.code_analysis_v2.core.exceptions import InvalidOperationError


class BaseController:
    def list_subjects_by_course(self, context: Student | Teacher) -> list[Subject]:
        # TODO Get the course `nui` from the `context` in a general implementaion
        # or use the spefici method `get_subject` of the context to return the filtered
        # list of subjects. For example, if the student selects the list of subjects, just the missing
        # subjects should be returned. If the Teacher does the search, just the 'in progress' course shoulde be
        # returned. It depends on the future features to be defined
        # If they need a complete list of Subjects, they could ask to the Course Coordinator or to Adminstrators, for example
        raise NotImplementedError


class ControllerStudent(BaseController):
    def add_basic_information(self, basic_information: BasicInformation) -> None:
        raise NotImplementedError

    def subscribe_to_subject(self, subject_nui: int) -> None | InvalidOperationError:
        raise NotImplementedError


class ControllerTeacher(BaseController):
    def subscribe_to_subject(self, subject_nui) -> None | InvalidOperationError:
        raise NotImplementedError

    def set_student_grade(
        self, grade: int, student_nui: int, subject_nui: int
    ) -> None | InvalidOperationError:
        raise NotImplementedError

    def get_students_by_subject(self, subject_nui: int) -> list[Student] | InvalidOperationError:
        # TODO Should return at least the nui and the complete name
        raise NotImplementedError
