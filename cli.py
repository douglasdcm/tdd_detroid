import click
from src.cursos import Cursos
from src.banco_dados import BancoDados as bd
from src.config import NOME_BANCO
from src.banco_dados import Tabela
from src.alunos import Alunos

conn = bd(NOME_BANCO)


@click.group()
def cli():
    cursos = Tabela(Cursos)
    cursos.colunas = "nome"
    conn.cria_tabela(cursos)

    alunos = Tabela(Alunos)
    alunos.colunas = "nome"
    conn.cria_tabela(alunos)


@cli.command()
@click.option("--nome", required=True, help="Nome do aluno")
def define_aluno(nome):
    Alunos(conn).cria(nome)
    id_ = conn.lista_maximo(Alunos)[0][0]
    print(f"Aluno definido: id {id_}, nome {nome}")


@cli.command()
@click.option("--nome", required=True, help="Nome do curso")
def define_curso(nome):
    Cursos(conn).cria(nome)
    id_ = conn.lista_maximo(Cursos)[0][0]
    print(f"Curso definido: id {id_}, nome {nome}")


if __name__ == "__main__":
    cli()
