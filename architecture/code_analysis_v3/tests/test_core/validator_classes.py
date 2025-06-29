from architecture.code_analysis_v3.core.course import Course
from architecture.code_analysis_v3.core.student import (
    Student,
)


class ValidatorCourse(Course):
    def force_state(self, value):
        self._state = value

    def force_students(self, value):
        self._students.append(value)

    def force_subject(self, value):
        self._subjects.append(value)

    def force_has_minimum_students(self):
        self.has_minimum_inprogress_students = lambda: True

    def force_has_minimum_subjects(self):
        self.has_minimum_inprogress_subjects = lambda: True

    def force_full_objects(self):
        pass


class ValidatorStudent(Student):
    def force_state(self, value):
        self._state = value

    def force_gpa(self, value):
        self._gpa = value
