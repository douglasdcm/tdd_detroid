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
    courses = _populate(Course)
    students = _populate(Student)
    for student in students:
        student.course = courses[0]
    subjects = _populate(Subject)
    for subject in subjects:
        subject.course = courses[0]
    save_all(CourseDataManager(), courses)
    save_all(StudentDataManager(), students)
    save_all(SubjectDataManager(), subjects)


def _populate(obj_type: type[AbstractCoreObject]):
    objs = []
    for _ in RANGE:
        objs.append(obj_type(""))
    return objs


def save_all(data_manager: BaseCoreDataManager, obj_type: type[AbstractCoreObject]):
    data_manager.clear()
    data_manager.save_objects(obj_type)


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
