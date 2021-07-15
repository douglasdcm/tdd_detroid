from src.model.aluno import Aluno
from tests.massa_dados import aluno_nome_1, aluno_nome_2, aluno_nome_3
from src.model.administrador import Adminstrador


class TestAdministrador:

    def test_admin_pode_listar_todos_alunos(self):
        Aluno(aluno_nome_1)
        Aluno(aluno_nome_2)
        Aluno(aluno_nome_3)
        expected = {
                        "alunos": [
                            {"nome": aluno_nome_1},
                            {"nome": aluno_nome_2},
                            {"nome": aluno_nome_3}
                        ]
                    }
        actual = Adminstrador().lista_alunos()
        assert actual == expected
