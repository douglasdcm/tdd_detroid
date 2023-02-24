import click
from src.controllers import disciplines


@click.group()
def materia():
    # do nothing #
    pass


@materia.command()
@click.option("--nome", required=True, help="Discipline name")
@click.option("--curso-id", type=int, required=True, help="Cours identification")
def create(nome, curso_id):
    try:
        disciplines.create(nome, curso_id)
        id_ = disciplines.get_maximum().id
        click.echo(f"Materia definida: id {id_}, nome {nome}")
    except Exception as e:
        click.echo(e)
