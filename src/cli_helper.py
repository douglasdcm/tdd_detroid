import logging
from src.services.student_handler import StudentHandler, NonValidStudent
from src.services.course_handler import CourseHandler, NonValidCourse

UNEXPECTED_ERROR = "Unexpected error. Consult the system adminstrator."


def cancel_course(database, name):
    try:
        course_handler = CourseHandler(database)
        course_handler.load_from_database(name)
        course_handler.cancel()
        print(f"Course cancelled.")
        return True
    except NonValidCourse as e:
        logging.error(str(e))
        print(f"Course '{name}' is not valid.")
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def deactivate_course(database, name):
    try:
        course_handler = CourseHandler(database)
        course_handler.load_from_database(name)
        course_handler.deactivate()
        print(f"Course deactivated.")
        return True
    except NonValidCourse as e:
        logging.error(str(e))
        print(f"Course '{name}' is not valid.")
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def activate_course(database, name):
    try:
        course_handler = CourseHandler(database)
        course_handler.load_from_database(name)
        course_handler.activate()
        print(f"Course activated.")
        return True
    except NonValidCourse as e:
        logging.error(str(e))
        print(f"Course '{name}' is not valid.")
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def enroll_student(database, name, cpf, course_identifier):
    try:
        student = StudentHandler(database)
        student.name = name
        student.cpf = cpf
        student.enroll_to_course(course_identifier)
        print("Student enrolled.")
        return True
    except NonValidStudent as e:
        logging.error(str(e))
        print(
            f"Student '{name}' with CPF '{cpf}' is not valid in course '{course_identifier}'"
        )
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False
