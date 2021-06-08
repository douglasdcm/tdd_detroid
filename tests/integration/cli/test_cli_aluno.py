from sqlite3 import connect
from src.model.aluno import Aluno
from src.dao.dao_fabrica import DaoFabrica
from tests.helper import executa_comando
from src.model.banco_dados import BancoDados
from src.utils.messagens import LISTA_PARAMETROS_INVALIDA
from src.tabelas import alunos
from src.config import banco_dados
from tests.massa_dados import aluno_nome_1, aluno_nome_2, aluno_nome_3
from pytest import fixture
from src.controller.controller import Controller

class TestCliAluno:
    
    _MENSSAGEM_SUCESSO = "Aluno %s criado com sucesso."
    _comando_cria_aluno = "cria-aluno"

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco_real):        
        self.bd = cria_banco_real
        self.bd.deleta_tabela(alunos)
    
    def test_criacao_alunos_sem_nome_retorna_excecao(self):
        expected = LISTA_PARAMETROS_INVALIDA
        parametros = [self._comando_cria_aluno, "--nome"]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_alunos_sem_parametro__nome__retorna_excecao(self):
        expected = LISTA_PARAMETROS_INVALIDA
        parametros = [self._comando_cria_aluno]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_tres_alunos_distintos_com_informacoes_basicas(self):
        expected = self._MENSSAGEM_SUCESSO % aluno_nome_3
        self._cria_aluno_por_cli(aluno_nome_1)
        self._cria_aluno_por_cli(aluno_nome_2)
        actual = self._cria_aluno_por_cli(aluno_nome_3)
        assert actual == expected

    def test_aluno_criado_banco_dados(self):
        expected = [tuple((1, aluno_nome_1))]
        self._cria_aluno_por_cli(aluno_nome_1)
        actual = Controller(Aluno(aluno_nome_1), self.bd).pega_registros()
        assert actual == expected

    def test_criacao_um_aluno_com_informacoes_basicas(self):
        expected = self._MENSSAGEM_SUCESSO % aluno_nome_1
        actual = self._cria_aluno_por_cli(aluno_nome_1)
        assert actual == expected

    def _cria_aluno_por_cli(self, nome, tag="--nome"):
        comando_1 = [self._comando_cria_aluno, tag, nome]
        return executa_comando(comando_1)