from src.dao import dao_aluno
from src.exceptions.exceptions import (
    AlunoNaoEncontrado,
    CursoNaoEncontrado,
    ErroBancoDados,
)
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.model.curso import Curso
from src.dao.dao_base import DaoBase
from src.tabelas import inscricao_aluno_curso, alunos, cursos
from src.model.banco_dados import BancoDados
from src.controller import controller
from typing import List
from src.dao import dao_curso, dao_aluno
from src.model import aluno, curso


class DaoInscricao(DaoBase):
    def __init__(self, inscricao: InscricaoAlunoCurso, bd: BancoDados):
        self.__db = bd
        self.__tabela = inscricao_aluno_curso
        self._campo_1 = "aluno_id"
        self._campo_2 = "curso_id"
        self._campos = f"{self._campo_1}, {self._campo_2}"
        self._complemento = f"FOREIGN KEY({self._campo_1}) REFERENCES {alunos}(id), \
                FOREIGN KEY({self._campo_2}) REFERENCES {cursos}(id)"
        if inscricao is None:
            inscricao = InscricaoAlunoCurso()
        self._inscricao = inscricao
        self.__subscription = inscricao
        super().__init__(self.__db, self.__tabela, self._campos, self._complemento)

    def get_by_student_id(self, id_):
        rows = self.__db.get_by_query(
            "select * from {} where aluno_id = {}".format(self.__tabela, id_)
        )
        return self.__tuple_to_object(rows)[0]

    def get_by_course_id(self, id_):
        rows = self.__db.get_by_query(
            "select * from {} where curso_id = {}".format(self.__tabela, id_)
        )
        return self.__tuple_to_object(rows)

    def save(self):
        return self.salva()

    def get_by_biggest_id(self):
        return self.__tuple_to_object(super().get_by_biggest_id())[0]

    def salva(self):
        try:
            self.__valida_valores()
            student = self.__subscription.pega_aluno()

            course = dao_curso.DaoCurso(Curso(), self.__db).get_by_id(
                self.__subscription.pega_curso().pega_id()
            )

            valores = f"'{student.pega_id()}', \
                '{course.pega_id()}'"
            self.__db.salva_registro(self.__tabela, self._campos, valores)

            student.inscreve_curso(course)

            self.__subscription.atualiza_aluno(student)
            self.__subscription.atualiza_curso(course)

            controller.Controller(student, self.__db).update(student.pega_id())

            return True

        except AlunoNaoEncontrado:
            raise AlunoNaoEncontrado("Aluno não encontrado.")
        except CursoNaoEncontrado:
            raise CursoNaoEncontrado("Curso não encontrado.")
        except Exception as e:
            raise ErroBancoDados(e)

    def __valida_valores(self):
        try:
            self.__db.pega_registro_por_id(
                alunos, self._inscricao.pega_aluno().pega_id()
            )
        except Exception:
            raise AlunoNaoEncontrado
        try:
            self.__db.pega_registro_por_id(
                cursos, self._inscricao.pega_curso().pega_id()
            )
        except Exception:
            raise CursoNaoEncontrado

    def __tuple_to_object(self, rows) -> List[InscricaoAlunoCurso]:
        # assoc_list = []
        for row in rows:
            # local_assoc = InscricaoAlunoCurso()
            (id_, student_id, course_id) = row
            student = dao_aluno.DaoAluno(aluno.Aluno(), self.__db).get_by_id(student_id)
            course = dao_curso.DaoCurso(curso.Curso(), self.__db).get_by_id(course_id)
            self.__subscription.subscribe(student, course)
            # assoc_list.append(local_assoc)
        return self.__subscription
