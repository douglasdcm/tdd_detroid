from src.model.catalogo_curso import CatalogoCurso
from src.model.coordenador import Coordenador


class CoordenadorCurso(Coordenador):
    def __init__(self, curso):
        """
        Args:
            curso (Curso): cursos do coordenador
        """
        self._cursos = [curso]
        super().__init__()

    def listar_detalhe_alunos(self):
        return super().listar_detalhe_alunos(self._cursos)

    def adiciona_cursos(self, curso):
        """
            Args:
                cursos (Cursos): curso a ser adicionado
        """
        self._cursos.append(curso)

    def pega_lista_cursos(self):
        return self._cursos
