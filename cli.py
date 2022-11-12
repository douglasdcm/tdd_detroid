import click
from src.cursos import Cursos
from src.banco_dados import BancoDados as bd
from src.config import NOME_BANCO
from src.banco_dados import Tabela

conn = bd(NOME_BANCO)


@click.group()
def cli():
    cursos = Tabela(Cursos)
    cursos.colunas = "nome"
    conn.cria_tabela(cursos)


@cli.command()
@click.option("--id", required=True, type=int, help="Identificador do curso")
@click.option("--nome", required=True, help="Nome do curso")
def define_curso(id, nome):
    Cursos(conn).cria(nome)
    # TODO definir apenas o nome e pegar o id do banco
    print(f"Curso definido: id {id}, nome {nome}")


if __name__ == "__main__":
    cli()
