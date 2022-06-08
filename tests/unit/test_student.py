from src.student import Student


class TestStudent:

    def test_has_score(self):
        score = 7
        student = Student()
        student.set_score(score)
        actual = student.get_score()
        assert actual == score
