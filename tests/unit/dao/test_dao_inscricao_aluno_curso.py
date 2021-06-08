from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.dao.dao_inscricao import DaoInscricao
from pytest import raises, fixture
from src.controller.controller import Controller

class TestDaoInscricaoAlunoCurso:

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco):
        self.aluno_id = "1" 
        self.curso_id = "1"
        self.dao = DaoInscricao(InscricaoAlunoCurso(self.aluno_id, self.curso_id), cria_banco)

    def test_excecao_retornada_quando_curso_id_nao_existe(self, cria_aluno_em_memoria):
        with raises(Exception, match="Curso não encontrado."):
            self.dao.salva()

    def test_excecao_retornada_quando_aluno_id_nao_existe(self, cria_curso_com_materias):
        with raises(Exception, match="Aluno não encontrado."):
            self.dao.salva()

    def test_inscricao_aluno_curso_pode_ser_criado_banco_dados(self, cria_massa_dados_em_memoria):
        expected = [tuple((1, self.aluno_id, self.curso_id))]
        self.dao.salva()
        actual = self.dao.pega_tudo()
        assert actual == expected