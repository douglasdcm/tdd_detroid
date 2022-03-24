from src.exceptions.exceptions import (
    AlunoNaoEncontrado,
    CursoNaoEncontrado,
    ErroBancoDados,
)
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.dao.dao_base import DaoBase
from src.tabelas import inscricao_aluno_curso, alunos, cursos
from src.model.banco_dados import BancoDados
from src.controller import controller
from typing import List


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
        self.__enrollment = inscricao
        super().__init__(self.__db, self.__tabela, self._campos, self._complemento)

    def get_by_student_id(self, id_):
        rows = self.__db.get_by_query(
            "select * from {} where aluno_id = {}".format(self.__tabela, id_)
        )
        return self.__tuple_to_object(rows)

    def save(self):
        return self.salva()

    def salva(self):
        try:
            self._valida_valores()
            student_obj = self.__enrollment.pega_aluno()
            course_obj = self.__enrollment.pega_curso()

            valores = f"'{student_obj.pega_id()}', \
                '{course_obj.pega_id()}'"
            self.__db.salva_registro(self.__tabela, self._campos, valores)

            student_obj.inscreve_curso(course_obj)

            self.__enrollment.atualiza_aluno(student_obj)
            self.__enrollment.atualiza_curso(course_obj)

            controller.Controller(student_obj, self.__db).update(student_obj.pega_id())
            # controller.Controller(course_obj, self.__db).upd  ate(course_obj.pega_id())

            return True

        except AlunoNaoEncontrado:
            raise AlunoNaoEncontrado("Aluno não encontrado.")
        except CursoNaoEncontrado:
            raise CursoNaoEncontrado("Curso não encontrado.")
        except Exception as e:
            raise ErroBancoDados(e)

    def _valida_valores(self):
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
        assoc_list = []
        for row in rows:
            local_assoc = InscricaoAlunoCurso()
            (id_, student_id, course_id) = row
            local_assoc.update_student_id(student_id)
            local_assoc.update_course_id(course_id)
            assoc_list.append(local_assoc)
        return assoc_list
