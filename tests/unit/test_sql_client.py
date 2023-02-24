from src.schemes.course import CourseDB
from src.utils import sql_client
from src.schemes.student import StudentDB


def test_aluno_tem_materia_id(popula_banco_dados):
    aluno = StudentDB(nome="any")
    aluno.materia_id = 1
    assert aluno.materia_id == 1


def test_create_novo_curso():
    curso = CourseDB(nome="any")
    sql_client.create(curso)
    assert sql_client.get_all(CourseDB)[0].nome == "any"
