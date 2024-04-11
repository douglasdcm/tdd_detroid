import logging
from src.services.student_handler import StudentHandler, NonValidStudent


def enroll_student(database, name, cpf, course_identifier):
    try:
        student = StudentHandler(database)
        student.name = name
        student.cpf = cpf
        student.enroll_to_course(course_identifier)
        print("Student enrolled.")
        return True
    except NonValidStudent:
        print(
            f"Student '{name}' with CPF '{cpf}' is not valid in course '{course_identifier}'"
        )
    except Exception as e:
        logging.error(str(e))
        print("Unexpected error. Consult the system adminstrator.")
    return False
