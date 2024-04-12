import logging
from src.services.enrollment_validator import EnrollmentValidator
from src.services.course_handler import CourseHandler
from src.services.subject_handler import SubjectHandler


class StudentHandler:
    LOCKED = "locked"
    ENROLLED = "enrolled"

    def __init__(self, database):
        self.__identifier = None
        self.__state = None
        self.__gpa = 0
        self.__subjects = []
        self.__course = None
        self.__name = None
        self.__cpf = None
        self.__database = database

    @property
    def identifier(self):
        return self.__identifier

    @identifier.setter
    def identifier(self, value):
        self.__identifier = value

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
        self.__cpf = value

    def __is_locked(self):
        return self.__state == self.LOCKED

    def __is_valid_student(self, course_identifier=None):
        course = self.__course
        if course_identifier:
            course = course_identifier
        return EnrollmentValidator(self.__database).validate_student(
            self.name, self.cpf, course
        )

    def __save(self):
        self.__database.student.name = self.name
        self.__database.student.state = self.state
        self.__database.student.cpf = self.cpf
        self.__database.student.identifier = self.identifier
        self.__database.student.gpa = self.gpa
        self.__database.student.subjects = ",".join(self.subjects)
        self.__database.student.course = self.__course
        self.__database.student.save()

    def enroll_to_course(self, course_name):
        if not self.__is_valid_student(course_name):
            raise NonValidStudent()

        course = CourseHandler(self.__database)
        course.load_from_database(course_name)

        enrollment_validator = EnrollmentValidator(self.__database)
        self.__identifier = enrollment_validator.generate_student_identifier(
            self.name, self.cpf, course_name
        )
        self.__course = course_name
        course.enroll_student(self.identifier)
        self.__state = self.ENROLLED
        self.__save()

        # post condition
        self.__database.student.load(self.identifier)
        assert self.__database.student.identifier == self.identifier
        assert self.__database.student.state == self.ENROLLED
        assert self.__database.student.course == self.__course
        assert self.identifier in course.enrolled_students

        return True

    def take_subject(self, subject_identifier):
        """
        subject_identifier (str): The unique identifier of the subject. It follows the pattern
        <course name>-<subject name>
        """
        is_valid_student = self.__is_valid_student()
        if not is_valid_student:
            raise NonValidStudent()

        if self.__is_locked():
            raise NonValidStudent()

        subject_handler = SubjectHandler(self.__database)
        try:
            subject_handler.load_from_database(subject_identifier)
        except Exception as e:
            logging.error(str(e))
            raise NonValidSubject()

        if subject_handler.course != self.__course:
            raise NonValidSubject()

        if not subject_handler.is_available() or not subject_handler.is_active():
            raise NonValidSubject()

        self.subjects.append(subject_identifier)
        self.__save()

        # post condition
        subject_handler.load_from_database(subject_identifier)
        assert subject_identifier in self.subjects

        return True

    def unlock_course(self):
        if self.__is_valid_student():
            self.__state = None
            self.__save()
            return self.state
        raise NonValidStudent()

    def lock_course(self):
        if self.__is_valid_student():
            self.__state = self.LOCKED
            self.__save()
            return self.state
        raise NonValidStudent()

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
            print("exxxxx ", str(e))
            logging.error(str(e))
            raise NonValidStudent("Student not found.")


class NonValidStudent(Exception):
    pass


class NonValidSubject(Exception):
    pass
