import pytest
from src.curso import Curso
from src.gerenciador_curso import GerenciadorCurso
from src.materia import Materia

class TestCurso:

    def test_curso_com_quantidade_materia_diferente_tres_retorna_uma_excecao(self):
        gerenciador_curso = GerenciadorCurso()
        curso = Curso()
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        cursos = gerenciador_curso.pega_lista_cursos()
        materia = Materia("mat")
        cursos[0].atualiza_materias(materia)
        cursos[0].atualiza_materias(materia)
        with pytest.raises(Exception):
            actual = cursos[0].pega_lista_materias()

    def test_cada_curso_deve_ter_tres_materias(self):
        expected = 3
        gerenciador_curso = GerenciadorCurso()
        curso = Curso()
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        cursos = gerenciador_curso.pega_lista_cursos()
        materia = Materia("mat")
        cursos[0].atualiza_materias(materia)
        cursos[0].atualiza_materias(materia)
        cursos[0].atualiza_materias(materia)
        cursos[0].atualiza_materias(materia) #deve ser ignorado
        actual = len(cursos[0].pega_lista_materias())
        assert actual == expected

    def test_numero_cursos_deve_ser_tres(self):
        expected = 3
        self.gerenciador_curso = GerenciadorCurso()
        self.curso = Curso()
        self.gerenciador_curso.atualiza_cursos(self.curso)
        self.gerenciador_curso.atualiza_cursos(self.curso)
        self.gerenciador_curso.atualiza_cursos(self.curso)
        self.gerenciador_curso.atualiza_cursos(self.curso) #deve ser ignorado    
        actual = len(self.gerenciador_curso.pega_lista_cursos())
        assert actual == expected