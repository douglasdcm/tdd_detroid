import logging
import click
from src import cli_helper
from src.database import Database

logging.basicConfig(
    filename="cli.log",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s: %(message)s",
    filemode="a",
)


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


if __name__ == "__main__":
    enroll_student()
