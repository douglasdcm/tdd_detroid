from _pytest.python_api import raises
from src.model.catalogo_curso import CatalogoCurso
from src.model.coordenador import Coordenador
from src.enums.enums import SituacaoCurso
from src.exceptions.exceptions import CursoCancelado


class CoordenadorCurso(Coordenador):
    def __init__(self, curso):
        """
        Args:
            curso (Curso): cursos do coordenador
        """
        self._valida_situacao_curso(curso)
        self._cursos = [curso]
        super().__init__()

    def _valida_situacao_curso(self, curso):
        if curso.pega_situacao() == SituacaoCurso.cancelado.value:
            raise CursoCancelado("O coordenador não pode se associar a um curso cancelado.")

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
