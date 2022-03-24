from src.dao.dao_curso import DaoCurso
from src.dao.dao_inscricao import DaoInscricao
from src.model.aluno import Aluno
from src.model.banco_dados import BancoDados
from src.dao.dao_base import DaoBase
from src.model.curso import Curso
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.tabelas import students
from typing import List


class DaoAluno(DaoBase):
    def __init__(self, aluno: Aluno, bd: BancoDados):
        self.__db = bd
        self.__tabela = students
        self.campo_1 = "name"
        self.campo_2 = "score"
        self.campo_3 = "situation"
        self._campos = f"{self.campo_1}, {self.campo_2}, {self.campo_3}"
        self._aluno = aluno
        self.__student = aluno
        super().__init__(self.__db, self.__tabela, self._campos)

    def salva(self):
        """Retorna objeto com campos atualizados via banco de dados"""
        self.__db.salva_registro(
            self.__tabela,
            self._campos,
            (
                f"'{self._aluno.pega_nome()}', "
                f"{self._aluno.pega_coeficiente_rendimento()}, "
                f"'{self._aluno.pega_situacao()}'"
            ),
        )
        return True

    def atualiza(self, id_):
        query = f"{self.campo_2} = {self._aluno.pega_coeficiente_rendimento()}"

        if isinstance(self._aluno.pega_nome(), str):
            query += f", {self.campo_1} = '{self._aluno.pega_nome()}'"

        if isinstance(self._aluno.pega_situacao(), str):
            query += f", {self.campo_3} = '{self._aluno.pega_situacao()}'"

        self.__db.atualiza_registro(self.__tabela, query, id_)
        return True

    def get_by_id(self, id_):
        return self.pega_por_id(id_)

    def pega_por_id(self, id_):
        """
        Args:
            id (int): identificador do aluno
        Returns:
            objeto aluno com dados pegos do banco de dados
        """
        linha = super().pega_por_id(id_)
        return self.__tuple_to_object(linha[0])

    def pega_tudo(self):
        registros = super().pega_tudo()
        lista_alunos = list()
        for linha in registros:
            aluno = self.__tuple_to_object(linha)
            lista_alunos.append(aluno)
        return lista_alunos

    def get_all(self):
        return self.pega_tudo()

    def get_by_name(self, name):
        rows = super().get_by_name(name)
        students = []
        for row in rows:
            students.append(self.__tuple_to_object(row))
        return students

    def get_by_biggest_id(self):
        row = super().get_by_biggest_id()[0]
        return self.__tuple_to_object(row)

    def __tuple_to_object(self, rows) -> List[Aluno]:
        (id_, name, cr, status) = rows
        self.__student.define_id(id_)
        self.__student.define_nome(name)
        self.__student.define_cr(cr)

        assocs = DaoInscricao(InscricaoAlunoCurso(), self.__db).get_by_student_id(id_)
        for assoc in assocs:
            self.__student.inscreve_curso(
                DaoCurso(Curso(), self.__db).pega_por_id(assoc.get_course_id())
            )

        self.__student.define_situacao(status)
        return self.__student
