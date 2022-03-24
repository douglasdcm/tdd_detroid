class TestDatabaseGet:
    def test_should_return_the_student_when_many_columns_informed(
        self, setup_database_in_memory
    ):
        query = "SELECT NAME, SCORE, SITUATION FROM STUDENTS WHERE ID = 1"
        student = [("student_name", 10, "in progress")]
        expected = query, student
        database = setup_database_in_memory
        columns = ["name", "score", "situation"]
        actual = database.get_by_id(columns, "students", 1)
        assert actual == expected

    def test_should_return_the_student_when_all_columns_informed(
        self, setup_database_in_memory
    ):
        query = "SELECT * FROM STUDENTS WHERE ID = 1"
        student = [(1, "student_name", 10, "in progress")]
        expected = query, student
        database = setup_database_in_memory
        actual = database.get_by_id(["*"], "students", 1)
        assert actual == expected

    def test_should_return_the_student_when_id_informed(self, setup_database_in_memory):
        query = "SELECT NAME FROM STUDENTS WHERE ID = 3"
        student = [("student_name_3",)]
        expected = query, student
        database = setup_database_in_memory
        actual = database.get_by_id(["name"], "students", 3)
        assert actual == expected
