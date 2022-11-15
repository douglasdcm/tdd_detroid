from enum import Enum


class Tipos(Enum):
    MATERIAS = "materias"
    CURSOS = "cursos"
    ALUNOS = "alunos"


class ErroCurso(Exception):
    pass


class Manager:
    def __init__(self, conn) -> None:
        self._conn = conn

    def pode_criar_curso(self):
        query_livre = f"select count(*) from {Tipos.MATERIAS.value} group by curso;"
        resultado = self._conn.roda_query(query_livre)

        if len(self._conn.lista_tudo(Tipos.CURSOS.value)) < 3:
            return True
        if len(resultado) == 0:
            raise ErroCurso(
                "Necessários 3 cursos com 3 três matérias para se criar novos cursos"
            )
        for linha in resultado:
            if linha[0] < 3:
                raise ErroCurso(
                    "Necessários 3 cursos com 3 três matérias para se criar novos cursos"
                )
        return True

    def pode_criar_materia(self):
        if len(self._conn.lista_tudo(Tipos.CURSOS.value)) < 3:
            raise ErroCurso("Necessários 3 cursos para se criar a primeira matéria")
        return True
