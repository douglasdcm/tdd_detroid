import click
from src.disciplines import Disciplines, MateriaBd
from src.config import conn_external


@click.group()
def materia():
    # do nothing #
    pass


@materia.command()
@click.option("--nome", required=True, help="Discipline name")
@click.option("--curso-id", type=int, required=True, help="Cours identification")
def create(nome, curso_id):
    try:
        Disciplines(conn_external).create(nome, curso_id)
        id_ = conn_external.lista_maximo(MateriaBd).id
        click.echo(f"Materia definida: id {id_}, nome {nome}")
    except Exception as e:
        click.echo(e)
