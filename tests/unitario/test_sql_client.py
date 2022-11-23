from src.esquemas.curso import CursoBd
from tests.config import conn
from src.esquemas.aluno import AlunoBd


def test_aluno_tem_materia_id(popula_banco_dados):
    aluno = AlunoBd(nome="any")
    aluno.materia_id = 1
    assert aluno.materia_id == 1


def test_cria_novo_curso():
    curso = CursoBd(nome="any")
    conn.cria(curso)
    assert conn.lista_tudo(CursoBd)[0].nome == "any"
