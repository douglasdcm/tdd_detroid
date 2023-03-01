import click
from src.controllers import courses
from src.schemes.course import CourseDB
from src.utils import sql_client


@click.group()
def course():
    # do nothing #
    pass


@course.command()
@click.option("--name", required=True, help="Course name")
def create(name):
    try:
        courses.create(name)
        id_ = sql_client.get_maximum(CourseDB).id
        click.echo(f"course definido: id {id_}, name {name}")
    except Exception as e:
        click.echo(e)
