from architecture.code_analysis_v3.core.course import Course
from architecture.code_analysis_v3.core.student import (
    Student,
)
from architecture.code_analysis_v3.core.subject import Subject
from architecture.code_analysis_v3.core.teacher import Teacher


class ValidatorCourse(Course):
    def __init__(self, name=""):
        super().__init__(f"{self.__hash__()}")

    def force_state(self, value):
        self._state = value

    def force_students(self, value):
        self._students.append(value)

    def force_subject(self, value):
        value.course = self

    def force_has_minimum_students(self):
        self.has_minimum_inprogress_students = lambda: True

    def force_has_minimum_subjects(self):
        self.has_minimum_inprogress_subjects = lambda: True

    def force_is_full_of_subjects(self):
        self.is_full_of_subjects = lambda: True

    def force_is_full_of_students(self):
        self.is_full_of_student = lambda: True


class ValidatorStudent(Student):
    def __init__(self, name=""):
        super().__init__(f"{self.__hash__()}")

    def force_state(self, value):
        self._state = value

    def force_gpa(self, value):
        self._gpa = value

    def force_has_course(self):
        self.has_course = lambda: True

    def force_has_minimun_subjects(self):
        self.has_minimum_subjects = lambda: True

    def force_grades(self, grades):
        self._grades_subjects = grades


class ValidatorSubject(Subject):
    def __init__(self, name=""):
        super().__init__(f"{self.__hash__()}")

    def force_course(self, value):
        self._course = value

    def force_state(self, value):
        self._state = value

    def force_has_course(self):
        self.has_course = lambda: True

    def force_has_teacher(self):
        self.has_teacher = lambda: True

    def force_has_minimum_in_progress_students(self):
        self.has_minimum_inprogress_students = lambda: True


class ValidatorTeacher(Teacher):
    def __init__(self, name=""):
        super().__init__(f"{self.__hash__()}")

    def force_has_maximum_subjects(self):
        self.has_maximum_subjects = lambda: True
