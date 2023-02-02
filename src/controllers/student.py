from src.utils.sql_client import SqlClient
from src.schemes.student import AlunoBd
from src.schemes.for_association import MateriaAlunoBd
from src.controllers.curso import CursoModelo
from src.utils.exceptions import ErroAluno, ErroBancoDados, ErroMateriaAluno
from src.controllers.materia import MateriaModelo
from src.business_logic.student import StudentBL
from src.storage.student import StudentStorage


class StudentController:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn
        self._aluno_id = None
        self._student_bl = StudentBL()
        self._student_storage = StudentStorage(conn)

    @property
    def id(self):
        return self._aluno_id

    @id.setter
    def id(self, valor):
        self._aluno_id = valor
        self.__pega_aluno()

    def set_grade(self, discipline_id, grade):
        grade = int(grade)
        self._student_bl.check_grade_boundaries(grade)
        self._student_storage.check_student_in_discipline(self._aluno_id, discipline_id)
        self._student_storage.update_grade(self._aluno_id, discipline_id, grade)
        self._student_storage.calculate_coef_rend(self._aluno_id)

    def __pega_aluno(self):
        try:
            return self._conn.lista(AlunoBd, self._aluno_id)
        except ErroBancoDados:
            raise ErroAluno(f"Aluno {self._aluno_id} não existe")

    def __verifica_pode_inscrever_curso(self):
        aluno = self.__pega_aluno()
        if aluno.curso_id is not None:
            raise ErroAluno("Aluno esta inscrito em outro curso")

    def __verifica_minimo_3_materias(self, aluno_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        qtde_materias = 0
        for instancia in resultado:
            if instancia.aluno_id == aluno_id:
                qtde_materias += 1
            if qtde_materias >= 3:
                return
        raise ErroMateriaAluno("Aluno deve se inscrever em 3 materias no minimo")

    def __verifica_aluno_ja_inscrito_materia(self, aluno_id, materia_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        for instancia in resultado:
            if instancia.aluno_id == int(aluno_id) and instancia.materia_id == int(
                materia_id
            ):
                raise ErroMateriaAluno(
                    f"Aluno {aluno_id} já está inscrito na matéria {materia_id}"
                )

    def __pega_curso_id(self):
        curso_id = self._conn.lista(AlunoBd, self.id).curso_id
        if not curso_id:
            raise ErroAluno(f"Aluno {self.id} não está inscrito em nenhum curso")
        return curso_id

    def create(self, nome):
        nome = self._student_bl.clear_name(nome)
        self._student_storage.create(nome)
        self._aluno_id = self._student_storage.get_maximum_id()

    def inscreve_materia(self, materia_id):
        curso_id = self.__pega_curso_id()
        MateriaModelo(self._conn).verifica_existencia(materia_id, curso_id)
        self.__verifica_aluno_ja_inscrito_materia(self._aluno_id, materia_id)
        ma = MateriaAlunoBd(aluno_id=self._aluno_id, materia_id=materia_id)
        self._conn.cria(ma)
        self.__verifica_minimo_3_materias(self._aluno_id)

    def inscreve_curso(self, curso_id):
        aluno = self.__pega_aluno()
        CursoModelo(self._conn).verifica_existencia(curso_id)
        self.__verifica_pode_inscrever_curso()
        aluno.curso_id = curso_id
        self._conn.confirma()
