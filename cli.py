import click
from src.utils.utils import inicializa_tabelas
from config import conn
from src.commands.aluno import aluno
from src.commands.materia import materia
from src.commands.curso import curso


@click.group()
def cli():
    # do nothing #
    pass


@cli.command()
def init_bd():
    inicializa_tabelas(conn)
    click.echo("Banco de dados inicializado")


cli.add_command(aluno)
cli.add_command(materia)
cli.add_command(curso)


if __name__ == "__main__":
    cli()
