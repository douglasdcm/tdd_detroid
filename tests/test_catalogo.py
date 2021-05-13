from src.catalogo_curso import CatalogoCurso
from src.curso import Curso
from src.materia import Materia


class TestCatalogo:
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
        curso_1 = Curso("marcenaria")        
        curso_1.atualiza_materias(Materia("prego"))
        curso_1.atualiza_materias(Materia("parafuso"))
        curso_1.atualiza_materias(Materia("martelo"))
        curso_2 = Curso("pedreiro")
        curso_2.atualiza_materias(Materia("prego"))
        curso_2.atualiza_materias(Materia("parafuso"))
        curso_2.atualiza_materias(Materia("martelo"))
        expected = list()
        self.catalogo.limpa_catalogo()
        actual = self.catalogo.pega_cursos()
        assert actual == expected

    def test_remove_curso_do_catalogo(self):
        curso_1 = Curso("marcenaria")        
        curso_1.atualiza_materias(Materia("prego"))
        curso_1.atualiza_materias(Materia("parafuso"))
        curso_1.atualiza_materias(Materia("martelo"))
        curso_2 = Curso("pedreiro")
        curso_2.atualiza_materias(Materia("prego"))
        curso_2.atualiza_materias(Materia("parafuso"))
        curso_2.atualiza_materias(Materia("martelo"))
        expected = [curso_1]
        self.catalogo.remove_curso(curso_2)
        actual = self.catalogo.pega_cursos()
        assert actual == expected

    def test_catalogo_vazio_retorna_lista_vazia(self):
        expected = list()
        actual = self.catalogo.pega_cursos()
        assert actual == expected

    def test_adiciona_dois_cursos_no_catalogo(self):
        curso_1 = Curso("marcenaria")        
        curso_1.atualiza_materias(Materia("prego"))
        curso_1.atualiza_materias(Materia("parafuso"))
        curso_1.atualiza_materias(Materia("martelo"))
        curso_2 = Curso("pedreiro")
        curso_2.atualiza_materias(Materia("prego"))
        curso_2.atualiza_materias(Materia("parafuso"))
        curso_2.atualiza_materias(Materia("martelo"))
        expected = [curso_1, curso_2]
        actual = self.catalogo.pega_cursos()
        assert actual == expected

    def test_adiciona_curso_no_catalogo(self):
        curso_1 = Curso("marcenaria")        
        curso_1.atualiza_materias(Materia("prego"))
        curso_1.atualiza_materias(Materia("parafuso"))
        curso_1.atualiza_materias(Materia("martelo"))
        expected = [curso_1]
        actual = self.catalogo.pega_cursos()
        assert actual == expected