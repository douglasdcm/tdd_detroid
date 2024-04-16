import logging
from src.services.student_handler import (
    StudentHandler,
    NonValidStudent,
    NonValidGrade,
)
from src.services.course_handler import CourseHandler, NonValidCourse
from src.services.grade_calculator import GradeCalculator, NonValidGradeOperation
from src.services.subject_handler import SubjectHandler, NonValidSubject

UNEXPECTED_ERROR = "Unexpected error. Consult the system adminstrator."


def remove_subject(database, course_name, subject_name):
    try:
        subject_handler = SubjectHandler(database, course=course_name)
        subject_handler.name = subject_name
        subject_handler.remove()
        print(f"Subject removed from course.")
        return True
    except NonValidSubject as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


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
    except (NonValidStudent, NonValidGradeOperation) as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def take_subject(database, student_identifier, subject_name):
    try:
        student_handler = StudentHandler(database, student_identifier)
        student_handler.take_subject(subject_name)
        print(f"Student '{student_identifier}' toke subject '{subject_name}'.")
        return True
    except (NonValidStudent, NonValidSubject, NonValidGrade) as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def lock_course(database, student_identifier):
    try:
        student_handler = StudentHandler(database, student_identifier)
        student_handler.lock_course()
        print(f"Student '{student_identifier}' locked the course.")
        return True
    except (NonValidStudent, NonValidSubject, NonValidGrade) as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def unlock_course(database, student_identifier):
    try:
        student_handler = StudentHandler(database, student_identifier)
        student_handler.unlock_course()
        print(f"Student '{student_identifier}' unlocked the course.")
        return True
    except (NonValidStudent, NonValidSubject, NonValidGrade) as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def update_grade(database, student_identifier, subject_name, grade):
    try:
        student_handler = StudentHandler(database, student_identifier)
        student_handler.update_grade_to_subject(grade, subject_name)
        print(
            f"Student '{student_identifier}' updated grade of subject '{subject_name}' to '{grade}'."
        )
        return True
    except (NonValidStudent, NonValidSubject, NonValidGrade) as e:
        logging.error(str(e))
        print(str(e))
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
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False
