import click
from architecture.code_analysis_v3.commands.student import student_cmd
from architecture.code_analysis_v3.core.base_object import AbstractCoreObject
from architecture.code_analysis_v3.core.course import Course
from architecture.code_analysis_v3.core.student import Student
from architecture.code_analysis_v3.core.subject import Subject
from architecture.code_analysis_v3.db_manager import (
    BaseCoreDataManager,
    CourseDataManager,
    StudentDataManager,
    SubjectDataManager,
)

RANGE = range(10)


@click.group()
def cli():
    # do nothing #
    pass


### while does not have admins ititialize the database with some basic data
def _list_db(data_manager: BaseCoreDataManager):
    click.echo(f"==== {data_manager.__class__.__name__} NUIs ====")
    for obj in data_manager.loadall():
        click.echo(obj)


def _associate(course_dm: BaseCoreDataManager, subject_dm: BaseCoreDataManager):
    return
    for course in course_dm.loadall():
        for subject in subject_dm.loadall():
            course


@cli.command()
def init_db():
    _populate(CourseDataManager(), Course)
    _populate(StudentDataManager(), Student)
    _populate(SubjectDataManager(), Subject)
    _associate(CourseDataManager, SubjectDataManager)


def _populate(data_manager: BaseCoreDataManager, obj_type: type[AbstractCoreObject]):
    data_manager.clear()
    objs = []
    for _ in RANGE:
        objs.append(obj_type(""))
    data_manager.save_objects(objs)
    _list_db(data_manager)


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
