from src.schemes.course import CourseDB
from src.utils import sql_client
from src.schemes.student import StudentDB


def test_aluno_tem_discipline_id(popula_banco_dados):
    aluno = StudentDB(name="any")
    aluno.discipline_id = 1
    assert aluno.discipline_id == 1


def test_create_novo_course():
    course = CourseDB(name="any")
    sql_client.create(course)
    assert sql_client.get_all(CourseDB)[0].name == "any"
