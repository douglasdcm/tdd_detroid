from src.model.aluno import Aluno
from tests.helper import executa_comando
from src.utils.messagens import LISTA_PARAMETROS_INVALIDA
from src.tabelas import alunos
from tests.massa_dados import aluno_nome_1, aluno_nome_2, aluno_nome_3
from pytest import fixture
from src.controller.controller import Controller


class TestCliAluno:

    _MENSSAGEM_SUCESSO = "Aluno %s criado com sucesso."
    _MENSSAGEM_SUCESSO_ATULIZACAO = "Aluno %s atualizado com sucesso."
    _comando_cria_aluno = "cria-aluno"
    _comando_atualiza_aluno = "atualiza-aluno"

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco_real):
        self.bd = cria_banco_real
        self.bd.deleta_tabela(alunos)

    def test_aluno_pode_atualizar_cr(self, cria_massa_dados):
        cria_massa_dados
        aluno_id = "1"
        expected = self._MENSSAGEM_SUCESSO_ATULIZACAO % aluno_nome_1
        actual = self._atualiza_aluno_por_cli(aluno_id)
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
        expected = self._MENSSAGEM_SUCESSO % aluno_nome_3
        self._cria_aluno_por_cli(aluno_nome_1)
        self._cria_aluno_por_cli(aluno_nome_2)
        actual = self._cria_aluno_por_cli(aluno_nome_3)
        assert actual == expected

    def test_aluno_criado_banco_dados(self):
        expected = aluno_nome_1
        self._cria_aluno_por_cli(expected)
        actual = Controller(Aluno(expected), self.bd).pega_registros()
        assert actual[0].pega_nome() == expected

    def test_criacao_um_aluno_com_informacoes_basicas(self):
        expected = self._MENSSAGEM_SUCESSO % aluno_nome_1
        actual = self._cria_aluno_por_cli(aluno_nome_1)
        assert actual == expected

    def _cria_aluno_por_cli(self, nome, tag="--nome"):
        comando_1 = [self._comando_cria_aluno, tag, nome]
        return executa_comando(comando_1)

    def _atualiza_aluno_por_cli(self, aluno_id):
        comando = [self._comando_atualiza_aluno, "--aluno-id", aluno_id]
        return executa_comando(comando)
