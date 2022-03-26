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
        id_ = 1
        with raises(Exception, match="Curso não encontrado."):
            DaoInscricao(
                InscricaoAlunoCurso(Aluno().define_id(id_), Curso()),
                BancoDados(setup_database_in_memory),
            ).salva()

    def test_excecao_retornada_quando_aluno_id_nao_existe(
        self, setup_database_in_memory
    ):
        id_ = 1
        curso = Curso(curso_nome_1).define_id(id_)
        with raises(Exception, match="Aluno não encontrado."):
            DaoInscricao(
                InscricaoAlunoCurso(Aluno(), curso), setup_database_in_memory
            ).salva()

    def test_inscricao_aluno_curso_pode_ser_criado_banco_dados(
        self, setup_database_in_memory
    ):
        student_id = 2
        course_id = 1
        expected = student_id
        dao = DaoInscricao(
            InscricaoAlunoCurso(
                Aluno().define_id(student_id), Curso().define_id(course_id)
            ),
            BancoDados(setup_database_in_memory),
        )
        dao.salva()
        actual = dao.get_by_biggest_id().get_student_id()
        assert actual == expected
