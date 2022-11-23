from src.utils.sql_client import SqlClient
from src.esquemas.aluno import AlunoBd
from src.modelos.aluno import AlunoModelo


class Alunos:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def inscreve_curso(self, aluno_id, curso_id):
        AlunoModelo(self._conn, aluno_id).inscreve_curso(curso_id)

    def inscreve_materia(self, aluno_id, materia_id):
        AlunoModelo(self._conn, aluno_id).inscreve_materia(materia_id)

    def cria(self, nome):
        AlunoModelo(self._conn).cria(nome)

    def lista_tudo(self):
        return self._conn.lista_tudo(AlunoBd)

    def lista(self, id_):
        return self._conn.lista(AlunoBd, id_)
