from src.schemes.course import CourseDB
from tests.config import conn
from src.schemes.student import StudentDB


def test_aluno_tem_materia_id(popula_banco_dados):
    aluno = StudentDB(nome="any")
    aluno.materia_id = 1
    assert aluno.materia_id == 1


def test_cria_novo_curso():
    curso = CourseDB(nome="any")
    conn.cria(curso)
    assert conn.lista_tudo(CourseDB)[0].nome == "any"
