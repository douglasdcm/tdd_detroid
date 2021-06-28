from src.model.catalogo_curso import CatalogoCurso
from src.model.coordenador import Coordenador


class CoordenadorCurso(Coordenador):
    def __init__(self, curso,):
        self._curso = curso
        super().__init__()

    def listar_detalhe_alunos(self):              
        return super().listar_detalhe_alunos(self._curso)
