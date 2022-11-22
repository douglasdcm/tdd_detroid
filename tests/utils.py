import uuid
from src.materias import Materias
from src.cursos import Cursos


def cria_materia(conn, curso_id):
    nome_aleatorio = str(uuid.uuid4())
    Materias(conn).cria(nome_aleatorio, curso_id)


def cria_curso(conn):
    nome_aleatorio = str(uuid.uuid4())
    Cursos(conn).cria(nome_aleatorio)
