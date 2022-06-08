from src import persister
from src.student import Student
from src.persister import Persister
from pytest import fixture


class TestStudentPersistence:

    @fixture
    def setup(self):
        persister = Persister()
        persister.save_student(1000, Student())
        persister.save_student(1000, Student())
        persister.save_student(1000, Student())
        persister.save_student(1000, Student())
        yield persister

    def test_save_student(self, setup):
        id_ = 4
        student = Student()
        persister = setup
        persister.save_student(1000, student)

        actual = persister.get_student(id_)
        assert actual == student

    def test_save_score_when_many_students(self, setup):
        score = 8
        id_ = 2
        persister = setup
        student = persister.get_student(id_)
        student.set_score(score)
        persister.save_student(id_, student)
        student_obj = persister.get_student(id_)

        actual = student_obj.get_score()
        assert actual == score
