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
from src.kinde.user_profile import UserProfile
from src.exceptions import NonValidOperation, NonValidToken
from src.constants import TOKEN_FILE, TESTING_FLAG
from src.kinde.token import Token
from src.kinde.organization import Organization
from src.exceptions import NonValidOperation


class Roles:
    STUDENT = "student"
    COORDINATOR = "coordinator"


def __check_user_authentication():
    if TESTING_FLAG:
        return

    try:
        token = ""
        with open(TOKEN_FILE) as f:
            token = f.readline()
        user_profile = UserProfile(token)
        response = user_profile.get()
        if not response:
            raise NonValidToken("Token is not valid.")
        return response.id
    except Exception as e:
        logging.error(str(e))
        raise


def __check_coordenator_role(function):
    def inner_function(*args, **kwargs):
        if TESTING_FLAG:
            return function(*args, **kwargs)

        user_id = __check_user_authentication()
        token = Token().get()
        token_text = token.access_token
        organization = Organization(token_text)
        roles = organization.get_user_roles(user_id)
        for role in roles:
            if role.key == Roles.COORDINATOR or role.name == Roles.COORDINATOR:
                return function(*args, **kwargs)
        logging.warn(f"The user need to be a '{Roles.COORDINATOR}'.")
        raise NonValidOperation(f"The user need to be a '{Roles.COORDINATOR}'.")

    return inner_function


def __check_student_role(function):
    def inner_function(*args, **kwargs):
        if TESTING_FLAG:
            return function(*args, **kwargs)

        token = Token().get()
        token_text = token.access_token
        organization = Organization(token_text)
        user_id = __check_user_authentication()
        roles = organization.get_user_roles(user_id)
        for role in roles:
            if role.key == Roles.STUDENT or role.name == Roles.STUDENT:
                return function(*args, **kwargs)
        logging.warn(f"The user need to be a '{Roles.STUDENT}'.")
        raise NonValidOperation(f"The user need to be a '{Roles.STUDENT}'.")

    return inner_function


@__check_coordenator_role
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


@__check_coordenator_role
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


@__check_coordenator_role
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


@__check_coordenator_role
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


@__check_coordenator_role
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


@__check_coordenator_role
def create_course(database, name, max_enrollment):
    try:
        course_handler = CourseHandler(database)
        course_handler.create(name, max_enrollment)
        print(f"Course '{name}' created.")
        return True
    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return False


@__check_coordenator_role
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


@__check_student_role
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


@__check_student_role
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


@__check_student_role
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


@__check_student_role
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


@__check_student_role
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


@__check_student_role
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


@__check_coordenator_role
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


@__check_coordenator_role
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
