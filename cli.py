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
def take_subject(student_identifier, subject_name):
    try:
        database = Database()
        cli_helper.take_subject(database, student_identifier, subject_name)
    except Exception as e:
        logging.error(str(e))


cli.add_command(enroll_student)
cli.add_command(take_subject)
cli.add_command(calculate_student_gpa)
cli.add_command(activate_course)
cli.add_command(deactivate_course)
cli.add_command(cancel_course)

if __name__ == "__main__":
    cli()
