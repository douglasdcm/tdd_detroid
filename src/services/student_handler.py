import logging
from src.services.enrollment_validator import EnrollmentValidator
from src.services.course_handler import CourseHandler
from src.services.subject_handler import SubjectHandler, NonValidSubject
from src.services.grade_calculator import GradeCalculator
from src.services.cpf_validator import is_valide_cpf
from src import utils


class StudentHandler:
    LOCKED = "locked"
    ENROLLED = "enrolled"

    def __init__(self, database, identifier=None):
        self.__identifier = identifier
        self.__state = None
        self.__gpa = 0
        self.__subjects = []
        self.__course = None
        self.__name = None
        self.__cpf = None
        self.__subjects_2 = []
        self.__database = database

    @property
    def identifier(self):
        return self.__identifier

    @property
    def state(self):
        return self.__state

    @property
    def gpa(self):
        return self.__gpa

    @property
    def subjects(self):
        return self.__subjects

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, value):
        if not is_valide_cpf(value):
            raise NonValidStudent(f"CPF {value} is not valid.")
        self.__cpf = value

    def __is_locked(self):
        return self.__state == self.LOCKED

    def __is_enrolled_student(self, course_name):
        enrollment_validator = EnrollmentValidator(self.__database)
        return enrollment_validator.validate_student_by_data(
            self.name, self.cpf, course_name
        ) or enrollment_validator.validate_student_by_identifier(self.identifier)

    def __save(self):
        self.__database.student.name = self.name
        self.__database.student.state = self.state
        self.__database.student.cpf = self.cpf
        self.__database.student.identifier = self.identifier
        self.__database.student.gpa = self.gpa
        self.__database.student.subjects = ",".join(self.subjects)
        self.__database.student.course = self.__course
        self.__database.student.save()

    def __add(self):
        self.__database.student.name = self.name
        self.__database.student.state = self.state
        self.__database.student.cpf = self.cpf
        self.__database.student.identifier = self.identifier
        self.__database.student.gpa = self.gpa
        self.__database.student.subjects = ",".join(self.subjects)
        self.__database.student.course = self.__course
        self.__database.student.add()

    def update_grade_to_subject(self, grade, subject_name):
        if grade < 0 or grade > 10:
            raise NonValidGrade("Grade must be between '0' and '10'")

        self.load_from_database(self.identifier)

        if self.__is_locked():
            raise NonValidStudent(f"Student '{self.identifier}' is locked.")

        subject_identifier = utils.generate_subject_identifier(
            self.__course, subject_name
        )
        if not self.__is_valid_subject(subject_identifier):
            raise NonValidSubject(
                f"The student is not enrolled to this subject '{subject_name}'"
            )

        class Subject:
            identifier = None
            grade = None

        subject = Subject()
        subject.identifier = subject_identifier
        subject.grade = grade
        self.__subjects_2.append(subject)

        grade_calculator = GradeCalculator(self.__database)
        grade_calculator.student_identifier = self.identifier
        grade_calculator.subject_identifier = subject_identifier
        grade_calculator.grade = grade
        grade_calculator.save()
        grade_calculator.load_from_database(self.identifier, subject_identifier)

        # post condition
        assert grade_calculator.student_identifier == self.identifier
        assert grade_calculator.subject_identifier in [
            s.identifier for s in self.__subjects_2
        ]
        assert grade_calculator.grade == grade

    def __is_valid_subject(self, subject_identifier):
        return subject_identifier in self.subjects

    def enroll_to_course(self, course_name):
        try:
            if not self.__name:
                raise NonValidStudent("Need to set the student's name.")
            if not self.__cpf:
                raise NonValidStudent("Need to set the student's CPF.")
            if not self.__is_enrolled_student(course_name):
                raise NonValidStudent(
                    f"Student '{self.identifier}' does not appears in enrollment list."
                )

            course = CourseHandler(self.__database)
            course.load_from_database(course_name)

            self.__identifier = utils.generate_student_identifier(
                self.name, self.cpf, course_name
            )
            self.__course = course_name
            course.enroll_student(self.identifier)
            self.__state = self.ENROLLED
            self.__add()

            # post condition
            self.__database.student.load(self.identifier)
            assert self.__database.student.identifier == self.identifier
            assert self.__database.student.state == self.ENROLLED
            assert self.__database.student.course == self.__course
            assert self.identifier in course.enrolled_students

            return self.identifier
        except Exception as e:
            logging.error(str(e))
            raise

    def take_subject(self, subject_name):
        if not self.__is_enrolled_student(self.__course):
            raise NonValidStudent(f"Student '{self.identifier}' is not valid.")

        self.load_from_database(self.identifier)

        if self.__is_locked():
            raise NonValidStudent(f"Student '{self.identifier}' is locked.")

        subject_identifier = utils.generate_subject_identifier(
            self.__course, subject_name
        )
        subject_handler = SubjectHandler(self.__database)
        try:
            subject_handler.load_from_database(subject_identifier)
        except Exception as e:
            logging.error(str(e))
            raise NonValidSubject(f"Subject '{subject_identifier}' not found.")

        if subject_handler.course != self.__course:
            raise NonValidSubject()

        if not subject_handler.is_available() or not subject_handler.is_active():
            raise NonValidSubject()

        self.subjects.append(subject_identifier)
        self.__save()

        subject_handler.enrolled_students.append(self.identifier)
        subject_handler.save()

        grade_calculator = GradeCalculator(self.__database)
        grade_calculator.add(self.identifier, subject_identifier, grade=0)

        # post condition
        subject_handler.load_from_database(subject_identifier)
        assert self.identifier in subject_handler.enrolled_students

        self.load_from_database(self.identifier)
        assert subject_identifier in self.subjects

        grade_calculator.load_from_database(self.identifier, subject_identifier)
        assert self.identifier in grade_calculator.student_identifier
        assert subject_identifier in grade_calculator.subject_identifier
        assert grade_calculator.grade == 0

        return True

    def unlock_course(self):
        if not self.__is_enrolled_student(self.__course):
            raise NonValidStudent(f"Student is not not enrolled in any course.")
        self.__state = None
        self.__save()
        return self.state

    def lock_course(self):
        if not self.__is_enrolled_student(self.__course):
            raise NonValidStudent(f"Student is not not enrolled in any course.")
        self.__state = self.LOCKED
        self.__save()
        return self.state

    def load_from_database(self, student_identifier):
        try:
            self.__database.student.load(student_identifier)

            self.__name = self.__database.student.name
            self.__state = self.__database.student.state
            self.__cpf = self.__database.student.cpf
            self.__identifier = self.__database.student.identifier
            self.__gpa = self.__database.student.gpa
            self.__subjects = self.__database.student.subjects
            self.__course = self.__database.student.course

        except Exception as e:
            logging.error(str(e))
            raise NonValidStudent("Student not found.")


class NonValidStudent(Exception):
    pass


class NonValidGrade(Exception):
    pass
