import click
from src.controllers import students
from src.schemes.student import StudentDB
from src.utils import sql_client


@click.group()
def aluno():
    # do nothing #
    pass


@aluno.command()
@click.option("--student-id", type=int, required=True, help="Student identification")
@click.option("--discipline-id", type=int, required=True, help="Discipline ientification")
@click.option("--nota", type=int, required=True, help="Student grade")
def lanca_nota(student_id, discipline_id, nota):
    try:
        students.set_grade(student_id, discipline_id, nota)
        click.echo(
            f"Nota {nota} do aluno {student_id} na materia {discipline_id} lancada com sucesso"
        )
    except Exception as e:
        click.echo(e)


@aluno.command()
@click.option("--student-id", type=int, required=True, help="Student identification")
@click.option("--discipline-id", type=int, required=True, help="Discipline identification")
def inscreve_materia(student_id, discipline_id):
    try:
        students.subscribe_in_discipline(student_id, discipline_id)
        click.echo(f"Aluno {student_id} inscrito na materia {discipline_id}")
    except Exception as e:
        click.echo(e)


@aluno.command()
@click.option("--name", required=True, help="Student name")
def create(name):
    students.create(name)
    id_ = sql_client.get_maximum(StudentDB).id
    click.echo(f"Aluno definido: id {id_}, name {name}")


@aluno.command()
@click.option("--student-id", type=int, required=True, help="Student identification")
@click.option("--course-id", type=int, required=True, help="Course identification")
def inscreve_course(student_id, course_id):
    try:
        students.subscribe_in_course(student_id, course_id)
        click.echo(f"Aluno inscrito no course {course_id}")
    except Exception as e:
        click.echo(e)
