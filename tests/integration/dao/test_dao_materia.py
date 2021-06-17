from tests.conftest import cria_banco
from src.dao.dao_materia import DaoMateria
from src.model.materia import Materia
from pytest import raises


class TestDaoMateria:

    def test_materia_sem_nome_nao_pode_ser_salva_banco(self, cria_banco):
        with raises(Exception, match="Matéria especificada sem nome."):
            DaoMateria(Materia(None), cria_banco).salva()

    def test_materia_pode_ser_salva_banco(self, cria_banco):
        expected = "Química"
        dao = DaoMateria(Materia(expected), cria_banco)
        dao.salva()
        actual = dao.pega_por_id(id=1)
        assert actual.pega_nome() == expected
