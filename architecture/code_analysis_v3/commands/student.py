import click
from core.controller import StudentController

CONTROLLER = StudentController()


@click.group()
def student_cmd():
    # do nothing #
    pass


@student_cmd.command()
@click.option(
    "--nui",
    prompt="Inform student NUI",
    help="NUI of the student.",
)
@click.option(
    "--name",
    prompt="Inform student name",
    help="Name of the student.",
)
@click.option(
    "--age",
    prompt="Inform student age",
    help="Age of the student.",
    type=int,
)
def add_info(nui, name, age):
    CONTROLLER.add_basic_information(nui, name, age)


@student_cmd.command()
@click.option(
    "--nui",
    prompt="Inform student NUI (Number Unique Identification)",
    help="NUI of the student.",
    type=int,
)
def list_info(nui):
    click.echo(vars(CONTROLLER.list_information(nui)))


@student_cmd.command()
@click.option(
    "--nui",
    prompt="Inform student NUI (Number Unique Identification)",
    help="NUI of the student.",
    type=int,
)
def list_subjects(nui):
    click.echo(CONTROLLER.list_subjects(nui))


@student_cmd.command()
@click.option(
    "--nui",
    prompt="Inform student NUI (Number Unique Identification)",
    help="NUI of the student.",
    type=int,
)
@click.option(
    "--snui",
    prompt="Inform subject NUI (Number Unique Identification)",
    help="NUI of the subject.",
    type=int,
)
def subscribe(nui, snui):
    CONTROLLER.subscribe_to_subject(nui, snui)
