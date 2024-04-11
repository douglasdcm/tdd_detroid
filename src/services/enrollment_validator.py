import uuid


class EnrollmentValidator:
    def __init__(self, database):
        self.__database = database

    def validate_student(self, name, cpf, course_identifier):
        # the valid students are predifined as the list of approved person in the given course
        student_identifier = self.generate_student_identifier(
            name, cpf, course_identifier
        )
        return self.__database.enrollment.select(student_identifier)

    def generate_student_identifier(self, name, cpf, course_identifier):
        return uuid.uuid5(
            uuid.NAMESPACE_URL, str(f"{name}{cpf}{course_identifier}")
        ).hex
