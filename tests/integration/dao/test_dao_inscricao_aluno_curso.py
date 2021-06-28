from src.dao.dao_aluno import DaoAluno
from src.dao.dao_curso import DaoCurso
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.dao.dao_inscricao import DaoInscricao
from pytest import raises, fixture
from tests.massa_dados import aluno_nome_1, curso_nome_1


class TestDaoInscricaoAlunoCurso:

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco):
        self.aluno_id = "1"
        self.curso_id = "1"
        self.dao = DaoInscricao(InscricaoAlunoCurso(self.aluno_id,
                                                    self.curso_id),
                                cria_banco)

    def test_excecao_retornada_quando_curso_id_nao_existe(self, cria_banco):
        aluno = Aluno(aluno_nome_1).define_id(self.aluno_id)
        DaoAluno(aluno, cria_banco).salva()
        with raises(Exception, match="Curso não encontrado."):
            self.dao.salva()

    def test_excecao_retornada_quando_aluno_id_nao_existe(self):
        with raises(Exception, match="Aluno não encontrado."):
            self.dao.salva()

    def test_inscricao_aluno_curso_pode_ser_criado_banco_dados(self, cria_banco):
        id_ = 1
        DaoAluno(Aluno(aluno_nome_1).define_id(id_), cria_banco).salva()
        DaoCurso(Curso(curso_nome_1).define_id(id_), cria_banco).salva()
        expected = [tuple((1, self.aluno_id, self.curso_id))]
        self.dao.salva()
        actual = self.dao.pega_tudo()
        assert actual == expected
