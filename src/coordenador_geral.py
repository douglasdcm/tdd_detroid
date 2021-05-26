from src.catalogo_curso import CatalogoCurso
from src.coordenador import Coordenador

class CoordenadorGeral(Coordenador):
    def __init__(self):
        self._catalogo = CatalogoCurso()
        self._curso = CatalogoCurso.pega_cursos()
        super().__init__()

    def listar_detalhe_alunos(self):     
        return super().listar_detalhe_alunos(curso=self._curso)
