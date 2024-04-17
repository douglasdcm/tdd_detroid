import logging
import click
from src import cli_helper
from src.database import Database


logging.basicConfig(
    filename="cli.log",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s: [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s",
    filemode="a",
    level="DEBUG",
)


@click.group()
def cli():
    # do nothing #
    pass


@click.command()
def list_courses():
    try:
        database = Database()
        cli_helper.list_all_course_details(database)
    except Exception as e:
        logging.error(str(e))


@click.command()
@click.option(
    "--course-name",
    prompt="Course name",
    help="Course name.",
)
def list_students(course_name):
    try:
        database = Database()
        cli_helper.list_student_details(database, course_name)
    except Exception as e:
        logging.error(str(e))


@click.command()
@click.option("--course-name", prompt="Course name", help="Name of the course.")
@click.option("--subject-name", prompt="Subject name", help="Name of the subject.")
def remove_subject(course_name, subject_name):
    database = Database()
    cli_helper.remove_subject(database, course_name, subject_name)


@click.command()
@click.option("--name", prompt="Course name", help="Name of the course.")
def cancel_course(name):
    database = Database()
    cli_helper.cancel_course(database, name)


@click.command()
@click.option("--name", prompt="Course name", help="Name of the course.")
def deactivate_course(name):
    database = Database()
    cli_helper.deactivate_course(database, name)


@click.command()
@click.option("--name", prompt="Course name", help="Name of the course.")
def activate_course(name):
    database = Database()
    cli_helper.activate_course(database, name)


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
        database = Database()
        cli_helper.enroll_student(database, name, cpf, course_name)
    except Exception as e:
        logging.error(str(e))


@click.command()
@click.option(
    "--student-identifier",
    prompt="Student identifier",
    help="Student identifier number.",
)
def calculate_student_gpa(student_identifier):
    try:
        database = Database()
        cli_helper.calculate_student_gpa(database, student_identifier)
    except Exception as e:
        logging.error(str(e))


@click.command()
@click.option(
    "--student-identifier",
    prompt="Student identifier",
    help="Student identifier number.",
)
@click.option(
    "--subject-name",
    prompt="Subject name",
    help="The name of the subject the student wants to take.",
)
@click.option(
    "--grade",
    type=int,
    prompt="Subject name",
    help="The name of the subject the student wants to take.",
)
def update_grade(student_identifier, subject_name, grade):
    try:
        database = Database()
        cli_helper.update_grade(database, student_identifier, subject_name, grade)
    except Exception as e:
        logging.error(str(e))


@click.command()
@click.option(
    "--student-identifier",
    prompt="Student identifier",
    help="Student identifier number.",
)
@click.option(
    "--subject-name",
    prompt="Subject name",
    help="The name of the subject the student wants to take.",
)
def take_subject(student_identifier, subject_name):
    try:
        database = Database()
        cli_helper.take_subject(database, student_identifier, subject_name)
    except Exception as e:
        logging.error(str(e))


@click.command()
@click.option(
    "--student-identifier",
    prompt="Student identifier",
    help="Student identifier number.",
)
def lock_course(student_identifier):
    try:
        database = Database()
        cli_helper.lock_course(database, student_identifier)
    except Exception as e:
        logging.error(str(e))


@click.command()
@click.option(
    "--student-identifier",
    prompt="Student identifier",
    help="Student identifier number.",
)
def unlock_course(student_identifier):
    try:
        database = Database()
        cli_helper.unlock_course(database, student_identifier)
    except Exception as e:
        logging.error(str(e))


cli.add_command(enroll_student)
cli.add_command(take_subject)
cli.add_command(update_grade)
cli.add_command(calculate_student_gpa)
cli.add_command(lock_course)
cli.add_command(unlock_course)

cli.add_command(activate_course)
cli.add_command(deactivate_course)
cli.add_command(cancel_course)
cli.add_command(remove_subject)
cli.add_command(list_students)
cli.add_command(list_courses)

if __name__ == "__main__":
    cli()
