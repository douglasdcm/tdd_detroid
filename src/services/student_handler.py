from src.services.enrollment_validator import EnrollmentValidator
from src.services.course_handler import CourseHandler
from src.services.subject_handler import SubjectHandler


class StudentHandler:
    def __init__(self) -> None:
        self.__identifier = None
        self.__state = None
        self.__gpa = 0
        self.__subjects = []
        self.__course = None

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

    def enroll_to_course(self, course_identifier):
        enrollment_validator = EnrollmentValidator()
        is_valid_student = enrollment_validator.validate_student(
            self.name, self.cpf, course_identifier
        )
        if is_valid_student:
            self.__identifier = enrollment_validator.generate_student_identifier(
                self.name, self.cpf, course_identifier
            )
            self.__course = course_identifier
            course = CourseHandler(course_identifier)
            course.enroll_student(self.identifier)
            return self.identifier in course.enrolled_students
        raise NonValidStudent()

    def take_subject(self, subject_identifier):
        enrollment_validator = EnrollmentValidator()
        is_valid_student = enrollment_validator.validate_student(
            self.name, self.cpf, self.__course
        )
        if not is_valid_student:
            raise NonValidStudent()

        subject_handler = SubjectHandler(subject_identifier)
        if subject_handler.course != self.__course:
            raise NonValidSubject()
        if not subject_handler.is_available():
            raise NonValidSubject()

        return self.subjects.append(subject_identifier)


class NonValidStudent(Exception):
    pass


class NonValidSubject(Exception):
    pass
