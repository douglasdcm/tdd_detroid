from tests.helper import executa_comando
from src.model.curso import Curso
from tests.massa_dados import curso_nome_1, materia_nome_1, \
    materia_nome_2, materia_nome_3
from src.tabelas import cursos
from pytest import fixture
from src.controller.controller import Controller


class TestCliCurso:

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco_real):
        self._MENSSAGEM_SUCESSO = f"Curso de {curso_nome_1} criado."
        self._MENSSAGEM_ERRO = "Lista de parâmetros inválida."
        self._cria_curso = "cria-curso"
        self._bd = cria_banco_real
        self._bd.deleta_tabela(cursos)

    def teardown_method(self, method):
        self._bd.fecha_conexao_existente()

    def test_criacao_curso_com_menos_materias_que_minimo_retorna_excecao(self):
        expected = self._MENSSAGEM_ERRO
        parametros = [self._cria_curso, "--nome", curso_nome_1,
                      "-m", materia_nome_1, materia_nome_2]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_de_curso_sem_materias_retorna_excecao(self):
        expected = self._MENSSAGEM_ERRO
        parametros = [self._cria_curso, "--nome", curso_nome_1, "-m"]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_de_curso_sem_nome_retorna_excecao(self):
        expected = self._MENSSAGEM_ERRO
        parametros = [self._cria_curso, "--nome", "--materias",
                      materia_nome_1, materia_nome_2, materia_nome_3]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_de_curso_usando_tag__m__para_lista_das_materias(self):
        expected = self._MENSSAGEM_SUCESSO
        parametros = [self._cria_curso, "--nome", curso_nome_1, "--materias",
                      materia_nome_1, materia_nome_2, materia_nome_3]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_criacao_de_curso_com_paramtro__materias__antes__nome(self):
        expected = self._MENSSAGEM_SUCESSO
        parametros = [self._cria_curso, "--materias",
                      materia_nome_1, materia_nome_2, materia_nome_3, "--nome",
                      curso_nome_1]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_curso_criado_banco_dados(self):
        expected = [tuple((1, curso_nome_1))]
        parametros = [self._cria_curso, "--nome", curso_nome_1, "--materias",
                      materia_nome_1, materia_nome_2, materia_nome_3]
        executa_comando(parametros)
        actual = Controller(Curso(curso_nome_1), self._bd).pega_registros()
        assert actual == expected
