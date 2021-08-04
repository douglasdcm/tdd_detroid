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
from tests.massa_dados import aluno_nome_1, curso_nome_1, materia_nome_1, \
    materia_nome_2, materia_nome_3


class TestDaoInscricaoAlunoCurso:

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco):
        self.aluno_id = self.curso_id = "1"
        self.dao = DaoInscricao(InscricaoAlunoCurso(Aluno(), Curso()), cria_banco)

    def test_excecao_retornada_quando_curso_id_nao_existe(self, cria_banco):
        aluno = Aluno(aluno_nome_1).define_id(self.aluno_id)
        DaoAluno(aluno, cria_banco).salva()
        with raises(Exception, match="Curso não encontrado."):
            DaoInscricao(InscricaoAlunoCurso(aluno, Curso()), cria_banco).salva()

    def test_excecao_retornada_quando_aluno_id_nao_existe(self, cria_banco):
        curso = Curso(curso_nome_1).define_id(self.curso_id)
        DaoCurso(curso, cria_banco).salva()
        with raises(Exception, match="Aluno não encontrado."):
            DaoInscricao(InscricaoAlunoCurso(Aluno(), curso), cria_banco).salva()

    def test_inscricao_aluno_curso_pode_ser_criado_banco_dados(self, cria_banco):
        id_ = 1
        aluno = Aluno(aluno_nome_1).define_id(id_)
        DaoAluno(aluno, cria_banco).salva()

        curso = Curso(curso_nome_1).define_id(id_)
        DaoCurso(curso, cria_banco).salva()

        materias = [materia_nome_1, materia_nome_2, materia_nome_3]
        for materia in materias:
            materia_obj = Materia(materia)
            DaoMateria(materia_obj, cria_banco).salva()
            associa_curso_materia = AssociaCursoMateria(curso, materia_obj)
            DaoAssociaCursoMateria(associa_curso_materia, cria_banco).salva()

        expected = [tuple((1, self.aluno_id, self.curso_id))]
        dao = DaoInscricao(InscricaoAlunoCurso(aluno, curso), cria_banco)
        dao.salva()
        actual = dao.pega_tudo()
        assert actual == expected
