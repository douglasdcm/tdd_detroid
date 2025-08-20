import click
from core.controller import TeacherController

CONTROLLER = TeacherController()


@click.group()
def teacher_cmd():
    # do nothing #
    pass


@teacher_cmd.command()
@click.option(
    "--nui",
    prompt="Inform teacher NUI",
    help="NUI of the teacher.",
)
@click.option(
    "--name",
    prompt="Inform teacher name",
    help="Name of the teacher.",
)
@click.option(
    "--age",
    prompt="Inform teacher age",
    help="Age of the teacher.",
    type=int,
)
def add_info(nui, name, age):
    CONTROLLER.add_basic_information(nui, name, age)


@teacher_cmd.command()
@click.option(
    "--nui",
    prompt="Inform teacher NUI (Number Unique Identification)",
    help="NUI of the teacher.",
    type=int,
)
def list_info(nui):
    click.echo(vars(CONTROLLER.list_information(nui)))


@teacher_cmd.command()
@click.option(
    "--nui",
    prompt="Inform teacher NUI (Number Unique Identification)",
    help="NUI of the teacher.",
    type=int,
)
def list_subjects(nui):
    click.echo(CONTROLLER.list_subjects(nui))


@teacher_cmd.command()
@click.option(
    "--nui",
    prompt="Inform teacher NUI (Number Unique Identification)",
    help="NUI of the teacher.",
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
