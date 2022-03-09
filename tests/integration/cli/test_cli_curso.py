from os import EX_OK
from src.model.materia import Materia
from tests.helper import executa_comando
from src.model.curso import Curso
from tests.massa_dados import curso_nome_1, materia_nome_1, \
    materia_nome_2, materia_nome_3
from src.tabelas import cursos, materias
from pytest import fixture, raises
from src.controller.controller import Controller


class TestCliCurso:

    first = 0

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco_real):
        self._MENSSAGEM_SUCESSO = f"Curso de {curso_nome_1} criado."
        self._MENSSAGEM_ERRO = "Lista de parâmetros inválida."
        self._cria_curso = "cria-curso"
        self._bd = cria_banco_real
        self._bd.deleta_tabela(cursos)
        self._bd.deleta_tabela(materias)

    def teardown_method(self, method):
        self._bd.fecha_conexao_existente()

    def test_criacao_curso_com_materia_mesmo_nome_retorna_excecao(self):
        self._cria_materias()
        expected = "O curso não pode ter duas matérias com mesmo nome."
        parametros = [self._cria_curso, "--nome", curso_nome_1, "--materias",
                      materia_nome_1, materia_nome_1, materia_nome_3]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_curso_com_materia_inexistente_retorna_excecao(self):
        expected = "Registro especificado \'Materia 1\' não foi encontrado."
        parametros = [self._cria_curso, "--nome", curso_nome_1, "--materias",
                      materia_nome_1, materia_nome_2, materia_nome_3]
        actual = executa_comando(parametros)
        assert expected in actual

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
        self._cria_materias()
        expected = self._MENSSAGEM_SUCESSO
        parametros = [self._cria_curso, "--nome", curso_nome_1, "--materias",
                      materia_nome_1, materia_nome_2, materia_nome_3]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_criacao_de_curso_com_paramtro__materias__antes__nome(self):
        self._cria_materias()
        expected = self._MENSSAGEM_SUCESSO
        parametros = [self._cria_curso, "--materias",
                      materia_nome_1, materia_nome_2, materia_nome_3, "--nome",
                      curso_nome_1]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_curso_criado_banco_dados(self):
        self._cria_materias()
        expected = Curso(curso_nome_1).pega_nome()
        parametros = [self._cria_curso, "--nome", curso_nome_1, "--materias",
                      materia_nome_1, materia_nome_2, materia_nome_3]
        executa_comando(parametros)
        curso = Controller(Curso(curso_nome_1), self._bd).pega_registros()[self.first]
        actual = curso.pega_nome()
        assert actual == expected

    def _cria_materias(self):
        Controller(Materia(materia_nome_1), self._bd).salva()
        Controller(Materia(materia_nome_2), self._bd).salva()
        Controller(Materia(materia_nome_3), self._bd).salva()
