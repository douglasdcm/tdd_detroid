import uuid
import logging
from src.constants import DUMMY_IDENTIFIER
from src.services.grade_calculator import GradeCalculator


class CourseHandler:
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"

    def __init__(self, database) -> None:
        self.__identifier = DUMMY_IDENTIFIER
        self.__name = None
        self.__state = self.INACTIVE  # TODO use enum
        self.__enrolled_students = []
        self.__subjects = []
        self.__max_enrollment = 0
        self.__database = database

    @property
    def identifier(self):
        return self.__identifier

    @property
    def state(self):
        return self.__state

    @property
    def enrolled_students(self):
        return self.__enrolled_students

    @property
    def subjects(self):
        return self.__subjects

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if len(value) > 10:
            raise NonValidCourse(
                f"The maximum number of characters to course's name is '10'. Set with '{len(value)}'."
            )
        self.__name = value

    @property
    def max_enrollment(self):
        return self.__max_enrollment

    @max_enrollment.setter
    def max_enrollment(self, value):
        self.__max_enrollment = value

    def save(self):
        self.__database.course.name = self.name
        self.__database.course.state = self.state
        self.__database.course.identifier = self.identifier
        self.__database.course.enrolled_students = ",".join(self.enrolled_students)
        self.__database.course.max_enrollment = self.max_enrollment
        self.__database.course.subjects = ",".join(self.subjects)
        self.__database.course.save()

    def load_from_database(self, name):
        try:
            self.__database.course.load_from_database(name)

            self.name = self.__database.course.name
            self.__state = self.__database.course.state
            self.__identifier = self.__database.course.identifier
            self.__enrolled_students = self.__database.course.enrolled_students
            self.max_enrollment = self.__database.course.max_enrollment
            self.__subjects = self.__database.course.subjects

        except Exception as e:
            logging.error(str(e))
            raise NonValidCourse("Course not found.")

    def list_student_details(self):
        self.load_from_database(self.name)
        enrolled_students = self.__database.course.enrolled_students
        result = {}
        for student_identifier in enrolled_students:
            self.__database.student.load(student_identifier)
            result[self.__database.student.identifier] = {
                "name": self.__database.student.name,
                "gpa": self.__database.student.gpa,
                "course": self.__database.student.course,
            }

        for student_identifier in enrolled_students:
            self.__database.student.load(student_identifier)
            for subject_identifier in self.__database.student.subjects:
                grade_calculator = GradeCalculator(self.__database)
                grade_calculator.load_from_database(
                    student_identifier, subject_identifier
                )
                result[student_identifier][subject_identifier] = grade_calculator.grade
        return result

    def list_all_courses_with_details(self):
        all_details = {}
        for course in self.__database.course.search_all():
            self.name = course.name
            all_details[self.name] = self.list_student_details()
        return all_details

    def enroll_student(self, student_identifier):
        if not self.state == self.ACTIVE:
            raise NonValidCourse("Course is not active.")
        self.__enrolled_students.append(student_identifier)
        self.save()
        return True

    def add_subject(self, subject):
        self.subjects.append(subject)
        self.save()

    def cancel(self):
        if not self.name:
            raise NonValidCourse("No name set to course.")
        self.__state = self.CANCELLED
        self.save()
        return self.__state

    def deactivate(self):
        if not self.name:
            raise NonValidCourse("No name set to course.")

        if self.state == self.ACTIVE:
            self.__state = self.INACTIVE
            self.save()
        return self.__state

    def activate(self):
        if not self.name:
            raise NonValidCourse("No name set to course.")

        MINIMUM = 3
        if not len(self.subjects) >= MINIMUM:
            raise NonValidCourse(
                f"Need '{MINIMUM}' subjects. Set '{len(self.subjects)}'"
            )

        self.__identifier = uuid.uuid5(uuid.NAMESPACE_URL, f"{self.name}").hex
        self.__state = self.ACTIVE
        self.save()
        return self.__state


class NonValidCourse(Exception):
    pass
