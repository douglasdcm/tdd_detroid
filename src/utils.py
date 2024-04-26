import uuid
import logging
import time


def check_function_execution_time(func):
    def inner(*args, **kwargs):
        t1 = time.perf_counter(), time.process_time()
        result = func(*args, **kwargs)
        t2 = time.perf_counter(), time.process_time()
        print(f"Finished {func.__name__}")
        print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
        print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
        print("---")
        return result

    return inner


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
    return uuid.uuid5(uuid.NAMESPACE_URL, str(f"{name}{course}")).hex
