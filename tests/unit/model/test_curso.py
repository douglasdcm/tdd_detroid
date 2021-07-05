from typing import Coroutine
import pytest
from src.model.curso import Curso
from src.model.unidade import Unidade
from src.model.gerenciador_curso import GerenciadorCurso
from src.model.materia import Materia
from tests.massa_dados import unidade_nome_1, unidade_nome_2, curso_nome_1, \
    curso_nome_2


class TestCurso:

    def test_cursos_devem_ter_nomes_diferentes_se_mesma_unidade(self):
        unidade = Unidade(unidade_nome_1)
        curso_1 = Curso(curso_nome_1)
        curso_2 = Curso(curso_nome_1)
        expected = "Curso já existente na unidade {}".format(unidade_nome_1)
        curso_1.define_unidade(unidade)
        with pytest.raises(Exception, match=expected):
            curso_2.define_unidade(unidade)

    def test_cursos_podem_ter_nomes_iguais_se_unidades_diferentes(self):
        unidade = Unidade(unidade_nome_1)
        curso_1 = Curso(curso_nome_1)
        curso_2 = Curso(curso_nome_2)
        expected = unidade_nome_1
        curso_1.define_unidade(unidade)
        curso_2.define_unidade(unidade)
        actual = curso_1.pega_unidade()
        assert actual == expected


    def setup_method(self, method):
        self.curso = Curso("Administra")
        self.curso.atualiza_materias(Materia("Política"))
        self.curso.atualiza_materias(Materia("Trabalho"))
        self.curso.atualiza_materias(Materia("Pessoas"))

    def teardown_method(self, method):
        self.curso = None

    def test_nome_curso_deve_ter_no_maximo_dez_letras(self):
        with pytest.raises(Exception, match=f"Nome do curso deve ter no máximao 10 letras."):
            Curso("AAAAAAAAAA_")

    def test_curso_nao_deve_adicionar_aluno_sem_nome(self):
        with pytest.raises(Exception, match=f"Não foi possível adicionar o aluno ao curso de {self.curso.pega_nome()}"):
            self.curso.adiciona_aluno("")

    def test_curso_deve_ter_todas_materias_com_nomes_diferentes(self):
        curso = Curso("mat")
        curso.atualiza_materias(Materia("alg"))
        curso.atualiza_materias(Materia("calc"))
        # deve ser ignorado
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
        expected = "administra"
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
        # deve ser ignorado
        cursos[0].atualiza_materias(Materia("vet"))
        actual = len(cursos[0].pega_lista_materias())
        assert actual == expected

    def test_numero_cursos_deve_ser_tres(self):
        expected = 3
        self.gerenciador_curso = GerenciadorCurso()
        self.curso = Curso("vet")
        self.gerenciador_curso.atualiza_cursos(self.curso)
        self.gerenciador_curso.atualiza_cursos(self.curso)
        self.gerenciador_curso.atualiza_cursos(self.curso)
        # deve ser ignorado
        self.gerenciador_curso.atualiza_cursos(self.curso)    
        actual = len(self.gerenciador_curso.pega_lista_cursos())
        assert actual == expected
