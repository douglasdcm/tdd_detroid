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
@click.option("--materia-id", type=int, required=True, help="Discipline ientification")
@click.option("--nota", type=int, required=True, help="Student grade")
def lanca_nota(student_id, materia_id, nota):
    try:
        students.set_grade(student_id, materia_id, nota)
        click.echo(
            f"Nota {nota} do aluno {student_id} na materia {materia_id} lancada com sucesso"
        )
    except Exception as e:
        click.echo(e)


@aluno.command()
@click.option("--student-id", type=int, required=True, help="Student identification")
@click.option("--materia-id", type=int, required=True, help="Discipline identification")
def inscreve_materia(student_id, materia_id):
    try:
        students.subscribe_in_discipline(student_id, materia_id)
        click.echo(f"Aluno {student_id} inscrito na materia {materia_id}")
    except Exception as e:
        click.echo(e)


@aluno.command()
@click.option("--nome", required=True, help="Student name")
def create(nome):
    students.create(nome)
    id_ = sql_client.get_maximum(StudentDB).id
    click.echo(f"Aluno definido: id {id_}, nome {nome}")


@aluno.command()
@click.option("--student-id", type=int, required=True, help="Student identification")
@click.option("--curso-id", type=int, required=True, help="Course identification")
def inscreve_curso(student_id, curso_id):
    try:
        students.subscribe_in_course(student_id, curso_id)
        click.echo(f"Aluno inscrito no curso {curso_id}")
    except Exception as e:
        click.echo(e)
