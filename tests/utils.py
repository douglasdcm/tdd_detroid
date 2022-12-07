import uuid
from src.models.curso import CursoModelo
from src.models.materia import MateriaModelo
from src.models.aluno import AlunoModelo
from src.config import conn
from pytest import raises
from src.utils.utils import inicializa_tabelas


def popula_banco_dados():
    "Cria 3 cursos com 3 matérias cada, cria aluno, inscreve em um dos cursos e inscreve em 3 matérias"
    inicializa_tabelas(conn)
    cria_curso(conn)
    cria_curso(conn)
    cria_curso(conn)
    for i in range(3):
        for _ in range(3):
            cria_materia(conn, i + 1)
            cria_materia(conn, i + 1)
            cria_materia(conn, i + 1)
    cria_aluno_completo(conn)


def cria_aluno_completo(conn):
    aluno = AlunoModelo(conn)
    aluno.cria("test_manual")
    aluno.inscreve_curso(1)
    with raises(Exception):
        aluno.inscreve_materia(1)
    with raises(Exception):
        aluno.inscreve_materia(2)
    aluno.inscreve_materia(3)


def cria_materia(conn, curso_id):
    nome_aleatorio = str(uuid.uuid4())
    MateriaModelo(conn).cria(nome_aleatorio, curso_id)


def cria_curso(conn):
    nome_aleatorio = str(uuid.uuid4())
    CursoModelo(conn).cria(nome_aleatorio)
