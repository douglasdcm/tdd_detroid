import uuid
from src import utils


class EnrollmentValidator:
    def __init__(self, database):
        self.__database = database

    def validate_student(self, name, cpf, course_name):
        # the valid students are predefined as the list of approved person in the given course
        student_identifier = utils.generate_student_identifier(name, cpf, course_name)
        return self.__database.enrollment.select(student_identifier)
