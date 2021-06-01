from sqlite3 import connect
from src.model.aluno import Aluno
from src.dao.dao_fabrica import DaoFabrica
from tests.helper import executa_comando
from src.model.banco_dados import BancoDados
from src.utils.messagens import LISTA_PARAMETROS_INVALIDA

class TestCliAluno:

    _tabela = "alunos"
    _aluno_1 = "Maria"
    _aluno_2 = "João"
    _aluno_3 = "José"
    _curso = "Matemática"
    _MENSSAGEM_SUCESSO = "Aluno %s criado com sucesso."
    _comando_cria_aluno = "cria-aluno"

    def setup_method(self, method):        
        self.bd = BancoDados(connect("sample.db"))
        self.bd.deleta_tabela(self._tabela)

    def teardown_method(self, method):
        self.bd.fecha_conexao_existente()
        self.bd = None

    def test_aluno_pode_ser_incrito_em_curso(self):
        expected = f"Aluno {self._aluno_1} inscrito no curso de {self._curso}."
        parametros = ["inscreve-aluno-curso", "--aluno",
                     self._aluno_1, "--curso", self._curso]
        actual = executa_comando(parametros)
        assert actual == expected
    
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
        expected_1 = self._MENSSAGEM_SUCESSO % self._aluno_1
        expected_2 = self._MENSSAGEM_SUCESSO % self._aluno_2
        expected_3 = self._MENSSAGEM_SUCESSO % self._aluno_3
        actual_1 = self._cria_aluno_por_cli(self._aluno_1)
        actual_2 = self._cria_aluno_por_cli(self._aluno_2)
        actual_3 = self._cria_aluno_por_cli(self._aluno_3)
        assert actual_1 == expected_1
        assert actual_2 == expected_2
        assert actual_3 == expected_3

    def test_aluno_criado_banco_dados(self):
        expected = [tuple((1, self._aluno_1)),]
        self._cria_aluno_por_cli(self._aluno_1)
        actual = DaoFabrica(Aluno(self._aluno_1), self.bd) \
                    .fabrica_objetos_dao() \
                    .pega_tudo()        
        assert actual == expected

    def test_criacao_um_aluno_com_informacoes_basicas(self):
        expected = self._MENSSAGEM_SUCESSO % self._aluno_1
        actual = self._cria_aluno_por_cli(self._aluno_1)
        assert actual == expected

    def _cria_aluno_por_cli(self, nome, tag="--nome"):
        comando_1 = [self._comando_cria_aluno, tag, nome]
        return executa_comando(comando_1)