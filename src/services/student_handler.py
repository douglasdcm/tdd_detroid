import logging
from src.services.enrollment_validator import EnrollmentValidator
from src.services.course_handler import CourseHandler, NonValidCourse
from src.services.subject_handler import SubjectHandler, NonValidSubject
from src.services.grade_calculator import GradeCalculator
from src.services.cpf_validator import is_valide_cpf
from src import utils
from src.database import Database, NotFoundError
from src.services.grade_calculator import GradeCalculator, NonValidGradeOperation
from src.constants import (
    DUMMY_IDENTIFIER,
    SUBJECT_IN_PROGRESS,
    STUDENT_APPROVED,
    STUDENT_FAILED,
    MAX_SEMESTERS_TO_FINISH_COURSE,
)
from src.exceptions import NonValidStudent, NonValidGrade


class StudentHandler:
    class Subject:
        identifier = None
        grade = None

    def __init__(self, database: Database, identifier=None):
        self.__LOCKED = "locked"
        self.__ENROLLED = "enrolled"
        self.__state = None
        self.__gpa = 0
        self.__course = None
        self.__name = None
        self.__cpf = None
        self.__semester_counter = 0
        self.__subjects = []
        self.__database = database
        self.__identifier = identifier
        if identifier:
            self.load_from_database(identifier)

    def __generate_identifier_when_student_ready(self):
        if self.__name and self.__cpf and self.__course:
            self.__identifier = utils.generate_student_identifier(
                self.__name, self.__cpf, self.__course
            )

    def __check_cpf_validity(self, value):
        if not is_valide_cpf(value):
            raise NonValidStudent(f"CPF '{value}' is not valid.")

    def __check_cpf(self):
        if not self.__cpf:
            raise NonValidStudent("Need to set the student's CPF.")

    def __check_locked(self):
        if self.__state == self.__LOCKED:
            raise NonValidStudent(f"Student is locked.")

    def __check_enrolled_student(self, course_name):
        enrollment_validator = EnrollmentValidator(self.__database)
        if not (
            enrollment_validator.validate_student_by_data(
                self.__name, self.__cpf, course_name
            )
            or enrollment_validator.validate_student_by_identifier(self.__identifier)
        ):
            raise NonValidStudent(
                f"Student '{self.__name}' does not appears in enrollment list."
            )

        courser_handler = CourseHandler(self.__database)
        courser_handler.name = course_name
        if not courser_handler.is_active():
            raise NonValidCourse(f"The course '{course_name}' is not active.")

    def __check_grade_range(self, grade):
        if grade < 0 or grade > 10:
            raise NonValidGrade("Grade must be between '0' and '10'.")

    def __remove_dummy_subject(self, grade_calculator):
        if grade_calculator.search(self.__identifier, DUMMY_IDENTIFIER):
            grade_calculator.remove(self.__identifier, DUMMY_IDENTIFIER)

    def __check_subject_activation(self, subject_handler):
        if not subject_handler.is_active():
            raise NonValidSubject(
                f"Subject '{subject_handler.identifier}' is not active."
            )

    def __check_subject_availability(self, subject_handler):
        if not subject_handler.is_available():
            raise NonValidSubject(
                f"Subject '{subject_handler.identifier}' is not available."
            )

    def __check_course_is_same_of_subject(self, subject_handler):
        if subject_handler.course != self.__course:
            raise NonValidSubject(
                f"The subject '{subject_handler.identifier}' is not part of course '{self.__course}'."
            )

    def __return_subject_situation(self, grade):
        if grade < 7:
            return "failed"
        return "passed"

    def __check_valid_subject(self, subject_identifier):
        if not subject_identifier in self.subjects:
            raise NonValidSubject(
                f"The student is not enrolled to this subject '{subject_identifier}'"
            )

    def __check_finished_course(self):
        if self.__state == STUDENT_APPROVED or self.__state == STUDENT_FAILED:
            raise NonValidStudent(
                f"Can not perform the operation. The student '{self.__name}' is '{self.__state}' in course '{self.__course}'"
            )

    def __check_name(self):
        if not self.__name:
            raise NonValidStudent("Need to set the student's name.")

    def __fail_course_if_exceed_max_semester(self):
        if self.__semester_counter > MAX_SEMESTERS_TO_FINISH_COURSE:
            self.__state = STUDENT_FAILED
            self.__database.student.save_state(self.__state)

    def __save(self):
        if not self.__identifier:
            return
        try:
            self.__database.student.name = self.__name
            self.__database.student.state = self.__state
            self.__database.student.cpf = self.__cpf
            self.__database.student.identifier = self.__identifier
            self.__database.student.gpa = GradeCalculator(
                self.__database
            ).calculate_gpa_for_student(self.__identifier)
            self.__database.student.subjects.extend(self.__subjects)
            self.__database.student.course = self.__course
            self.__database.student.semester_counter = self.__semester_counter
            self.__database.student.save()
        except Exception as e:
            logging.error(str(e))
            raise

    @property
    def identifier(self):
        return self.__identifier

    @property
    def semester_counter(self):
        self.load_from_database(self.__identifier)
        return self.__semester_counter

    @property
    def state(self):
        self.load_from_database(self.__identifier)
        return self.__state

    @state.setter
    def state(self, value):
        self.load_from_database(self.__identifier)
        self.__state = value
        self.__save()

    @property
    def gpa(self):
        self.__calculate_gpa()
        return self.__gpa

    @property
    def subjects(self):
        self.load_from_database(self.__identifier)
        return self.__subjects

    @property
    def name(self):
        self.load_from_database(self.__identifier)
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self.__generate_identifier_when_student_ready()
        self.__save()

    @property
    def cpf(self):
        self.load_from_database(self.__identifier)
        return self.__cpf

    @property
    def course(self):
        self.load_from_database(self.__identifier)
        return self.__course

    @cpf.setter
    def cpf(self, value):
        self.__check_cpf_validity(value)
        self.__cpf = value
        self.__generate_identifier_when_student_ready()
        self.__save()

    def __calculate_gpa(self):
        self.__check_enrolled_student(self.course)
        self.load_from_database(self.__identifier)
        self.__check_locked()
        try:
            self.__gpa = GradeCalculator(self.__database).calculate_gpa_for_student(
                self.__identifier
            )
        except NonValidGradeOperation as e:
            raise NonValidGrade(f"Student may not be enrolled to any subject.")
        except Exception as e:
            logging.error(str(e))
            raise

    def increment_semester(self):
        self.load_from_database(self.__identifier)
        self.__check_finished_course()
        self.__semester_counter += 1
        self.__fail_course_if_exceed_max_semester()
        self.__database.student.save_semester_counter(self.__semester_counter)

    def update_grade_to_subject(self, grade, subject_name):
        self.__check_grade_range(grade)
        self.__check_finished_course()
        self.load_from_database(self.__identifier)
        self.__check_locked()
        subject_identifier = utils.generate_subject_identifier(
            self.__course, subject_name
        )
        self.__check_valid_subject(subject_identifier)

        self.__subjects.append(subject_identifier)

        grade_calculator = GradeCalculator(self.__database)
        grade_calculator.student_identifier = self.__identifier
        grade_calculator.subject_identifier = subject_identifier
        grade_calculator.grade = grade
        subject_situation = self.__return_subject_situation(grade)
        grade_calculator.subject_situation = subject_situation
        grade_calculator.save()

    def enroll_to_course(self, course_name):
        try:
            self.__check_name()
            self.__check_cpf()
            self.__check_enrolled_student(course_name)
            self.__check_finished_course()

            course = CourseHandler(self.__database)
            course.load_from_database(course_name)
            self.__course = course_name
            self.__generate_identifier_when_student_ready()
            course.enroll_student(self.__identifier)

            self.__state = self.__ENROLLED
            self.__database.student.name = self.__name
            self.__database.student.state = self.__state
            self.__database.student.cpf = self.__cpf
            self.__database.student.identifier = self.__identifier
            self.__database.student.gpa = 0
            self.__database.student.subjects.extend(self.__subjects)
            self.__database.student.course = self.__course
            self.__database.student.semester_counter = self.__semester_counter
            self.__database.student.add()

            grade_calculator = GradeCalculator(self.__database)
            grade_calculator.add(self.__identifier, DUMMY_IDENTIFIER, grade=0)

            return self.__identifier
        except Exception as e:
            logging.error(str(e))
            raise

    def take_subject(self, subject_name):
        self.__check_enrolled_student(self.__course)
        self.__check_finished_course()
        self.load_from_database(self.__identifier)
        self.__check_locked()

        subject_identifier = utils.generate_subject_identifier(
            self.__course, subject_name
        )
        if subject_identifier in self.__subjects:
            raise NonValidSubject(
                f"The student already toke the subject '{subject_name}'."
            )
        subject_handler = SubjectHandler(self.__database)
        try:
            subject_handler.load_from_database(subject_identifier)
        except NotFoundError as e:
            logging.error(str(e))
            raise NonValidSubject(f"Subject '{subject_identifier}' not found.")
        except Exception as e:
            logging.error(str(e))
            raise

        self.__check_course_is_same_of_subject(subject_handler)
        self.__check_subject_availability(subject_handler)
        self.__check_subject_activation(subject_handler)

        self.__subjects.append(subject_identifier)
        self.__database.student.save_subjects(self.__subjects)

        subject_handler.enrolled_students.append(self.__identifier)
        self.__database.subject.save_students(subject_handler.enrolled_students)

        grade_calculator = GradeCalculator(self.__database)
        self.__remove_dummy_subject(grade_calculator)
        grade_calculator.subject_situation = SUBJECT_IN_PROGRESS
        grade_calculator.add(self.__identifier, subject_identifier, grade=0)

        return True

    def unlock_course(self):
        self.__check_enrolled_student(self.__course)
        self.__check_finished_course()
        self.load_from_database(self.__identifier)
        self.__state = self.__ENROLLED
        self.__save()
        return self.state

    def lock_course(self):
        self.__check_enrolled_student(self.__course)
        self.__check_finished_course()
        self.load_from_database(self.__identifier)
        self.__state = self.__LOCKED
        self.__save()
        return self.state

    def search_all(self):
        return self.__database.student.search_all()

    def load_from_database(self, student_identifier):
        try:
            self.__database.student.load(student_identifier)

            self.__name = self.__database.student.name
            self.__state = self.__database.student.state
            self.__cpf = self.__database.student.cpf
            self.__identifier = self.__database.student.identifier
            self.__gpa = self.__database.student.gpa
            self.__subjects.extend(self.__database.student.subjects)
            self.__course = self.__database.student.course
            self.__semester_counter = self.__database.student.semester_counter

        except NotFoundError as e:
            raise NonValidStudent(f"Student not found.")
        except Exception as e:
            logging.error(str(e))
            raise
