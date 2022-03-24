from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.model.aluno import Aluno
from tests.helper import executa_comando
from src.utils.messagens import LISTA_PARAMETROS_INVALIDA
from src.tabelas import alunos
from tests.massa_dados import aluno_nome_1, aluno_nome_2, aluno_nome_3
from pytest import fixture
from src.controller.controller import Controller


class TestCliAluno:

    _MENSSAGEM_SUCESSO = "Aluno %s criado com sucesso."
    __MENSSAGEM_SUCESSO_ATULIZACAO = (
        "Aluno com identificador %s atualizado com sucesso."
    )
    __comando_cria_aluno = "cria-aluno"

    def test_aluno_pode_atualizar_situacao(self, setup_database_in_memory):
        connection = setup_database_in_memory
        expected = "trancado"
        self.__atualiza_aluno_por_cli(aluno_id=1, situacao=expected)
        aluno = Controller(Aluno(), connection).pega_registro_por_id(1)
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_pode_atualizar_nome(self, setup_database_in_real_db):
        aluno_id = "1"
        nome = "student_name_1"
        expected = nome
        self.__atualiza_aluno_por_cli(aluno_id, nome)
        aluno = Controller(Aluno(), setup_database_in_real_db).pega_registro_por_id(
            aluno_id
        )
        actual = aluno.pega_nome()
        assert actual == expected

    def test_aluno_pode_atualizar_cr(self, cria_massa_dados):
        cria_massa_dados
        aluno_id = "1"
        expected = self.__MENSSAGEM_SUCESSO_ATULIZACAO % aluno_id
        actual = self.__atualiza_aluno_por_cli(aluno_id)
        assert actual == expected

    def test_criacao_alunos_sem_nome_retorna_excecao(self):
        expected = LISTA_PARAMETROS_INVALIDA
        parametros = [self.__comando_cria_aluno, "--nome"]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_alunos_sem_parametro__nome__retorna_excecao(self):
        expected = LISTA_PARAMETROS_INVALIDA
        parametros = [self.__comando_cria_aluno]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_tres_alunos_distintos_com_informacoes_basicas(self):
        expected = self._MENSSAGEM_SUCESSO % aluno_nome_3
        self.__cria_aluno_por_cli(aluno_nome_1)
        self.__cria_aluno_por_cli(aluno_nome_2)
        actual = self.__cria_aluno_por_cli(aluno_nome_3)
        assert actual == expected

    def test_aluno_criado_banco_dados_cli(self, setup_empty_database_real_v2):
        expected = aluno_nome_1
        connection = setup_empty_database_real_v2
        self.__cria_aluno_por_cli(expected)
        actual = Controller(Aluno(), connection).get_by_name(aluno_nome_1)
        assert actual[0].pega_nome() == expected

    def test_criacao_um_aluno_com_informacoes_basicas(self):
        expected = self._MENSSAGEM_SUCESSO % aluno_nome_1
        actual = self.__cria_aluno_por_cli(aluno_nome_1)
        assert actual == expected

    def __cria_aluno_por_cli(self, nome, tag="--nome"):
        comando_1 = [self.__comando_cria_aluno, tag, nome]
        return executa_comando(comando_1)

    def __atualiza_aluno_por_cli(self, aluno_id, nome=None, situacao=None):
        comando = ["atualiza-aluno", "--aluno-id", str(aluno_id)]
        if isinstance(nome, str):
            comando.extend(["--nome", nome])
        if isinstance(situacao, str):
            comando.extend(["--situacao", situacao])
        return executa_comando(comando)
