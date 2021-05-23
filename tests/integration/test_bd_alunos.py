import sqlite3
from src.aluno import Aluno
from src.banco_dados import BancoDados

class TestBdAlunos:

    bd = None

    def setup_method(self, method):
        self.bd = BancoDados(sqlite3.connect(":memory:"))

    def teardown_method(self, method):
        self.bd.fecha_conexao_existente()

    def test_aluno_criado_foi_salvo_banco_dados(self):
        nome = "João"
        expected = [tuple((nome,)),]
        Aluno(nome)
        actual = self.bd.pega_todos_registros("alunos")
        assert actual == expected
