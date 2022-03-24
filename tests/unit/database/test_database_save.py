from pytest import fixture


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
        database = setup_database_in_memory
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

    def test_should_insert_one_item_when_one_item_informed(
        self, setup_database_in_memory
    ):
        student = [
            {
                "name": "student_name",
            }
        ]
        table = {
            "name": "students",
            "columns": [{"name": "name", "type": "text", "constraints": "not null"}],
        }
        database = setup_database_in_memory
        database.create_table(table)
        expected = 'insert into students (name) values ("student_name")'
        actual, _ = database.save(table["name"], student)
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
