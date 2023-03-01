import click
from src.controllers import disciplines


@click.group()
def materia():
    # do nothing #
    pass


@materia.command()
@click.option("--name", required=True, help="Discipline name")
@click.option("--course-id", type=int, required=True, help="Cours identification")
def create(name, course_id):
    try:
        disciplines.create(name, course_id)
        id_ = disciplines.get_maximum().id
        click.echo(f"Materia definida: id {id_}, name {name}")
    except Exception as e:
        click.echo(e)
