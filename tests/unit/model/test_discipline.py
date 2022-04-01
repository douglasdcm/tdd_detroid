from src.model.discipline import Discipline


class TestDiscipline:
    def test_shoud_discipline_have_unique_id_when_created(self):
        id_ = 1
        assert Discipline().set_id(id_)

    def test_should_discipline_have_name_when_specified(self):
        name = "test_name"
        assert Discipline().set_name(name)

    def test_should_discipline_has_grade_updated_when_asked_for(self):
        grade = 4
        discipline = Discipline()
        actual = discipline.set_grade(grade)
        assert actual
