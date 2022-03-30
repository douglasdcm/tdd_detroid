from src.dao.dao_inscricao import DaoInscricao
from src.model.curso import Curso
from src.dao.dao_base import DaoBase
from src.model.banco_dados import BancoDados
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.tabelas import cursos
from src.dao.dao_associa_curso_materia import DaoAssociaCursoMateria
from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.materia import Materia
from src.dao.dao_materia import DaoMateria
from src.dao import dao_aluno
from src.model.aluno import Aluno


class DaoCurso(DaoBase):
    def __init__(self, curso: Curso, bd: BancoDados):
        self.__db = bd
        self._tabela = cursos
        self._campos = "nome"
        self._curso = curso
        self.__course = curso
        super().__init__(self.__db, self._tabela, self._campos)

    def salva(self):
        """Retorna objeto com campos atualizados via banco de dados"""
        self._curso.pega_lista_materias()
        self.__db.salva_registro(
            self._tabela, self._campos, f"'{self._curso.pega_nome()}'"
        )
        return True

    def pega_tudo(self) -> list():
        registros = super().pega_tudo()
        lista = list()
        for linha in registros:
            (id_, nome) = linha
            curso = Curso(nome)
            curso.define_id(id_)
            lista.append(curso)
        return lista

    def pega_por_nome(self, nome):
        try:
            return self.__tuple_to_object(super().pega_por_nome(nome))
        except Exception:
            raise

    def pega_por_id(self, id) -> Curso:
        """
        Args:
            id (int): identificador do curso
        Returns:
            objeto curso com dados pegos do banco de dados
        """
        linha = super().pega_por_id(id)
        return self.__tuple_to_object(linha[0])

    def get_by_id(self, id_):
        return self.pega_por_id(id_)

    def get_by_biggest_id(self):
        row = super().get_by_biggest_id()[0]
        return self.__tuple_to_object(row)

    def __tuple_to_object(self, row) -> Curso:
        (id_, name) = row
        self.__course.define_id(id_)

        assocs_course_discipline = DaoAssociaCursoMateria(
            AssociaCursoMateria(Curso(), Materia()), self.__db
        ).get_by_course_id(id_)
        for assoc in assocs_course_discipline:
            self.__course.atualiza_materias(
                DaoMateria(Materia(), self.__db).pega_por_id(assoc.pega_materia_id())
            )
        assocs_course_student = DaoInscricao(
            InscricaoAlunoCurso(), self.__db
        ).get_by_course_id(id_)

        for assoc in assocs_course_student:
            self.__course.adiciona_aluno(
                dao_aluno.DaoAluno(Aluno(), self.__db).get_by_id(assoc.get_student_id())
            )
        return self.__course
