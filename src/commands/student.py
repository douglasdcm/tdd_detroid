import click
from src.sdk.students import Students
from src.schemes.student import AlunoBd
from src.config import conn


@click.group()
def aluno():
    # do nothing #
    pass


@aluno.command()
@click.option("--aluno-id", type=int, required=True, help="Student identification")
@click.option("--materia-id", type=int, required=True, help="Discipline ientification")
@click.option("--nota", type=int, required=True, help="Student grade")
def lanca_nota(aluno_id, materia_id, nota):
    try:
        Students(conn).set_grade(aluno_id, materia_id, nota)
        click.echo(
            f"Nota {nota} do aluno {aluno_id} na materia {materia_id} lancada com sucesso"
        )
    except Exception as e:
        click.echo(e)


@aluno.command()
@click.option("--aluno-id", type=int, required=True, help="Student identification")
@click.option("--materia-id", type=int, required=True, help="Discipline identification")
def inscreve_materia(aluno_id, materia_id):
    try:
        Students(conn).subscribe_in_discipline(aluno_id, materia_id)
        click.echo(f"Aluno {aluno_id} inscrito na materia {materia_id}")
    except Exception as e:
        click.echo(e)


@aluno.command()
@click.option("--nome", required=True, help="Student name")
def cria(nome):
    Students(conn).create(nome)
    id_ = conn.lista_maximo(AlunoBd).id
    click.echo(f"Aluno definido: id {id_}, nome {nome}")


@aluno.command()
@click.option("--aluno-id", type=int, required=True, help="Student identification")
@click.option("--curso-id", type=int, required=True, help="Course identification")
def inscreve_curso(aluno_id, curso_id):
    try:
        Students(conn).subscribe_in_course(aluno_id, curso_id)
        click.echo(f"Aluno inscrito no curso {curso_id}")
    except Exception as e:
        click.echo(e)
