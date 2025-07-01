import click
import logging
from commands.student import student_cmd
from core.base_object import AbstractCoreObject
from core.course import Course
from core.student import Student
from core.subject import Subject
from db_manager import (
    BaseCoreDataManager,
    CourseDataManager,
    StudentDataManager,
    SubjectDataManager,
)

# Configure the root logger to capture INFO messages and above
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

RANGE = range(10)


@click.group()
def cli():
    # do nothing #
    pass


# while does not have admins ititialize the database with some basic data
def _list_db(data_manager: BaseCoreDataManager):
    click.echo(f"==== {data_manager.__class__.__name__} NUIs ====")
    for obj in data_manager.loadall():
        click.echo(obj)


@cli.command()
def init_db():
    _populate(CourseDataManager(), Course)
    _populate(StudentDataManager(), Student)
    _populate(SubjectDataManager(), Subject)


def _populate(data_manager: BaseCoreDataManager, obj_type: type[AbstractCoreObject]):
    data_manager.clear()
    objs = []
    for _ in RANGE:
        objs.append(obj_type(""))
    data_manager.save_objects(objs)


@cli.command()
def list_db():
    _list_db(StudentDataManager())
    _list_db(SubjectDataManager())
    _list_db(CourseDataManager())


###

# NUI 7727150366633
cli.add_command(student_cmd)
cli.add_command(init_db)
if __name__ == "__main__":
    cli()
