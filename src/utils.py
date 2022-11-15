from src.banco_dados import BancoDados as bd
from src.banco_dados import Tabela
from src.manager import Tipos


def create_tables(conn: bd):
    try:
        # precisa deletar as materias antes de deletar o curso
        conn.deleta_tabela(Tipos.MATERIAS.value)
        conn.deleta_tabela(Tipos.CURSOS.value)
        conn.deleta_tabela(Tipos.ALUNOS.value)
    except:
        pass

    cursos = Tabela(Tipos.CURSOS.value)
    cursos.colunas = ["nome"]
    conn.cria_tabela(cursos)

    alunos = Tabela(Tipos.ALUNOS.value)
    alunos.colunas = ["nome"]
    conn.cria_tabela(alunos)

    materias = Tabela(Tipos.MATERIAS.value)
    materias.colunas = ["nome", "curso"]
    materias.chave_estrangeira = ("curso", Tipos.CURSOS.value, "id")
    conn.cria_tabela(materias)
