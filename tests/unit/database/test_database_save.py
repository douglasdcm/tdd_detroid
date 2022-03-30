from pytest import fixture
from src.model.banco_dados import BancoDados


class TestDatabaseSave:
    @fixture
    def setup(self, setup_database_in_memory):
        table = {
            "name": "students",
            "columns": [
                {"name": "name", "type": "text", "constraints": "not null"},
                {"name": "score", "type": "integer", "constraints": "not null"},
                {"name": "situation", "type": "text", "constraints": "not null"},
            ],
        }
        database = BancoDados(setup_database_in_memory)
        database.create_table(table)
        yield database

    def test_should_insert_many_itens_when_list_informed(self, setup):
        student = [
            {"name": "student_name", "score": 10, "situation": "in progress"},
            {"name": "student_name_2", "score": 10, "situation": "in progress"},
            {"name": "student_name_3", "score": 10, "situation": "in progress"},
        ]
        table = "students"
        expected = 'insert into students (name, score, situation) values ("student_name_3", 10, "in progress")'
        database = setup
        actual, _ = database.save(table, student)
        assert actual == expected

    def test_should_insert_many_columns_when_informed(self, setup):
        student = [{"name": "student_name", "score": 10, "situation": "in progress"}]
        table = "students"
        expected = 'insert into students (name, score, situation) values ("student_name", 10, "in progress")'
        database = setup
        actual, _ = database.save(table, student)
        assert actual == expected

    def test_should_insert_one_item_when_just_one__item_informed(
        self, setup_database_in_memory
    ):
        data = [
            {
                "col_1": "val_1",
            }
        ]
        table = {
            "name": "table_test",
            "columns": [{"name": "col_1", "type": "text"}],
        }
        database = BancoDados(setup_database_in_memory)
        database.create_table(table)
        expected = 'insert into table_test (col_1) values ("val_1")'
        actual, _ = database.save(table["name"], data)
        assert actual == expected

    def test_should_save_student_list_when_the_valid_list_informed(self, setup):
        students = [
            {
                "name": "student_name_1",
                "score": 10,
                "situation": "in progress",
            },
            {
                "name": "student_name_2",
                "score": 10,
                "situation": "in progress",
            },
            {
                "name": "student_name_3",
                "score": 10,
                "situation": "in progress",
            },
        ]
        table = "students"
        expected = 'insert into students (name, score, situation) values ("student_name_3", 10, "in progress")'
        database = setup
        actual, _ = database.save(table, students)
        assert actual == expected

    def test_should_save_student_when_values_of_dict_informed(self, setup):
        student = [
            {
                "name": "student_name",
                "score": 10,
                "situation": "in progress",
            }
        ]
        database = setup
        _, actual = database.save("students", student)
        assert actual == []
