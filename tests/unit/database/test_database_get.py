class TestDatabaseGet:
    def test_should_return_the_student_when_many_columns_informed(
        self, setup_database_in_memory
    ):
        query = "SELECT NAME, SCORE, SITUATION FROM STUDENT WHERE ID = 1"
        student = [("student_name", 10, "in progress")]
        expected = query, student
        database = setup_database_in_memory
        columns = ["name", "score", "situation"]
        actual = database.get_by_id(columns, "student", 1)
        assert actual == expected

    def test_should_return_the_student_when_all_columns_informed(
        self, setup_database_in_memory
    ):
        query = "SELECT * FROM STUDENT WHERE ID = 1"
        student = [(1, "student_name", 10, "in progress")]
        expected = query, student
        database = setup_database_in_memory
        actual = database.get_by_id(["*"], "student", 1)
        assert actual == expected

    def test_should_return_the_student_when_id_informed(self, setup_database_in_memory):
        query = "SELECT NAME FROM STUDENT WHERE ID = 3"
        student = [("student_name_3",)]
        expected = query, student
        database = setup_database_in_memory
        actual = database.get_by_id(["name"], "student", 3)
        assert actual == expected
