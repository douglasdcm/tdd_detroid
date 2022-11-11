from sys import argv
from src.cursos import Cursos
from src.banco_dados import BancoDados as bd
from src.config import NOME_BANCO
from src.banco_dados import Tabela

conn = bd(NOME_BANCO)


def main(*args):
    cursos = Tabela(Cursos)
    cursos.colunas = "nome"
    conn.cria_tabela(cursos)

    linha_cmd = args[0]
    comando = linha_cmd[1]
    comandos = {"define_curso": define_curso}
    comandos[comando](linha_cmd[2:])


def define_curso(args):
    Cursos(conn).cria(args[1])
    print(f"Curso definido: id {args[0]}, nome {args[1]}")


if __name__ == "__main__":
    main(argv)
