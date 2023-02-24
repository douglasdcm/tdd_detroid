import click
from src.controllers import courses
from src.schemes.course import CourseDB
from src.utils import sql_client


@click.group()
def curso():
    # do nothing #
    pass


@curso.command()
@click.option("--nome", required=True, help="Course name")
def create(nome):
    try:
        courses.create(nome)
        id_ = sql_client.get_maximum(CourseDB).id
        click.echo(f"Curso definido: id {id_}, nome {nome}")
    except Exception as e:
        click.echo(e)
