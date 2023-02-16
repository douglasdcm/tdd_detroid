import click
from src.courses import Courses
from src.schemes.course import CursoBd
from src.config import conn_external


@click.group()
def curso():
    # do nothing #
    pass


@curso.command()
@click.option("--nome", required=True, help="Course name")
def cria(nome):
    try:
        Courses(conn_external).cria(nome)
        id_ = conn_external.lista_maximo(CursoBd).id
        click.echo(f"Curso definido: id {id_}, nome {nome}")
    except Exception as e:
        click.echo(e)
