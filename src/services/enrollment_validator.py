import uuid


class EnrollmentValidator:
    def validate_student(self, name, cpf, course_identifier):
        # TODO do the true check
        dummy_identifier = "290f2113c2e6579c8bb6ec395ea56572"
        return (
            self.generate_student_identifier(name, cpf, course_identifier)
            == dummy_identifier
        )

    def generate_student_identifier(self, name, cpf, course_identifier):
        return uuid.uuid5(
            uuid.NAMESPACE_URL, str(f"{name}{cpf}{course_identifier}")
        ).hex
