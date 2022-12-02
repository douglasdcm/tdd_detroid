import click
from src.materias import Materias, MateriaBd
from src.config import conn


@click.group()
def materia():
    # do nothing #
    pass


@materia.command()
@click.option("--nome", required=True, help="Nome da materia")
<<<<<<< HEAD
@click.option("--curso", type=int, required=True, help="Identificador do curso")
def cria(nome, curso):
    try:
        Materias(conn).cria(nome, curso)
=======
@click.option("--curso-id", type=int, required=True, help="Identificador do curso")
def cria(nome, curso_id):
    try:
        Materias(conn).cria(nome, curso_id)
>>>>>>> Primeira versao da UI com PyScript
        id_ = conn.lista_maximo(MateriaBd).id
        click.echo(f"Materia definida: id {id_}, nome {nome}")
    except Exception as e:
        click.echo(e)
