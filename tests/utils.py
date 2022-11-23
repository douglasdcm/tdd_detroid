import uuid
from src.modelos.curso import CursoModelo
from src.modelos.materia import MateriaModelo


def cria_materia(conn, curso_id):
    nome_aleatorio = str(uuid.uuid4())
    MateriaModelo(conn).cria(nome_aleatorio, curso_id)


def cria_curso(conn):
    nome_aleatorio = str(uuid.uuid4())
    CursoModelo(conn).cria(nome_aleatorio)
