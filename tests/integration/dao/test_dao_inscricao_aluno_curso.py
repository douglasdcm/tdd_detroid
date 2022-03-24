from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.materia import Materia
from src.dao.dao_aluno import DaoAluno
from src.dao.dao_curso import DaoCurso
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.dao.dao_inscricao import DaoInscricao
from src.dao.dao_materia import DaoMateria
from src.dao.dao_associa_curso_materia import DaoAssociaCursoMateria
from pytest import raises, fixture
from tests.massa_dados import (
    aluno_nome_1,
    curso_nome_1,
    materia_nome_1,
    materia_nome_2,
    materia_nome_3,
)
from src.model.banco_dados import BancoDados


class TestDaoInscricaoAlunoCurso:
    @fixture(autouse=True, scope="function")
    def setup(self, setup_database_in_memory):
        self.aluno_id = self.curso_id = "1"
        self.dao = DaoInscricao(
            InscricaoAlunoCurso(Aluno(), Curso()), setup_database_in_memory
        )

    def test_should_return_student_id_when_enrolement_in_course(
        self, setup_database_in_memory
    ):
        expected = 1
        actual = len(
            DaoInscricao(
                InscricaoAlunoCurso(), BancoDados(setup_database_in_memory)
            ).get_by_student_id(1)
        )

        assert actual == expected

    def test_excecao_retornada_quando_curso_id_nao_existe(
        self, setup_database_in_memory
    ):
        aluno = Aluno(aluno_nome_1).define_id(self.aluno_id)
        DaoAluno(aluno, setup_database_in_memory).salva()
        with raises(Exception, match="Curso não encontrado."):
            DaoInscricao(
                InscricaoAlunoCurso(aluno, Curso()), setup_database_in_memory
            ).salva()

    def test_excecao_retornada_quando_aluno_id_nao_existe(
        self, setup_database_in_memory
    ):
        curso = Curso(curso_nome_1).define_id(self.curso_id)
        DaoCurso(curso, setup_database_in_memory).salva()
        with raises(Exception, match="Aluno não encontrado."):
            DaoInscricao(
                InscricaoAlunoCurso(Aluno(), curso), setup_database_in_memory
            ).salva()

    def test_inscricao_aluno_curso_pode_ser_criado_banco_dados(
        self, setup_database_in_memory
    ):
        id_ = 1
        aluno = Aluno(aluno_nome_1).define_id(id_)
        DaoAluno(aluno, setup_database_in_memory).salva()

        curso = Curso(curso_nome_1).define_id(id_)
        DaoCurso(curso, setup_database_in_memory).salva()

        materias = [materia_nome_1, materia_nome_2, materia_nome_3]
        for materia in materias:
            materia_obj = Materia(materia)
            materia_obj = DaoMateria(materia_obj, setup_database_in_memory).salva()
            associa_curso_materia = AssociaCursoMateria(curso, materia_obj)
            DaoAssociaCursoMateria(
                associa_curso_materia, setup_database_in_memory
            ).salva()

        expected = [tuple((1, self.aluno_id, self.curso_id))]
        dao = DaoInscricao(InscricaoAlunoCurso(aluno, curso), setup_database_in_memory)
        dao.salva()
        actual = dao.pega_tudo()
        assert actual == expected
