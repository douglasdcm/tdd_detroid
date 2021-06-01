from src.dao.dao_fabrica import DaoFabrica

class TestBdAlunos:

    def test_aluno_criado_foi_salvo_banco_dados(self, cria_banco, cria_aluno):
        nome = "José"
        expected = [tuple((1, nome,)),]
        DaoFabrica(cria_aluno, cria_banco).fabrica_objetos_dao().salva()
        actual = cria_banco.pega_todos_registros("alunos")
        assert actual == expected
