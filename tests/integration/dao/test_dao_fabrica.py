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
    def test_dao_cria_inscricao_aluno_curso_no_banco(self, setup_database_in_memory):
        id_ = 1
        course = Curso().define_id(id_)
        actual = DaoFabrica(
            InscricaoAlunoCurso(Aluno(), course),
            BancoDados(setup_database_in_memory),
        ).fabrica_objetos_dao()
        assert isinstance(actual, DaoInscricao)

    def test_dao_cria_curso_no_banco(self, setup_database_in_memory):
        actual = DaoFabrica(
            Curso(curso_nome_1), setup_database_in_memory
        ).fabrica_objetos_dao()
        assert isinstance(actual, DaoCurso)

    def test_dao_alunos_criada(self, setup_database_in_memory):
        dao = DaoFabrica(Aluno(aluno_nome_1), setup_database_in_memory)
        actual = dao.fabrica_objetos_dao()
        assert isinstance(actual, DaoAluno)
