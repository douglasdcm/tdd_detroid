from pytest import raises, fixture
from src.model.banco_dados import BancoDados
from sqlite3 import connect


class TestBancoDados:
    @fixture(autouse=True, scope="function")
    def setup(self, setup_database_in_memory):
        self.bd = BancoDados(setup_database_in_memory)
        self.tabela = "teste"
        yield
        self.bd.fecha_conexao_existente()

    def test_tabela_pode_ser_deletada(self):
        campo = "campo_1"
        valor = f"'valor_1'"
        self.bd.cria_tabela(self.tabela, campo)
        self.bd.salva_registro(self.tabela, campo, valor)

    def test_conexao_nao_criada_se_existe(self, setup_database_in_memory):
        bd_1 = BancoDados(setup_database_in_memory)
        bd_2 = BancoDados()
        campos = "campo_1"
        valor = "'valor_1'"
        expected = [tuple((1, "valor_1"))]
        bd_1.cria_tabela(self.tabela, campos)
        bd_1.salva_registro(self.tabela, campos, valor)
        actual = bd_2.pega_todos_registros(self.tabela)
        assert actual == expected

    def test_criacao_tabela_sem_nome_retorna_excecao(self):
        tabela = ""
        campos = "campos_1, campo_2"
        with raises(Exception, match="It was not possible to run the command"):
            self.bd.cria_tabela(tabela, campos)

    def test_criacao_tabela_sem_campos_retorna_excecao(self):
        campos = ""
        with raises(Exception, match="It was not possible to run the command"):
            self.bd.cria_tabela(self.tabela, campos)

    def test_api_banco_dados_pega_registros_de_tabela_inexistente_retorna_erro(self):
        with raises(Exception, match="It was not possible to run the command"):
            self.bd.pega_todos_registros(self.tabela)

    def test_api_banco_dados_nao_salva_registro_se_tabela_nao_existe(self):
        with raises(Exception, match="It was not possible to run the command"):
            self.bd.salva_registro(self.tabela, "campos", "quaisquer_valores")

    def test_api_banco_dados_cria_registro(self):
        campos = "campo_1, campo_2"
        valor_1 = "valor_1"
        valor_2 = "valor_2"
        valores = f"'{valor_1}', '{valor_2}'"
        expected = [tuple((1, valor_1, valor_2))]
        self.bd.cria_tabela(self.tabela, campos)
        self.bd.salva_registro(self.tabela, campos, valores)
        actual = self.bd.pega_todos_registros(self.tabela)
        assert actual == expected
