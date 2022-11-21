import click
from src.alunos import Alunos, Aluno
from config import conn


@click.group()
def aluno():
    # do nothing #
    pass


@aluno.command()
@click.option("--nome", required=True, help="Nome do aluno")
def cria(nome):
    Alunos(conn).cria(nome)
    id_ = conn.lista_maximo(Aluno).id
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
