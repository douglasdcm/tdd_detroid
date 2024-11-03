from src.utils.sql_client import SqlClient
from src.schemes.student import AlunoBd
from src.models.aluno import AlunoModelo


class Students:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def lanca_nota(self, aluno_id, materia_id, nota):
        aluno = AlunoModelo(self._conn)
        aluno.id = aluno_id
        aluno.lanca_nota(materia_id, nota)

    def inscreve_curso(self, aluno_id, curso_id):
        aluno = AlunoModelo(self._conn)
        aluno.id = aluno_id
        aluno.inscreve_curso(curso_id)

    def inscreve_materia(self, aluno_id, materia_id):
        aluno = AlunoModelo(self._conn)
        aluno.id = aluno_id
        return aluno.inscreve_materia(materia_id)

    def cria(self, nome):
        AlunoModelo(self._conn).cria(nome)

    def lista_tudo(self):
        return self._conn.lista_tudo(AlunoBd)

    def lista(self, id_):
        return self._conn.lista(AlunoBd, id_)
