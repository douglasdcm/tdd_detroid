import click
from src.alunos import Alunos
from src.esquemas.aluno import AlunoBd
from config import conn


@click.group()
def aluno():
    # do nothing #
    pass


@aluno.command()
@click.option("--aluno-id", required=True, help="Identificador do aluno")
@click.option("--materia-id", required=True, help="Identificador da materia")
def inscreve_materia(aluno_id, materia_id):
    try:
        Alunos(conn).inscreve_materia(aluno_id, materia_id)
        click.echo(f"Aluno {aluno_id} inscrito na materia {materia_id}")
    except Exception as e:
        click.echo(e)


@aluno.command()
@click.option("--nome", required=True, help="Nome do aluno")
def cria(nome):
    Alunos(conn).cria(nome)
    id_ = conn.lista_maximo(AlunoBd).id
    click.echo(f"Aluno definido: id {id_}, nome {nome}")


@aluno.command()
@click.option("--aluno-id", required=True, help="Identificador do aluno")
@click.option("--curso-id", required=True, help="Identificador do curso")
def inscreve_curso(aluno_id, curso_id):
    try:
        Alunos(conn).inscreve_curso(aluno_id, curso_id)
        click.echo(f"Aluno inscrito no curso {curso_id}")
    except Exception as e:
        click.echo(e)
