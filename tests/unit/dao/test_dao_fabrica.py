from sqlite3 import connect
from src.model.aluno import Aluno
from src.dao.dao_fabrica import DaoFabrica
from src.dao.dao_aluno import DaoAluno
from src.model.banco_dados import BancoDados
from src.model.curso import Curso
from src.dao.dao_curso import DaoCurso

class TestDaoFabrica:

    def test_dao_cria_curso_no_banco(self, cria_banco):
        actual = DaoFabrica(Curso("Adm"), cria_banco) \
                    .fabrica_objetos_dao()
        assert isinstance(actual, DaoCurso)

    def test_dao_alunos_criada(self, cria_banco):
        dao = DaoFabrica(Aluno("João"), cria_banco)
        actual = dao.fabrica_objetos_dao()
        assert isinstance(actual, DaoAluno)
