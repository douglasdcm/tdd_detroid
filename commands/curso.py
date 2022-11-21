import click
from src.cursos import Cursos, Curso
from config import conn


@click.group()
def curso():
    # do nothing #
    pass


@curso.command()
@click.option("--nome", required=True, help="Nome do curso")
def cria(nome):
    try:
        Cursos(conn).cria(nome)
        id_ = conn.lista_maximo(Curso).id
        click.echo(f"Curso definido: id {id_}, nome {nome}")
    except Exception as e:
        click.echo(e)
