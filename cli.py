import logging
import click
import requests
from src import cli_helper
from src.database import Database
import os


logging.basicConfig(
    filename="cli.log",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s: [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s",
    filemode="a",
    level="ERROR",
)

TOKEN_FILE = "token"


class NonValidToken(Exception):
    pass


def __check_connection():
    token = ""
    with open(TOKEN_FILE) as f:
        token = f.readline()
    url = "https://testrock.kinde.com/oauth2/user_profile"
    payload = {}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        raise NonValidToken("Token is not valid.")


@click.group()
def cli():
    # do nothing #
    pass


@click.command()
@click.option(
    "--identifier",
    prompt="Semester identifier",
    help="Semester identifier. E.g. '2024-1'.",
)
def close_semester(identifier):
    try:
        __check_connection()
        database = Database()
        cli_helper.close_semester(database, identifier)
    except Exception:
        raise


@click.command()
def list_courses():
    try:
        __check_connection()
        cli_helper.list_all_course_details(Database())
    except Exception:
        raise


@click.command()
@click.option(
    "--course-name",
    prompt="Course name",
    help="Course name.",
)
def list_students(course_name):
    try:
        __check_connection()
        database = Database()
        cli_helper.list_student_details(database, course_name)
    except Exception:
        raise


@click.command()
@click.option("--course-name", prompt="Course name", help="Name of the course.")
@click.option("--subject-name", prompt="Subject name", help="Name of the subject.")
def remove_subject(course_name, subject_name):
    try:
        __check_connection()
        database = Database()
        cli_helper.remove_subject(database, course_name, subject_name)
    except Exception:
        raise


@click.command()
@click.option("--name", prompt="Course name", help="Name of the course.")
def cancel_course(name):
    try:
        __check_connection()
        database = Database()
        cli_helper.cancel_course(database, name)
    except Exception:
        raise


@click.command()
@click.option("--name", prompt="Course name", help="Name of the course.")
def deactivate_course(name):
    try:
        __check_connection()
        database = Database()
        cli_helper.deactivate_course(database, name)
    except Exception:
        raise


@click.command()
@click.option("--name", prompt="Course name", help="Name of the course.")
@click.option(
    "--max-enrollment",
    prompt="Course maximum number of students",
    type=int,
    help="The maximum number of students in a course.",
)
def create_course(name, max_enrollment):
    database = Database()
    cli_helper.create_course(database, name, max_enrollment)


@click.command()
@click.option("--course-name", prompt="Course name", help="Name of the course.")
@click.option("--subject-name", prompt="Subject name", help="Name of the subject.")
def add_subject(course_name, subject_name):
    try:
        __check_connection()

        database = Database()
        cli_helper.add_subject_to_course(database, course_name, subject_name)
    except Exception:
        raise


@click.command()
@click.option("--name", prompt="Course name", help="Name of the course.")
def activate_course(name):
    try:
        __check_connection()
        database = Database()
        cli_helper.activate_course(database, name)
    except Exception:
        raise


@click.command()
@click.option("--name", prompt="Student name", help="Name of the student.")
@click.option(
    "--cpf", prompt="Student CPF. E.g. 123.456.789-10", help="CPF of the student."
)
@click.option(
    "--course-name",
    prompt="Course number identifier",
    help="Course number identifier.",
)
def enroll_student(name, cpf, course_name):
    try:
        __check_connection()
        database = Database()
        cli_helper.enroll_student(database, name, cpf, course_name)
    except Exception:
        raise


@click.command()
@click.option(
    "--student-identifier",
    prompt="Student identifier",
    help="Student identifier number.",
    hide_input=True,
)
def calculate_gpa(student_identifier):
    try:
        __check_connection()
        database = Database()
        cli_helper.calculate_student_gpa(database, student_identifier)
    except Exception:
        raise


@click.command()
@click.option(
    "--student-identifier",
    prompt="Student identifier",
    help="Student identifier number.",
    hide_input=True,
)
@click.option(
    "--subject-name",
    prompt="Subject name",
    help="The name of the subject the student wants to take.",
)
@click.option(
    "--grade",
    type=float,
    prompt="Subject name",
    help="The name of the subject the student wants to take.",
)
def update_grade(student_identifier, subject_name, grade):
    try:
        __check_connection()
        database = Database()
        cli_helper.update_grade(database, student_identifier, subject_name, grade)
    except Exception:
        raise


@click.command()
@click.option(
    "--student-identifier",
    prompt="Student identifier",
    help="Student identifier number.",
    hide_input=True,
)
@click.option(
    "--subject-name",
    prompt="Subject name",
    help="The name of the subject the student wants to take.",
)
def take_subject(student_identifier, subject_name):
    try:
        __check_connection()
        database = Database()
        cli_helper.take_subject(database, student_identifier, subject_name)
    except Exception:
        raise


@click.command()
@click.option(
    "--student-identifier",
    prompt="Student identifier",
    help="Student identifier number.",
    hide_input=True,
)
def lock_course(student_identifier):
    try:
        __check_connection()
        database = Database()
        cli_helper.lock_course(database, student_identifier)
    except Exception:
        raise


@click.command()
@click.option(
    "--student-identifier",
    prompt="Student identifier",
    help="Student identifier number.",
    hide_input=True,
)
def unlock_course(student_identifier):
    try:
        __check_connection()
        database = Database()
        cli_helper.unlock_course(database, student_identifier)
    except Exception:
        raise


@click.command()
@click.option(
    "--token",
    prompt="Inform token",
    help="Token to authenticate.",
    hide_input=True,
)
def set_token(token):
    try:
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
    except Exception:
        raise


cli.add_command(set_token)
cli.add_command(enroll_student)
cli.add_command(take_subject)
cli.add_command(update_grade)
cli.add_command(calculate_gpa)
cli.add_command(lock_course)
cli.add_command(unlock_course)

cli.add_command(activate_course)
cli.add_command(deactivate_course)
cli.add_command(cancel_course)
cli.add_command(remove_subject)
cli.add_command(list_students)
cli.add_command(list_courses)
cli.add_command(create_course)
cli.add_command(add_subject)

cli.add_command(close_semester)


if __name__ == "__main__":
    cli()
