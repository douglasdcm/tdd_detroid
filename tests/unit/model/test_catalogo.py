from src.model.catalogo_curso import CatalogoCurso
from src.model.curso import Curso
from src.model.materia import Materia


class TestCatalogo:

    curso = "marcenaria"
    materia_1 = "prego"
    materia_2 = "parafuso"
    materia_3 = "martelo"

    def setup_method(self, method):
        self.catalogo = CatalogoCurso()
        self.catalogo.limpa_catalogo()

    def teardown_method(self, method):
        self.catalogo.limpa_catalogo()

    def test_singleton_funciona(self):
        catalogo_1 = CatalogoCurso()
        catalogo_2 = CatalogoCurso()
        assert catalogo_1 == catalogo_2

    def test_limpa_catalogo(self):
        self._cria_curso()
        self._cria_curso(curso="pedreiro")
        expected = list()
        self.catalogo.limpa_catalogo()
        actual = self.catalogo.pega_cursos()
        assert actual == expected

    def test_remove_curso_do_catalogo(self):
        curso_1 = self._cria_curso()
        curso_2 = self._cria_curso(curso="pedreiro")
        expected = [curso_1]
        self.catalogo.remove_curso(curso_2)
        actual = self.catalogo.pega_cursos()
        assert actual == expected

    def test_catalogo_vazio_retorna_lista_vazia(self):
        expected = list()
        actual = self.catalogo.pega_cursos()
        assert actual == expected

    def test_adiciona_dois_cursos_no_catalogo(self):
        curso_1 = self._cria_curso()
        curso_2 = self._cria_curso("pedreiro")
        expected = [curso_1, curso_2]
        actual = self.catalogo.pega_cursos()
        assert actual == expected

    def test_adiciona_curso_no_catalogo(self):
        curso_1 = self._cria_curso()
        expected = [curso_1]
        actual = self.catalogo.pega_cursos()
        assert actual == expected

    def _cria_curso(
        self, curso=curso, materia_1=materia_1, materia_2=materia_2, materia_3=materia_3
    ):
        curso_1 = Curso(curso)
        curso_1.atualiza_materias(Materia(materia_1))
        curso_1.atualiza_materias(Materia(materia_2))
        curso_1.atualiza_materias(Materia(materia_3))
        return curso_1
