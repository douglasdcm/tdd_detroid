from src.model.catalogo_curso import CatalogoCurso
from src.model.coordenador import Coordenador

class CoordenadorGeral(Coordenador):
    def __init__(self):
        self._catalogo = CatalogoCurso()
        self._curso = CatalogoCurso.pega_cursos()
        super().__init__()

    def listar_detalhe_alunos(self):     
        return super().listar_detalhe_alunos(curso=self._curso)

    def listar_detalhe_alunos_por_banco(self):
        return {"alunos": [{"nome": "joão", "coeficiente rendimento": 6, "materias": {"m1": 6}}]}