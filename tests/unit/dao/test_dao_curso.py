from src.dao.dao_curso import DaoCurso
from src.model.curso import Curso
from tests.massa_dados import curso_nome_1

class TestDaoCurso:

    def test_curso_pode_ser_criado_banco_dados(self, cria_banco):
        expected = [tuple((1, curso_nome_1))]
        dao = DaoCurso(Curso(curso_nome_1), cria_banco)
        dao.salva()
        actual = dao.pega_tudo()
        assert actual == expected