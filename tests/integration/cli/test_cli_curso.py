from src.model.banco_dados import BancoDados
from tests.helper import executa_comando
from src.model.curso import Curso
from tests.massa_dados import (
    curso_nome_1,
    discipline_names,
)
from pytest import fixture
from src.controller.controller import Controller


class TestCliCurso:

    __cria_curso = "cria-curso"
    __MENSSAGEM_SUCESSO = f"Curso de {curso_nome_1} criado."
    __MENSSAGEM_ERRO = "Lista de parâmetros inválida."

    @fixture
    def setup(self, setup_database_in_real_db):
        self.__bd = setup_database_in_real_db
        self.__database = BancoDados(self.__bd)

    def teardown_method(self, method):
        self.__database.fecha_conexao_existente()

    def test_criacao_curso_com_materia_mesmo_nome_retorna_excecao(self, setup):
        expected = "O curso não pode ter duas matérias com mesmo nome."
        parametros = [
            self.__cria_curso,
            "--nome",
            curso_nome_1,
            "--materias",
            discipline_names[0],
            discipline_names[0],
            discipline_names[1],
        ]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_curso_com_materia_inexistente_retorna_excecao(self, setup):
        expected = "Registro especificado 'Materia 1' não foi encontrado."
        parametros = [
            self.__cria_curso,
            "--nome",
            curso_nome_1,
            "--materias",
            "Materia 1",
            discipline_names[1],
            discipline_names[2],
        ]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_curso_com_menos_materias_que_minimo_retorna_excecao(self, setup):
        expected = self.__MENSSAGEM_ERRO
        parametros = [
            self.__cria_curso,
            "--nome",
            curso_nome_1,
            "-m",
            discipline_names[0],
            discipline_names[1],
        ]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_de_curso_sem_materias_retorna_excecao(self, setup):
        expected = self.__MENSSAGEM_ERRO
        parametros = [self.__cria_curso, "--nome", curso_nome_1, "-m"]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_de_curso_sem_nome_retorna_excecao(self, setup):
        expected = self.__MENSSAGEM_ERRO
        parametros = [
            self.__cria_curso,
            "--nome",
            "--materias",
            discipline_names[0],
            discipline_names[1],
            discipline_names[2],
        ]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_de_curso_usando_tag__m__para_lista_das_materias(self, setup):
        expected = self.__MENSSAGEM_SUCESSO
        parametros = [
            self.__cria_curso,
            "--nome",
            curso_nome_1,
            "--materias",
            discipline_names[0],
            discipline_names[1],
            discipline_names[2],
        ]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_criacao_de_curso_com_paramtro__materias__antes__nome(self, setup):
        expected = self.__MENSSAGEM_SUCESSO
        parametros = [
            self.__cria_curso,
            "--materias",
            discipline_names[0],
            discipline_names[1],
            discipline_names[2],
            "--nome",
            curso_nome_1,
        ]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_curso_criado_banco_dados(self, setup):
        expected = Curso(curso_nome_1).pega_nome()
        parametros = [
            self.__cria_curso,
            "--nome",
            curso_nome_1,
            "--materias",
            discipline_names[0],
            discipline_names[1],
            discipline_names[2],
        ]
        executa_comando(parametros)
        curso = Controller(Curso(curso_nome_1), self.__bd).get_by_biggest_id()
        actual = curso.pega_nome()
        assert actual == expected
