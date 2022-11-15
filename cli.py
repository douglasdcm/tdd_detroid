import click
from src.cursos import Cursos
from src.banco_dados import BancoDados as bd
from src.config import NOME_BANCO
from src.alunos import Alunos
from src.materias import Materias
from src.utils import create_tables
from src.manager import Tipos

conn = bd(NOME_BANCO)


@click.group()
def cli():
    # do nothing #
    pass


@cli.command()
def init_bd():
    create_tables(conn)
    print("Banco de dados inicializado")


@cli.command()
@click.option("--nome", required=True, help="Nome da materia")
@click.option("--curso", type=int, required=True, help="Identificador do curso")
def define_materia(nome, curso):
    Materias(conn).cria(nome, curso)
    id_ = conn.lista_maximo(Tipos.MATERIAS.value)[0][0]
    print(f"Materia definida: id {id_}, nome {nome}")


@cli.command()
@click.option("--nome", required=True, help="Nome do aluno")
def define_aluno(nome):
    Alunos(conn).cria(nome)
    id_ = conn.lista_maximo(Tipos.ALUNOS.value)[0][0]
    print(f"Aluno definido: id {id_}, nome {nome}")


@cli.command()
@click.option("--nome", required=True, help="Nome do curso")
def define_curso(nome):
    Cursos(conn).cria(nome)
    id_ = conn.lista_maximo(Tipos.CURSOS.value)[0][0]
    print(f"Curso definido: id {id_}, nome {nome}")


if __name__ == "__main__":
    cli()
