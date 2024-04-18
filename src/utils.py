import uuid
import logging


def generate_course_identifier(name):
    logging.info(f"Generate identifier for course '{name}'")
    return uuid.uuid5(uuid.NAMESPACE_URL, str(f"{name}")).hex


def generate_student_identifier(name, cpf, course_name):
    logging.info(
        f"Generate identifier for student: NAME '{name}', CPF '{cpf}', COURSE NAME '{course_name}'"
    )
    return uuid.uuid5(uuid.NAMESPACE_URL, str(f"{name}{cpf}{course_name}")).hex


def generate_subject_identifier(course, name):
    logging.info(f"Generate identifier for subject '{name}'")
    # return uuid.uuid5(uuid.NAMESPACE_URL, str(f"{name}{course}")).hex
    return f"{course}_{name}"
