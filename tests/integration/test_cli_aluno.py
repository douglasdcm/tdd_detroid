import sqlite3
from tests.helper import executa_comando
from src.banco_dados import BancoDados

class TestCliAluno:

    bd = None

    def setup_method(self, method):
        self.bd = BancoDados(sqlite3.connect(":memory:"))

    def teardown_method(self, method):
        self.bd.fecha_conexao_existente()

    def test_aluno_pode_ser_incrito_em_curso(self):
        expected = "Aluno José inscrito no curso de Matemática."
        comando = ["python", "main.py", "--inscreve-aluno-curso", "--aluno",
                     "José", "--curso", "Matemática"]
        actual = executa_comando(comando)
        assert actual == expected
    
    def test_criacao_alunos_sem_nome_retorna_excecao(self):
        expected = "Lista de argumentos inválida."
        comando = ["python", "main.py", "cria-aluno", "--nome"]
        actual = executa_comando(comando)
        assert expected in actual

    def test_criacao_alunos_sem_parametro__nome__retorna_excecao(self):
        expected = "Lista de argumentos inválida."
        comando = ["python", "main.py", "cria-aluno"]
        actual = executa_comando(comando)
        assert expected in actual

    def test_criacao_tres_alunos_distintos_com_informacoes_basicas(self):
        expected_1 = "Aluno maria criado com sucesso."
        expected_2 = "Aluno jose criado com sucesso."
        expected_3 = "Aluno pedro criado com sucesso."
        comando_1 = ["python", "main.py", "cria-aluno", "--nome", "maria"]
        comando_2 = ["python", "main.py", "cria-aluno", "--nome", "jose"]
        comando_3 = ["python", "main.py", "cria-aluno", "--nome", "pedro"]
        actual_1 = executa_comando(comando_1)
        actual_2 = executa_comando(comando_2)
        actual_3 = executa_comando(comando_3)
        assert actual_1 == expected_1
        assert actual_2 == expected_2
        assert actual_3 == expected_3

    def test_criacao_um_aluno_com_informacoes_basicas_usando_parametro__n(self):
        expected = "Aluno jose criado com sucesso."
        comando = ["python", "main.py", "cria-aluno", "-n", "jose"]
        actual = executa_comando(comando)
        assert actual == expected

    def test_criacao_um_aluno_com_informacoes_basicas(self):
        bd = BancoDados(sqlite3.connect(":memory:")) 
        expected = "Aluno jose criado com sucesso."
        expected_2 = ('jose', 1)
        comando = ["python", "main.py", "cria-aluno", "--nome", "jose"]               
        actual = executa_comando(comando)
        actual_2 = bd.pega_todos_registros("alunos")
        assert actual == expected
        assert actual_2 == expected_2