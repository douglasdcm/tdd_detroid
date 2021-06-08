from sqlite3 import connect
from src.dao.dao_inscricao import DaoInscricao
from src.model.aluno import Aluno
from src.dao.dao_fabrica import DaoFabrica
from src.dao.dao_aluno import DaoAluno
from src.model.banco_dados import BancoDados
from src.model.curso import Curso
from src.dao.dao_curso import DaoCurso
from tests.massa_dados import curso_nome_1, aluno_nome_1
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso

class TestDaoFabrica:

    def test_dao_cria_inscricao_aluno_curso_no_banco(self, cria_banco):
        aluno_id = "1"
        curso_id = "1"
        actual = DaoFabrica(InscricaoAlunoCurso(aluno_id, curso_id), cria_banco) \
                    .fabrica_objetos_dao()
        assert isinstance(actual, DaoInscricao)

    def test_dao_cria_curso_no_banco(self, cria_banco):
        actual = DaoFabrica(Curso(curso_nome_1), cria_banco) \
                    .fabrica_objetos_dao()
        assert isinstance(actual, DaoCurso)

    def test_dao_alunos_criada(self, cria_banco):
        dao = DaoFabrica(Aluno(aluno_nome_1), cria_banco)
        actual = dao.fabrica_objetos_dao()
        assert isinstance(actual, DaoAluno)
