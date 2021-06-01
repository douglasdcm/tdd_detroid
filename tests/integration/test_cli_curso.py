from src.model.banco_dados import BancoDados
from tests.helper import executa_comando
from src.dao.dao_fabrica import DaoFabrica
from sqlite3 import connect
from src.model.curso import Curso

class TestCliCurso:

    def setup_method(self, method):
        self._curso = "Matemática"
        self._MENSSAGEM_SUCESSO = f"Curso de {self._curso} criado."
        self._MENSSAGEM_ERRO = "Lista de parâmetros inválida."
        self._file = "main.py"
        self._cria_curso = "cria-curso"
        self._bd = BancoDados(connect("sample.db"))

    def teardown_method(self, method):       
        self._bd.deleta_tabela("cursos")
        self._bd.fecha_conexao_existente()

    def test_criacao_de_curso_com_menos_materias_que_o_minimo_retorna_excecao(self):
        expected = self._MENSSAGEM_ERRO
        parametros = [self._cria_curso, "--nome", self._curso, 
                    "-m", "algebra", "calculo"]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_de_curso_sem_materias_retorna_excecao(self):
        expected = self._MENSSAGEM_ERRO
        parametros = [self._cria_curso, "--nome", self._curso, "-m"]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_de_curso_sem_nome_retorna_excecao(self):
        expected = self._MENSSAGEM_ERRO
        parametros = [self._cria_curso, "--nome", "--materias",
                     "algebra", "cálculo", "lógica"]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_criacao_de_curso_usando_tag__m__para_lista_das_materias(self):
        expected = self._MENSSAGEM_SUCESSO
        parametros = [self._cria_curso, "--nome", self._curso, "--materias",
                     "algebra", "cálculo", "lógica"]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_criacao_de_curso_usando_tag__n__para_nome_do_curso(self):
        expected = self._MENSSAGEM_SUCESSO
        parametros = [self._cria_curso, "--nome", self._curso, "--materias",
                     "algebra", "cálculo", "lógica"]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_criacao_de_curso_com_paramtro__materias__antes__nome(self):
        expected = self._MENSSAGEM_SUCESSO
        parametros = [self._cria_curso, "--materias",
                     "algebra", "cálculo", "lógica", "--nome", self._curso]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_criacao_de_curso_com_numero_minimo_de_materias(self):
        expected = self._MENSSAGEM_SUCESSO
        parametros = [self._cria_curso, "--nome", self._curso, "--materias",
                     "algebra", "cálculo", "lógica"]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_curso_criado_banco_dados(self):
        expected = [tuple((1, self._curso))]
        parametros = [self._cria_curso, "--nome", self._curso, "--materias",
                     "algebra", "cálculo", "lógica"]
        executa_comando(parametros)
        actual = DaoFabrica(Curso(self._curso), self._bd) \
                    .fabrica_objetos_dao() \
                    .pega_tudo()
        assert actual == expected