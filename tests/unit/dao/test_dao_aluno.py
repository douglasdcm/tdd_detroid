from src.controller.controller import Controller
from _pytest.fixtures import add_funcarg_pseudo_fixture_def
from src.dao.dao_aluno import DaoAluno
from tests.conftest import cria_curso_com_materias
from src.dao.dao_fabrica import DaoFabrica
from tests.massa_dados import aluno_nome_1
from src.enums.enums import Situacao

class TestDaoAluno:

    def test_aluno_pode_ser_salvo_banco_dados(self, cria_banco, cria_aluno):
        cr = 0
        situacao = Situacao.em_curso.value
        expected = [tuple((1, aluno_nome_1, cr, situacao))]
        actual = self._salva_aluno_banco(cria_banco, cria_aluno)
        assert actual == expected

    def _salva_aluno_banco(self, cria_banco, cria_aluno):
        bd = cria_banco
        dao = DaoAluno(cria_aluno, bd)
        dao.salva()
        return dao.pega_tudo()

