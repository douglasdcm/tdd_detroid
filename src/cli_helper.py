import logging
import json
from src.services.student_handler import (
    StudentHandler,
    NonValidStudent,
    NonValidGrade,
)
from src.services.course_handler import (
    CourseHandler,
    NonValidCourse,
    NonMinimunSubjects,
)
from src.services.grade_calculator import GradeCalculator, NonValidGradeOperation
from src.services.subject_handler import SubjectHandler, NonValidSubject
from src.services.semester_monitor import (
    SemesterMonitor,
    NonValidOperation,
    NonValidSemester,
)


UNEXPECTED_ERROR = "Unexpected error. Consult the system adminstrator."


def close_semester(database, identifier):
    try:
        course_handler = SemesterMonitor(database, identifier)
        course_handler.close()
        print(f"Semester '{identifier}' closed.")
        return True
    except (NonValidOperation, NonValidSemester) as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


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
        print(f"Course '{name}' cancelled.")
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
        print(f"Course '{name}' deactivated.")
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
        print(f"Course '{name}' activated.")
        return True
    except (NonValidCourse, NonMinimunSubjects) as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def create_course(database, name, max_enrollment):
    try:
        course_handler = CourseHandler(database)
        course_handler.create(name, max_enrollment)
        print(f"Course '{name}' created.")
        return True
    except NonValidCourse as e:
        logging.error(str(e))
        print(f"Course '{name}' is not valid.")
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def add_subject_to_course(database, course_name, subject_name):
    try:
        course_handler = CourseHandler(database)
        course_handler.name = course_name
        course_handler.add_subject(subject_name)
        print(f"Subject '{subject_name}' added to course '{course_name}'.")
        return True
    except NonValidCourse as e:
        logging.error(str(e))
        print(f"Course '{course_name}' is not valid.")
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
        print(
            f"Student '{name}' enrolled in course '{course_name}' with identifier '{identifier}'."
        )
        return True
    except (NonValidStudent, NonValidCourse) as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def list_student_details(database, course_name):
    try:
        course_handler = CourseHandler(database)
        course_handler.name = course_name
        students = course_handler.list_student_details()
        print(f"List of students in course {course_name}:")
        print(json.dumps(students, sort_keys=True, indent=4))
        return True
    except NonValidStudent as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False


def list_all_course_details(database):
    try:
        course_handler = CourseHandler(database)
        courses = course_handler.list_all_courses_with_details()
        print(f"List of courses:")
        print(json.dumps(courses, sort_keys=True, indent=4))
        return True
    except NonValidStudent as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(str(e))
        print(UNEXPECTED_ERROR)
    return False
