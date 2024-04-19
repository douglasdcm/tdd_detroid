import sqlite3
import logging
from src.constants import DUMMY_IDENTIFIER
from src.services.grade_calculator import GradeCalculator
from src.database import Database, NotFoundError
from src.services.subject_handler import SubjectHandler
from src import utils


class CourseHandler:
    def __init__(self, database: Database) -> None:
        self.ACTIVE = "active"
        self.INACTIVE = "inactive"
        self.CANCELLED = "cancelled"
        self.__identifier = DUMMY_IDENTIFIER
        self.__name = None
        self.__state = self.INACTIVE  # TODO use enum
        self.__enrolled_students = []
        self.__subjects = []
        self.__max_enrollment = 0
        self.__database = database

    def __check_name_lenght(self, value):
        if not value or len(value) > 10:
            raise NonValidCourse(
                f"The maximum number of characters to course's " f"name is '10'."
            )

    def __check_name(self):
        if not self.name:
            raise NonValidCourse("Need to set the name.")

    def __check_active(self):
        if not self.state == self.ACTIVE:
            raise NonValidCourse(f"Course '{self.name}' is not active.")

    def __check_cancelled(self):
        if self.state == self.CANCELLED:
            raise NonValidCourse(f"Course '{self.name}' is cancelled.")

    def __check_minimum_number_of_subjects(self):
        MINIMUM = 3
        if not len(self.subjects) >= MINIMUM:
            raise NonMinimunSubjects(
                f"Need '{MINIMUM}' subjects. Set '{len(self.subjects)}'"
            )

    def __check_maximum_enrollment(self):
        if len(self.__database.course.subjects) > self.max_enrollment:
            raise NonValidCourse(
                f"Exceeded the maximum number of subjects."
                f" Expected '{self.max_enrollment}. Set '{len(self.subjects)}'."
            )

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
        self.__subjects = list(set(self.__subjects))
        return self.__subjects

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__check_name_lenght(value)
        self.__identifier = utils.generate_course_identifier(value)
        self.__name = value

    @property
    def max_enrollment(self):
        return self.__max_enrollment

    @max_enrollment.setter
    def max_enrollment(self, value):
        self.__max_enrollment = value

    def is_active(self):
        self.load_from_database(self.name)
        return self.state == self.ACTIVE

    def save(self):
        self.__database.course.name = self.name
        self.__database.course.state = self.state
        self.__database.course.identifier = self.identifier
        self.__database.course.enrolled_students = self.enrolled_students
        self.__database.course.max_enrollment = self.max_enrollment
        self.__database.course.subjects = self.subjects
        self.__check_maximum_enrollment()
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

        except NotFoundError as e:
            logging.error(str(e))
            raise NonValidCourse(f"Course '{name}' not found.")
        except Exception as e:
            logging.error(str(e))
            raise

    def list_student_details(self):
        self.load_from_database(self.name)
        enrolled_students = self.__database.course.enrolled_students
        result = {}

        students_data = []
        for student_identifier in enrolled_students:
            self.__database.student.load(student_identifier)
            subjects_data = []

            for subject_identifier in self.__database.student.subjects:
                grade_calculator = GradeCalculator(self.__database)
                grade_calculator.load_from_database(
                    student_identifier, subject_identifier
                )
                subjects_data.append({subject_identifier: grade_calculator.grade})

            students_data.append(
                {
                    "name": self.__database.student.name,
                    "gpa": self.__database.student.gpa,
                    "grades": subjects_data,
                }
            )
        result["students"] = students_data

        return result

    def list_all_courses_with_details(self):
        all_details = {}
        for course in self.__database.course.search_all():
            self.name = course.name
            all_details[self.name] = self.list_student_details()
            all_details[self.name]["subjects"] = [
                s.name for s in self.__database.subject.search_all_by_course(self.name)
            ]
        return all_details

    def enroll_student(self, student_identifier):
        self.__check_active()
        self.load_from_database(self.name)
        self.__enrolled_students.append(student_identifier)
        self.save()
        return True

    def add_subject(self, subject):
        self.__check_name()
        self.load_from_database(self.name)
        self.__check_cancelled()
        subject_identifier = utils.generate_subject_identifier(self.name, subject)
        if subject_identifier in self.__subjects:
            raise NonValidSubject(
                f"Subject '{subject}' already exists in course '{self.__name}'"
            )
        self.__subjects.append(subject_identifier)
        self.save()

        subject_handler = SubjectHandler(self.__database)
        subject_handler.name = subject
        subject_handler.course = self.name
        subject_handler.add()
        return True

    def cancel(self):
        self.__check_name()
        self.load_from_database(self.name)
        self.__state = self.CANCELLED
        self.save()
        return self.__state

    def deactivate(self):
        self.__check_name()
        self.load_from_database(self.name)
        self.__state = self.INACTIVE
        self.save()
        return self.__state

    def activate(self):
        self.__check_name()
        self.load_from_database(self.name)
        self.__check_minimum_number_of_subjects()

        self.__state = self.ACTIVE
        self.save()
        return self.__state

    def create(self, course_name, max_enrollmet):
        if max_enrollmet < 1:
            raise NonValidCourse(
                f"The max enrollment '{max_enrollmet}' is not valid. Need to set a number bigger than '0'."
            )
        try:
            self.name = course_name
            self.__max_enrollment = max_enrollmet
            self.__database.course.identifier = self.identifier
            self.__database.course.name = course_name
            self.__database.course.state = self.state
            self.__database.course.enrolled_students = self.enrolled_students
            self.__database.course.max_enrollment = self.max_enrollment
            self.__database.course.add()
            return True
        except sqlite3.IntegrityError as e:
            raise NonValidCourse(f"Course '{course_name}' already exists.")
        except Exception as e:
            raise NonValidCourse(
                f"Not able to create the course '{course_name}'. Check with system adminstrator."
            )


class NonValidCourse(Exception):
    pass


class NonMinimunSubjects(Exception):
    pass


class NonValidSubject(Exception):
    pass
