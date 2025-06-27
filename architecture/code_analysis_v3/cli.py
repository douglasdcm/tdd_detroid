import click
from architecture.code_analysis_v3.core.controller import StudentController
import click


@click.group()
def cli():
    # do nothing #
    pass


@click.command()
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
def student_add_info(name, age):
    StudentController().add_basic_information(name, age)


@click.command()
@click.option(
    "--nui",
    prompt="Inform student NUI (Number Unique Identification)",
    help="NUI of the student.",
    type=int,
)
def student_list_info(nui):
    print(StudentController().list_information(nui))


cli.add_command(student_add_info)
cli.add_command(student_list_info)
if __name__ == "__main__":
    cli()
