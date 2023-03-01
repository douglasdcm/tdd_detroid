from src.controllers import disciplines
from src.schemes.discipline import MateriaBd
from src.utils import sql_client
from pytest import mark, raises
from src.utils.exceptions import ErrorDiscipline


@mark.parametrize("course_id", ["string", ""])
def test_create_discipline_raises_error_if_course_id_invalid(course_id):
    with raises(ErrorDiscipline, match="Course id is not a valid integer"):
        disciplines.create(name="any", course_id=course_id)

def test_materia_create(popula_banco_dados):
    disciplines.create(name="any", course_id=1)
    discipline_id = sql_client.get_maximum(MateriaBd).id
    assert sql_client.get(MateriaBd, discipline_id).name == "any"
