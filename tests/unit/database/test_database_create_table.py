from src.model.banco_dados import BancoDados


class TestDatabaseCreateTable:
    def test_should_create_table_when_it_does_not_exist(self, setup_database_in_memory):
        table = {
            "name": "table_name",
            "columns": [{"name": "col_1", "type": "text", "constraints": "not null"}],
        }
        expected = "CREATE TABLE IF NOT EXISTS TABLE_NAME (id INTEGER NOT NULL PRIMARY KEY, COL_1 TEXT NOT NULL);"
        database = BancoDados(setup_database_in_memory)
        actual = database.create_table(table)
        assert actual == expected

    def test_should_create_table_with_int_column_when_columns_type_is_integer(
        self, setup_database_in_memory
    ):
        table = {
            "name": "table_name",
            "columns": [
                {"name": "col_1", "type": "integer", "constraints": "not null"}
            ],
        }
        expected = "CREATE TABLE IF NOT EXISTS TABLE_NAME (id INTEGER NOT NULL PRIMARY KEY, COL_1 INTEGER NOT NULL);"
        database = BancoDados(setup_database_in_memory)
        actual = database.create_table(table)
        assert actual == expected

    def test_should_create_table_when_many_colums_informed(
        self, setup_database_in_memory
    ):
        table = {
            "name": "table_name",
            "columns": [
                {"name": "col_1", "type": "text", "constraints": "not null"},
                {"name": "col_2", "type": "text", "constraints": "not null"},
                {"name": "col_3", "type": "text", "constraints": "not null"},
            ],
        }
        expected = "CREATE TABLE IF NOT EXISTS TABLE_NAME (id INTEGER NOT NULL PRIMARY KEY, COL_1 TEXT NOT NULL, COL_2 TEXT NOT NULL, COL_3 TEXT NOT NULL);"
        database = BancoDados(setup_database_in_memory)
        actual = database.create_table(table)
        assert actual == expected

    def test_should_create_table_when_colums_and_values_informed(
        self, setup_database_in_memory
    ):
        table = {
            "name": "table_name",
            "columns": [{"name": "col_1", "type": "text", "constraints": "not null"}],
        }
        expected = "CREATE TABLE IF NOT EXISTS TABLE_NAME (id INTEGER NOT NULL PRIMARY KEY, COL_1 TEXT NOT NULL);"
        database = BancoDados(setup_database_in_memory)
        actual = database.create_table(table)
        assert actual == expected
