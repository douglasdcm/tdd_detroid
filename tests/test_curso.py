import pytest
from src.curso import Curso
from src.gerenciador_curso import GerenciadorCurso
from src.materia import Materia

class TestCurso:

    def test_curso_deve_ter_todas_materias_com_nomes_diferentes(self):
        curso = Curso("mat")
        curso.atualiza_materias(Materia("alg"))
        curso.atualiza_materias(Materia("calc"))
        #deve ser ignorado
        curso.atualiza_materias(Materia("alg"))
        with pytest.raises(Exception, match="Número mínimo que matérias é três. Adicione mais 1."):
            curso.pega_lista_materias()

    def test_curso_com_quantidade_materia_diferente_tres_retorna_uma_excecao(self):
        gerenciador_curso = GerenciadorCurso()
        curso = Curso("jornalismo")
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        cursos = gerenciador_curso.pega_lista_cursos()
        materia = Materia("mat")
        cursos[0].atualiza_materias(materia)
        cursos[0].atualiza_materias(materia)
        with pytest.raises(Exception, match="Número mínimo que matérias é três. Adicione mais 2."):
            cursos[0].pega_lista_materias()

    def test_os_cursos_podem_ter_nomes_iguais(self):
        curso_1 = Curso("adm")
        curso_2 = Curso("adm")
        actual_1 = curso_1.pega_nome()
        actual_2 = curso_2.pega_nome()
        assert actual_1 == actual_2

    def test_todo_curso_deve_ter_nome(self):
        expected = "administracao"
        curso = Curso(nome=expected)
        actual = curso.pega_nome()
        assert actual == expected

    def test_curso_deve_ter_identificador_unico(self):
        curso_1 = Curso("adm")
        curso_2 = Curso("mad")
        actual_1 = curso_1.pega_identificador_unico()
        actual_2 = curso_2.pega_identificador_unico()
        assert actual_1 != actual_2

    def test_cada_curso_deve_ter_tres_materias(self):
        expected = 3
        gerenciador_curso = GerenciadorCurso()
        curso = Curso("med")
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        cursos = gerenciador_curso.pega_lista_cursos()
        cursos[0].atualiza_materias(Materia("mat"))
        cursos[0].atualiza_materias(Materia("adm"))
        cursos[0].atualiza_materias(Materia("med"))
        cursos[0].atualiza_materias(Materia("vet")) #deve ser ignorado
        actual = len(cursos[0].pega_lista_materias())
        assert actual == expected

    def test_numero_cursos_deve_ser_tres(self):
        expected = 3
        self.gerenciador_curso = GerenciadorCurso()
        self.curso = Curso("vet")
        self.gerenciador_curso.atualiza_cursos(self.curso)
        self.gerenciador_curso.atualiza_cursos(self.curso)
        self.gerenciador_curso.atualiza_cursos(self.curso)
        self.gerenciador_curso.atualiza_cursos(self.curso) #deve ser ignorado    
        actual = len(self.gerenciador_curso.pega_lista_cursos())
        assert actual == expected