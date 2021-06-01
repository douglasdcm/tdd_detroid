import pytest
from src.model.gerenciador_curso import GerenciadorCurso
from src.model.curso import Curso
from src.model.materia import Materia

class TestMateria:
    def test_os_nomes_das_materias_nao_precisam_ser_diferentes(self):
        expected = "matematica"
        materia_1 = Materia(expected)
        materia_2 = Materia(expected)
        actual_1 = materia_1.pega_nome()
        actual_2 = materia_2.pega_nome()
        assert actual_1 == actual_2

    def test_cada_materia_deve_ter_um_nome(self):
        expected = "matematica"
        materia = Materia(expected)
        actual = materia.pega_nome()
        assert actual == expected

    def test_materias_curso_devem_ter_identificadores_unicos(self):
        gerenciador_curso = GerenciadorCurso()
        curso = Curso("pedagogia")
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        curso = gerenciador_curso.pega_lista_cursos()[0]
        curso.atualiza_materias(Materia("mat"))
        curso.atualiza_materias(Materia("hist"))
        curso.atualiza_materias(Materia("vet"))
        materias = curso.pega_lista_materias()
        actual_1 = materias[0].pega_identificador_unico()
        actual_2 = materias[1].pega_identificador_unico()
        assert actual_1 != actual_2