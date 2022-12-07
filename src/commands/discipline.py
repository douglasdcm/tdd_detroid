import click
from src.disciplines import Materias, MateriaBd
from src.config import conn


@click.group()
def materia():
    # do nothing #
    pass


@materia.command()
@click.option("--nome", required=True, help="Discipline name")
@click.option("--curso-id", type=int, required=True, help="Cours identification")
def cria(nome, curso_id):
    try:
        Materias(conn).cria(nome, curso_id)
        id_ = conn.lista_maximo(MateriaBd).id
        click.echo(f"Materia definida: id {id_}, nome {nome}")
    except Exception as e:
        click.echo(e)
