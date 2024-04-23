import logging
import json
from src.services.student_handler import (
    StudentHandler,
)
from src.services.course_handler import (
    CourseHandler,
)
from src.services.grade_calculator import GradeCalculator
from src.services.subject_handler import SubjectHandler
from src.services.semester_monitor import (
    SemesterMonitor,
)


def close_semester(database, identifier):
    try:
        course_handler = SemesterMonitor(database, identifier)
        course_handler.close()
        print(f"Semester '{identifier}' closed.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def remove_subject(database, course_name, subject_name):
    try:
        subject_handler = SubjectHandler(database, course=course_name)
        subject_handler.name = subject_name
        subject_handler.remove()
        print(f"Subject removed from course.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def cancel_course(database, name):
    try:
        course_handler = CourseHandler(database)
        course_handler.load_from_database(name)
        course_handler.cancel()
        print(f"Course '{name}' cancelled.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def deactivate_course(database, name):
    try:
        course_handler = CourseHandler(database)
        course_handler.load_from_database(name)
        course_handler.deactivate()
        print(f"Course '{name}' deactivated.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def activate_course(database, name):
    try:
        course_handler = CourseHandler(database)
        course_handler.load_from_database(name)
        course_handler.activate()
        print(f"Course '{name}' activated.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def create_course(database, name, max_enrollment):
    try:
        course_handler = CourseHandler(database)
        course_handler.create(name, max_enrollment)
        print(f"Course '{name}' created.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return str(e)


def add_subject_to_course(database, course_name, subject_name):
    try:
        course_handler = CourseHandler(database)
        course_handler.name = course_name
        course_handler.add_subject(subject_name)
        print(f"Subject '{subject_name}' added to course '{course_name}'.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def calculate_student_gpa(database, student_identifier):
    try:
        grade_calculator = GradeCalculator(database)
        gpa = grade_calculator.calculate_gpa_for_student(student_identifier)
        print(f"GPA of student is '{gpa}'.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def take_subject(database, student_identifier, subject_name):
    try:
        student_handler = StudentHandler(database, student_identifier)
        student_handler.take_subject(subject_name)
        print(f"Student toke subject '{subject_name}'.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def lock_course(database, student_identifier):
    try:
        student_handler = StudentHandler(database, student_identifier)
        student_handler.lock_course()
        print(f"Student locked the course.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def unlock_course(database, student_identifier):
    try:
        student_handler = StudentHandler(database, student_identifier)
        student_handler.unlock_course()
        print(f"Student unlocked the course.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def update_grade(database, student_identifier, subject_name, grade):
    try:
        student_handler = StudentHandler(database, student_identifier)
        student_handler.update_grade_to_subject(grade, subject_name)
        print(f"Student updated grade of subject '{subject_name}' to '{grade}'.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def enroll_student(database, name, cpf, course_name):
    try:
        student = StudentHandler(database)
        student.name = name
        student.cpf = cpf
        identifier = student.enroll_to_course(course_name)
        print(
            f"Student '{name}' enrolled in course '{course_name}' with identifier '{identifier}'."
            f" Save the identifier. It is necessary for next operations."
        )
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False
        # print(str(e))
        return False


def list_student_details(database, course_name):
    try:
        course_handler = CourseHandler(database)
        course_handler.name = course_name
        students = course_handler.list_student_details()
        print(f"List of students in course {course_name}:")
        print(json.dumps(students, sort_keys=True, indent=4))
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


def list_all_course_details(database):
    try:
        course_handler = CourseHandler(database)
        courses = course_handler.list_all_courses_with_details()
        print(f"List of courses:")
        print(json.dumps(courses, sort_keys=True, indent=4))
        return courses
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


class CommandError(Exception):
    pass