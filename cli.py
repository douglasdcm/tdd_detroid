import click
from src.utils import limpa_tabelas
from config import conn
from commands.aluno import aluno
from commands.materia import materia
from commands.curso import curso


@click.group()
def cli():
    # do nothing #
    pass


@cli.command()
def init_bd():
    limpa_tabelas(conn)
    click.echo("Banco de dados inicializado")


cli.add_command(aluno)
cli.add_command(materia)
cli.add_command(curso)


if __name__ == "__main__":
    cli()
