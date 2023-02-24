import click
from src.utils.utils import inicializa_tabelas
from src.commands.student import aluno
from src.commands.discipline import materia
from src.commands.course import curso


@click.group()
def cli():
    # do nothing #
    pass


@cli.command()
def init_bd():
    inicializa_tabelas()
    click.echo("Database initialized")


cli.add_command(aluno)
cli.add_command(materia)
cli.add_command(curso)


if __name__ == "__main__":
    cli()
