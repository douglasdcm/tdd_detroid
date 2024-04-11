import logging
import click
from src import cli_helper
from src.database import Database

logging.basicConfig(
    filename="cli.log",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s: [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s",
    filemode="a",
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
    "--course-identifier",
    prompt="Course number identifier",
    help="Course number identifier.",
)
def enroll_student(name, cpf, course_identifier):
    database = Database()
    cli_helper.enroll_student(database, name, cpf, course_identifier)


cli.add_command(enroll_student)
cli.add_command(activate_course)
cli.add_command(deactivate_course)
cli.add_command(cancel_course)

if __name__ == "__main__":
    cli()
