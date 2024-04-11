import uuid


def generate_subject_identifier(course, name):
    return uuid.uuid5(uuid.NAMESPACE_URL, str(f"{name}{course}")).hex
