from src.services.enrollment_validator import EnrollmentValidator
from src.services.course_handler import CourseHandler, NonValidCourse
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

    def save(self):
        self.__database.student.name = self.name
        self.__database.student.state = self.state
        self.__database.student.cpf = self.cpf
        self.__database.student.identifier = self.identifier
        self.__database.student.gpa = self.gpa
        self.__database.student.subjects = self.subjects
        self.__database.student.course = self.__course
        self.__database.student.save()

    def enroll_to_course(self, name):
        if not self.__is_valid_student(name):
            raise NonValidStudent()

        course = CourseHandler(self.__database)
        course.load_from_database(name)

        enrollment_validator = EnrollmentValidator(self.__database)
        self.__identifier = enrollment_validator.generate_student_identifier(
            self.name, self.cpf, name
        )
        self.__course = name
        course.enroll_student(self.identifier)
        self.__state = self.ENROLLED
        self.save()
        return self.identifier in course.enrolled_students

    def take_subject(self, subject_identifier):
        is_valid_student = self.__is_valid_student()
        if not is_valid_student:
            raise NonValidStudent()

        if self.__is_locked():
            raise NonValidStudent

        subject_handler = SubjectHandler(subject_identifier)
        if subject_handler.course != self.__course:
            raise NonValidSubject()
        if not subject_handler.is_available():
            raise NonValidSubject()

        return self.subjects.append(subject_identifier)

    def unlock_course(self):
        if self.__is_valid_student():
            self.__state = None
            self.save()
            return self.state
        raise NonValidStudent()

    def lock_course(self):
        if self.__is_valid_student():
            self.__state = self.LOCKED
            self.save()
            return self.state
        raise NonValidStudent()


class NonValidStudent(Exception):
    pass


class NonValidSubject(Exception):
    pass
