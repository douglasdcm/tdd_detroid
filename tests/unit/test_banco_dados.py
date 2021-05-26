import pytest
import sqlite3
from src.banco_dados import BancoDados

class TestBancoDados:

    IN_MEMORY_DB = ":memory:"

    def teardown_method(self, method):
        bd = BancoDados()
        bd.fecha_conexao_existente()

    def test_tabela_pode_ser_deletada(self):
        bd = BancoDados(sqlite3.connect("test.db"))
        tabela = "teste"
        campo = "campo_1"
        valor = f"'valor_1'"
        bd.cria_tabela(tabela, campo)
        bd.salva_registro(tabela, valor)
        bd.deleta_tabela(tabela)

    def test_conexao_nao_criada_se_existe(self):
        con = sqlite3.connect(self.IN_MEMORY_DB)
        bd_1 = BancoDados(con)
        bd_2 = BancoDados()
        tabela = "test"
        campos = "campo_1"
        valor = "'valor_1'"
        expected = [('valor_1',)]
        bd_1.cria_tabela(tabela, campos)
        bd_1.salva_registro(tabela, valor) 
        actual = bd_2.pega_todos_registros(tabela)
        assert actual == expected

    def test_criacao_tabela_sem_nome_retorna_excecao(self):
        bd = BancoDados(sqlite3.connect(self.IN_MEMORY_DB))
        tabela = ""
        campos = "campos_1, campo_2"
        with pytest.raises(Exception, match="Não foi possível criar a tabela."):
            bd.cria_tabela(tabela, campos)

    def test_criacao_tabela_sem_campos_retorna_excecao(self):
        bd = BancoDados(sqlite3.connect(self.IN_MEMORY_DB))
        tabela = "tabela_1"
        campos = ""
        with pytest.raises(Exception, match="Não foi possível criar a tabela."):
            bd.cria_tabela(tabela, campos)

    def test_api_banco_dados_pega_registros_de_tabela_inexixtente_retorna_erro(self):
        bd = BancoDados(sqlite3.connect(self.IN_MEMORY_DB))
        tabela = "nao_existe"
        with pytest.raises(Exception, match="Não foi possível pegar os registros."):
            bd.pega_todos_registros(tabela) 

    def test_api_banco_dados_nao_salva_registro_se_tabela_nao_existe(self):
        bd = BancoDados(sqlite3.connect(self.IN_MEMORY_DB))
        tabela = "nao_existe"
        with pytest.raises(Exception, match="Não foi possiível salvar o registro."):
            bd.salva_registro(tabela, "quaisquer_valores")

    def test_api_banco_dados_cria_registro(self):
        bd = BancoDados(sqlite3.connect(self.IN_MEMORY_DB))
        campos = "campo_1, campo_2"
        valor_1 = "valor_1"
        valor_2 = "valor_2"
        valores = f"'{valor_1}', '{valor_2}'"
        expected = [(valor_1, valor_2)]
        tabela = "test"
        bd.cria_tabela(tabela, campos)
        bd.salva_registro(tabela, valores)
        actual = bd.pega_todos_registros(tabela)
        assert actual == expected
