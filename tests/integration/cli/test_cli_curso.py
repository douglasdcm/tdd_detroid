from src.model.banco_dados import BancoDados
from tests.helper import executa_comando
from src.dao.dao_fabrica import DaoFabrica
from sqlite3 import connect
from src.model.curso import Curso
from tests.massa_dados import curso_nome_1, materia_nome_1, materia_nome_2, materia_nome_3
from src.config import banco_dados
from src.tabelas import cursos

class TestCliCurso:

    def setup_method(self, method):
        self._MENSSAGEM_SUCESSO = f"Curso de {curso_nome_1} criado."
        self._MENSSAGEM_ERRO = "Lista de parâmetros inválida."
        self._cria_curso = "cria-curso"
        self._bd = BancoDados(connect(banco_dados))
        self._bd.deleta_tabela(cursos)

    def teardown_method(self, method):
        self._bd.fecha_conexao_existente()

    def test_criacao_de_curso_com_menos_materias_que_o_minimo_retorna_excecao(self):
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
                     materia_nome_1, materia_nome_2, materia_nome_3, "--nome", curso_nome_1]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_criacao_de_curso_com_numero_minimo_de_materias(self):
        expected = self._MENSSAGEM_SUCESSO
        parametros = [self._cria_curso, "--nome", curso_nome_1, "--materias",
                     materia_nome_1, materia_nome_2, materia_nome_3]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_curso_criado_banco_dados(self):
        expected = {1: curso_nome_1}
        parametros = [self._cria_curso, "--nome", curso_nome_1, "--materias",
                     materia_nome_1, materia_nome_2, materia_nome_3]
        executa_comando(parametros)
        actual = DaoFabrica(Curso(curso_nome_1), self._bd) \
                    .fabrica_objetos_dao() \
                    .pega_tudo()
        assert actual == expected