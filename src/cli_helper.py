import logging
from src.services.student_handler import StudentHandler, NonValidStudent
from src.services.course_handler import CourseHandler, NonValidCourse
from src.services.grade_calculator import GradeCalculator

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


def calculate_student_gpa(database, student_identifier):
    try:
        grade_calculator = GradeCalculator(database)
        gpa = grade_calculator.calculate_gpa_for_student(student_identifier)
        print(f"GPA of student '{student_identifier}' is '{gpa}'.")
        return True
    except NonValidStudent as e:
        logging.error(str(e))
        print(f"Student '{student_identifier}' is not valid'")
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def enroll_student(database, name, cpf, course_name):
    try:
        student = StudentHandler(database)
        student.name = name
        student.cpf = cpf
        identifier = student.enroll_to_course(course_name)
        print(f"Student enrolled with identifier '{identifier}'.")
        return True
    except NonValidStudent as e:
        logging.error(str(e))
        print(
            f"Student '{name}' with CPF '{cpf}' is not valid in course '{course_name}'"
        )
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False
