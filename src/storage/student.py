from src.schemes.for_association import MateriaAlunoBd
from src.utils.exceptions import ErroAluno, ErroBancoDados
from src.utils.sql_client import SqlClient
from sqlalchemy.orm import Query
from src.schemes.student import AlunoBd


class StudentStorage:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def __get_student(self, aluno_id):
        try:
            return self._conn.lista(AlunoBd, aluno_id)
        except ErroBancoDados:
            raise ErroAluno(f"Aluno {aluno_id} não existe")

    def __get_disciplines_of_student(self, aluno_id):
        query = Query(MateriaAlunoBd).filter(
            MateriaAlunoBd.aluno_id == aluno_id,
        )
        mas = self._conn.roda_query(query)
        return mas

    def get_maximum_id(self):
        return self._conn.lista_maximo(AlunoBd).id

    def create(self, nome):
        aluno = AlunoBd(nome=nome)
        self._conn.cria(aluno)

    def calculate_coef_rend(self, aluno_id):
        mas = self.__get_disciplines_of_student(aluno_id)
        conta = 0
        soma_nota = 0
        for ma in mas:
            if ma.aluno_nota:
                soma_nota += ma.aluno_nota
                conta += 1
        aluno = self.__get_student(aluno_id)
        aluno.coef_rend = int(round(soma_nota / conta, 1))
        self._conn.update()

    def update_grade(self, aluno_id, materia_id, grade):
        query = Query(MateriaAlunoBd).filter(
            MateriaAlunoBd.aluno_id == aluno_id,
            MateriaAlunoBd.materia_id == materia_id,
        )
        mas = self._conn.roda_query(query)
        mas[0].aluno_nota = grade
        self._conn.update()

    def check_student_in_discipline(self, aluno_id, materia_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        for instancia in resultado:
            if instancia.aluno_id == int(aluno_id) and instancia.materia_id == int(
                materia_id
            ):
                return
        raise ErroAluno(f"Aluno {aluno_id} não está inscrito na matéria {materia_id}")
