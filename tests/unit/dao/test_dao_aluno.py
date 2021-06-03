from src.dao.dao_aluno import DaoAluno
from tests.conftest import cria_curso_com_materias
from src.dao.dao_fabrica import DaoFabrica
from tests.massa_dados import aluno_nome_1

class TestDaoAluno:

    def test_aluno_pode_ser_salvo_banco_dados(self, cria_banco, cria_aluno):        
        bd = cria_banco
        expected = {1: aluno_nome_1}
        dao = DaoAluno(cria_aluno, bd)
        dao.salva()
        actual = dao.pega_tudo()
        assert actual == expected
