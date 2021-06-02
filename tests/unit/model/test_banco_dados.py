from pytest import raises
from src.model.banco_dados import BancoDados

class TestBancoDados:

    def test_tabela_pode_ser_deletada(self, cria_banco):
        bd = cria_banco
        tabela = "teste"
        campo = "campo_1"
        valor = f"'valor_1'"
        bd.cria_tabela(tabela, campo)
        bd.salva_registro(tabela, campo, valor)
        bd.deleta_tabela(tabela)

    def test_conexao_nao_criada_se_existe(self, cria_banco):
        bd_1 = cria_banco
        bd_2 = BancoDados()
        tabela = "test"
        campos = "campo_1"
        valor = "'valor_1'"
        expected = [(1, 'valor_1',)]
        bd_1.cria_tabela(tabela, campos)
        bd_1.salva_registro(tabela, campos, valor) 
        actual = bd_2.pega_todos_registros(tabela)
        assert actual == expected

    def test_criacao_tabela_sem_nome_retorna_excecao(self, cria_banco):
        bd = cria_banco
        tabela = ""
        campos = "campos_1, campo_2"
        with raises(Exception, match="Não foi possível criar a tabela."):
            bd.cria_tabela(tabela, campos)

    def test_criacao_tabela_sem_campos_retorna_excecao(self, cria_banco):
        bd = cria_banco
        tabela = "tabela_1"
        campos = ""
        with raises(Exception, match="Não foi possível criar a tabela."):
            bd.cria_tabela(tabela, campos)

    def test_api_banco_dados_pega_registros_de_tabela_inexixtente_retorna_erro(self, cria_banco):
        bd = cria_banco
        tabela = "nao_existe"
        with raises(Exception, match="Não foi possível pegar os registros."):
            bd.pega_todos_registros(tabela) 

    def test_api_banco_dados_nao_salva_registro_se_tabela_nao_existe(self, cria_banco):
        bd = cria_banco
        tabela = "nao_existe"
        with raises(Exception, match="Não foi possiível salvar o registro."):
            bd.salva_registro(tabela, "campos", "quaisquer_valores")

    def test_api_banco_dados_cria_registro(self, cria_banco):
        bd = cria_banco
        campos = "campo_1, campo_2"
        valor_1 = "valor_1"
        valor_2 = "valor_2"
        valores = f"'{valor_1}', '{valor_2}'"
        expected = [(1, valor_1, valor_2)]
        tabela = "test"
        bd.cria_tabela(tabela, campos)
        bd.salva_registro(tabela, campos, valores)
        actual = bd.pega_todos_registros(tabela)
        assert actual == expected
