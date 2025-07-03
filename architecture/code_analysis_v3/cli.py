import logging
import click
from commands.student import student_cmd
from commands.teacher import teacher_cmd
from core.base_object import AbstractCoreObject
from core.course import Course
from core.student import Student
from core.subject import Subject
from core.teacher import Teacher
from db_manager import (
    BaseCoreDataManager,
    CourseDataManager,
    StudentDataManager,
    SubjectDataManager,
    TeacherDataManager,
)

LOGGER = logging.getLogger(__name__)
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

    teachers = _populate(Teacher)
    for teacher in teachers:
        teacher.course = courses[0]

    students = _populate(Student)
    for student in students:
        student.course = courses[0]
    subjects = _populate(Subject)

    for subject in subjects:
        subject.course = courses[0]
    save_all(CourseDataManager(), courses)
    save_all(StudentDataManager(), students)
    save_all(SubjectDataManager(), subjects)
    save_all(TeacherDataManager(), teachers)


def _populate(obj_type: type[AbstractCoreObject]) -> list[AbstractCoreObject]:
    objs = []
    for _ in RANGE:
        objs.append(obj_type(""))
    return objs


def save_all(data_manager: BaseCoreDataManager, objs: list[AbstractCoreObject]):
    data_manager.clear()
    data_manager.save_objects(objs)


@cli.command()
def list_db():
    _list_db(StudentDataManager())
    _list_db(SubjectDataManager())
    _list_db(CourseDataManager())
    _list_db(TeacherDataManager())


@cli.command()
@click.option(
    "--nui",
    prompt="Inform NUI",
    help="NUI.",
)
def info(nui):
    result = "Not found"
    dms = [StudentDataManager, SubjectDataManager, CourseDataManager, TeacherDataManager]
    for dm in dms:
        try:
            result = dm().load_by_nui(nui)
            click.echo(f"{result.__class__.__name__} {vars(result)}")
            return
        except Exception:
            pass
    click.echo(result)


###

# NUI 7727150366633
cli.add_command(student_cmd)
cli.add_command(teacher_cmd)
cli.add_command(init_db)
if __name__ == "__main__":
    cli()
