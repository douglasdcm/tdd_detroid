from src.model.catalogo_curso import CatalogoCurso
from src.model.coordenador import Coordenador


class CoordenadorGeral(Coordenador):
    def __init__(self):
        self._catalogo = CatalogoCurso()
        self._cursos = CatalogoCurso.pega_cursos()
        self._id = None
        super().__init__()

    def define_id(self, id):
        self._id = id
        return self

    def pega_id(self):
        return self._id

    def listar_detalhe_alunos(self, cursos=None):
        return super().listar_detalhe_alunos(cursos=self._cursos)
