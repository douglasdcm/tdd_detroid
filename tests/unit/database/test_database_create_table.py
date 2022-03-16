class TestDatabaseCreateTable:
    def test_should_create_table_when_it_does_not_exist(self, cria_banco):
        table = {
            "name": "table_name",
            "columns": [
                {"name": "col_1", "type": "integer", "constraints": "not null"}
            ],
        }
        expected = "CREATE TABLE IF NOT EXISTS TABLE_NAME (id INTEGER NOT NULL PRIMARY KEY, COL_1 INTEGER NOT NULL);"
        database = cria_banco
        actual = database.create_table(table)
        assert actual == expected

    def test_should_create_table_with_int_cloum_when_colums_type_is_integer(
        self, cria_banco
    ):
        table = {
            "name": "table_name",
            "columns": [
                {"name": "col_1", "type": "integer", "constraints": "not null"}
            ],
        }
        expected = "CREATE TABLE IF NOT EXISTS TABLE_NAME (id INTEGER NOT NULL PRIMARY KEY, COL_1 INTEGER NOT NULL);"
        database = cria_banco
        actual = database.create_table(table)
        assert actual == expected

    def test_should_create_table_when_many_colums_informed(self, cria_banco):
        table = {
            "name": "table_name",
            "columns": [
                {"name": "col_1", "type": "text", "constraints": "not null"},
                {"name": "col_2", "type": "text", "constraints": "not null"},
                {"name": "col_3", "type": "text", "constraints": "not null"},
            ],
        }
        expected = "CREATE TABLE IF NOT EXISTS TABLE_NAME (id INTEGER NOT NULL PRIMARY KEY, COL_1 TEXT NOT NULL, COL_2 TEXT NOT NULL, COL_3 TEXT NOT NULL);"
        database = cria_banco
        actual = database.create_table(table)
        assert actual == expected

    def test_should_create_table_when_colums_and_values_informed(self, cria_banco):
        table = {
            "name": "table_name",
            "columns": [{"name": "col_1", "type": "text", "constraints": "not null"}],
        }
        expected = "CREATE TABLE IF NOT EXISTS TABLE_NAME (id INTEGER NOT NULL PRIMARY KEY, COL_1 TEXT NOT NULL);"
        database = cria_banco
        actual = database.create_table(table)
        assert actual == expected
