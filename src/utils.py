import uuid


def generate_course_identifier(name):
    return uuid.uuid5(uuid.NAMESPACE_URL, str(f"{name}")).hex


def generate_student_identifier(name, cpf, course_name):
    return uuid.uuid5(uuid.NAMESPACE_URL, str(f"{name}{cpf}{course_name}")).hex


def generate_subject_identifier(course, name):
    return uuid.uuid5(uuid.NAMESPACE_URL, str(f"{name}{course}")).hex
