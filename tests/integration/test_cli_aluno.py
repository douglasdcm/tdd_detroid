import pytest, sqlite3
from tests.helper import executa_comando
from src.banco_dados import BancoDados

class TestCliAluno:

    tabela = "alunos"
    aluno_1 = "maria"
    aluno_2 = "joao"
    aluno_3 = "jose"

    def setup_method(self, method):        
        self.bd = BancoDados(sqlite3.connect("sample.db"))
        self.bd.deleta_tabela(self.tabela)

    def teardown_method(self, method):
        self.bd.fecha_conexao_existente()
        self.bd = None

    def test_aluno_pode_ser_incrito_em_curso(self):
        aluno = "José"
        curso = "Matemática"
        expected = f"Aluno {aluno} inscrito no curso de {curso}."
        comando = ["python", "main.py", "inscreve-aluno-curso", "--aluno",
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
        expected_1 = f"Aluno {self.aluno_1} criado com sucesso."
        expected_2 = f"Aluno {self.aluno_2} criado com sucesso."
        expected_3 = f"Aluno {self.aluno_3} criado com sucesso."
        expected_4 = [(self.aluno_1,), (self.aluno_2,), (self.aluno_3,)]
        actual_1 = self._cria_aluno(self.aluno_1)
        actual_2 = self._cria_aluno(self.aluno_2)
        actual_3 = self._cria_aluno(self.aluno_3)
        actual_4 = self.bd.pega_todos_registros(self.tabela)
        assert actual_1 == expected_1
        assert actual_2 == expected_2
        assert actual_3 == expected_3
        assert actual_4 == expected_4

    def test_criacao_um_aluno_com_informacoes_basicas_usando_parametro__n(self):
        expected = f"Aluno {self.aluno_1} criado com sucesso."
        actual = self._cria_aluno(self.aluno_1)
        assert actual == expected

    def test_criacao_um_aluno_com_informacoes_basicas(self):
        expected = f"Aluno {self.aluno_1} criado com sucesso."
        expected_2 = [tuple((self.aluno_1,)),]              
        actual = self._cria_aluno(self.aluno_1)
        actual_2 = self.bd.pega_todos_registros("alunos")
        assert actual == expected
        assert actual_2 == expected_2

    def _cria_aluno(self, nome, tag="--nome"):
        comando_1 = ["python", "main.py", "cria-aluno", tag, nome]
        return executa_comando(comando_1)