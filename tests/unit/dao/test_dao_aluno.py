from tests.conftest import cria_curso_com_materias
from src.dao.dao_fabrica import DaoFabrica

class TestDaoAluno:

    def test_aluno_pode_ser_salvo_banco_dados(self, cria_banco, cria_aluno):        
        bd = cria_banco
        nome = "José"
        expected = [tuple((1, nome))]
        dao = DaoFabrica(cria_aluno, bd)
        dao_aluno = dao.fabrica_objetos_dao()
        dao_aluno.salva()
        actual = dao_aluno.pega_tudo()
        assert actual == expected
