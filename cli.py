import click
from src.cursos import Cursos, Curso
from src.config import NOME_BANCO
from src.alunos import Alunos, Aluno
from src.utils import limpa_tabelas
from src.sql_client import SqlClient
from src.materias import Materias, Materia

conn = SqlClient(NOME_BANCO)


@click.group()
def cli():
    # do nothing #
    pass


@cli.command()
def init_bd():
    limpa_tabelas(conn)
    print("Banco de dados inicializado")


@cli.command()
@click.option("--nome", required=True, help="Nome da materia")
@click.option("--curso", type=int, required=True, help="Identificador do curso")
def define_materia(nome, curso):
    Materias(conn).cria(nome, curso)
    id_ = conn.lista_maximo(Materia).id
    print(f"Materia definida: id {id_}, nome {nome}")


@cli.command()
@click.option("--nome", required=True, help="Nome do aluno")
def define_aluno(nome):
    Alunos(conn).cria(nome)
    id_ = conn.lista_maximo(Aluno).id
    print(f"Aluno definido: id {id_}, nome {nome}")


@cli.command()
@click.option("--nome", required=True, help="Nome do curso")
def define_curso(nome):
    Cursos(conn).cria(nome)
    id_ = conn.lista_maximo(Curso).id
    print(f"Curso definido: id {id_}, nome {nome}")


if __name__ == "__main__":
    cli()
