from tests.conftest import setup_database_in_memory
from src.dao.dao_materia import DaoMateria
from src.model.materia import Materia
from pytest import raises
from src.model.banco_dados import BancoDados


class TestDaoMateria:
    def test_materia_sem_nome_nao_pode_ser_salva_banco(self, setup_database_in_memory):
        with raises(Exception, match="Matéria especificada sem nome."):
            DaoMateria(Materia(None), setup_database_in_memory).salva()

    def test_materia_pode_ser_salva_banco(self, setup_database_in_memory):
        expected = "Química"
        dao = DaoMateria(Materia(expected), BancoDados(setup_database_in_memory))
        dao.salva()
        actual = dao.get_by_biggest_id().pega_nome()
        assert actual == expected
