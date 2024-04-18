from src import utils
from src.services.course_handler import CourseHandler, NonValidCourse


class EnrollmentValidator:
    def __init__(self, database):
        self.__database = database

    def validate_student_by_data(self, name, cpf, course_name):
        courser_handler = CourseHandler(self.__database)
        courser_handler.name = course_name
        if not courser_handler.is_active():
            raise NonValidCourse(f"The course '{course_name}' is not active.")
        # the valid students are predefined as the list of approved person in the given course
        student_identifier = utils.generate_student_identifier(name, cpf, course_name)
        return self.validate_student_by_identifier(student_identifier)

    def validate_student_by_identifier(self, student_identifier):
        # the valid students are predefined as the list of approved person in the given course
        return self.__database.enrollment.select(student_identifier)
