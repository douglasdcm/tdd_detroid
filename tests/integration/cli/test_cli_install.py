from pytest import fixture
from tests.helper import executa_comando
from os import path
from src.config import database_name
from src.model.banco_dados import BancoDados
from sqlite3 import connect as connect


class TestInstallCli:
    @fixture(scope="function", autouse=True)
    def setup(self):
        executa_comando(["install"])

    def test_should_insert_class_when_asked_for(self):
        database = BancoDados(connect(database_name))
        student = [
            {
                "nome": "materia_1",
            }
        ]
        actual = database.save("materias", student)[1]
        assert actual == []

    def test_should_create_materias_table_when_asked_for(self):
        database = BancoDados(connect(database_name))
        actual = database.get_biggest_id("materias")
        assert actual == []

    def test_should_insert_student_when_asked_for(self):
        database = BancoDados(connect(database_name))
        student = [
            {
                "name": "student_name",
                "score": 10,
                "situation": "in progress",
            }
        ]
        actual = database.save("students", student)[1]
        assert actual == []

    def test_shoul_create_student_table_when_asked_for(self):
        database = BancoDados(connect(database_name))
        actual = database.get_biggest_id("students")
        assert actual == []

    def test_should_create_a_new_database_when_asked_for(self):
        assert path.exists(database_name) is True
