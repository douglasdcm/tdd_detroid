from src.schemes.for_association import MateriaAlunoBd
from src.utils.exceptions import ErroAluno, ErroBancoDados, ErroMateriaAluno
from src.utils.sql_client import SqlClient
from sqlalchemy.orm import Query
from src.schemes.student import AlunoBd


class StudentStorage:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn

    def get_student(self, aluno_id):
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

    def get_course_id(self, student_id):
        curso_id = self._conn.lista(AlunoBd, student_id).curso_id
        if not curso_id:
            raise ErroAluno(f"Aluno {student_id} não está inscrito em nenhum curso")
        return curso_id

    def check_student_in_tree_disciplines(self, aluno_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        qtde_materias = 0
        for instancia in resultado:
            if instancia.aluno_id == aluno_id:
                qtde_materias += 1
            if qtde_materias >= 3:
                return
        raise ErroMateriaAluno("Aluno deve se inscrever em 3 materias no minimo")

    def check_student_already_in_discipline(self, aluno_id, materia_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        for instancia in resultado:
            if instancia.aluno_id == int(aluno_id) and instancia.materia_id == int(
                materia_id
            ):
                raise ErroMateriaAluno(
                    f"Aluno {aluno_id} já está inscrito na matéria {materia_id}"
                )

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
        aluno = self.get_student(aluno_id)

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

    def subscribe_in_discipline(self, aluno_id, materia_id):
        ma = MateriaAlunoBd(aluno_id=aluno_id, materia_id=materia_id)
        self._conn.cria(ma)

    def can_subscribe_course(self, aluno_id):
        aluno = self.get_student(aluno_id)
        if aluno.curso_id is not None:
            raise ErroAluno("Aluno esta inscrito em outro curso")

    def check_student_in_discipline(self, aluno_id, materia_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        for instancia in resultado:
            if instancia.aluno_id == int(aluno_id) and instancia.materia_id == int(
                materia_id
            ):
                return
        raise ErroAluno(f"Aluno {aluno_id} não está inscrito na matéria {materia_id}")
