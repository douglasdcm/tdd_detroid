from pytest import raises
from src.model.curso import Curso
from src.model.unidade import Unidade
from src.model.gerenciador_curso import GerenciadorCurso
from src.model.materia import Materia
from tests.massa_dados import unidade_nome_1, curso_nome_1, curso_nome_2


class TestCurso:
    def test_should_ignore_status_when_invalid(self, setup_available_course):
        status = "unavailable"
        expected = "available"
        course = setup_available_course
        course.define_situacao(status)
        actual = course.pega_situacao()
        assert actual == expected

    def test_shouldnt_pending_course_be_available_when_hasnt_minium_disciplines_(self):
        new_status = "available"
        expected = "pending"
        course = Curso()
        course.define_situacao(new_status)
        actual = course.pega_situacao()
        assert actual == expected

    def test_shouldnt_available_course_be_pending_when_has_minium_disciplines_(
        self, setup_available_course
    ):
        new_status = "pending"
        expected = "available"
        course = setup_available_course
        course.define_situacao(new_status)
        actual = course.pega_situacao()
        assert actual == expected

    def test_shoulnt_cancelled_course_be_pending_when_has_minium_disciplines_(
        self, setup_available_course
    ):
        status = "cancelado"
        new_status = "pending"
        expected = status
        course = setup_available_course
        course.define_situacao(status)
        course.define_situacao(new_status)
        actual = course.pega_situacao()
        assert actual == expected

    def test_shouldnt_cancelled_course_be_available_when_hasnt_minium_disciplines_(
        self,
    ):
        status = "cancelado"
        new_status = "available"
        expected = status
        course = Curso()
        course.define_situacao(status)
        course.define_situacao(new_status)
        actual = course.pega_situacao()
        assert actual == expected

    def test_should_cancelled_courser_be_pending_when_hasnt_minimum_disciplines(self):
        status = "cancelado"
        new_status = "pending"
        expected = new_status
        course = Curso()
        course.define_situacao(status)
        course.define_situacao(new_status)
        actual = course.pega_situacao()
        assert actual == expected

    def test_should_cancelled_course_be_available_when_has_minimun_disciplines(
        self, setup_available_course
    ):
        status = "cancelado"
        new_status = "available"
        expected = new_status
        course = setup_available_course
        course.define_situacao(status)
        course.define_situacao(new_status)
        actual = course.pega_situacao()
        assert actual == expected

    def test_shouldnt_define_status_as_available_when_hasnt_minimun_disciplines(self):
        status = "available"
        expected = "pending"
        course = Curso()
        course.define_situacao(status)
        actual = course.pega_situacao()
        assert actual == expected

    def test_should_status_be_available_when_it_has_minimun_disciplines(
        self, setup_available_course
    ):
        expected = "available"
        course = setup_available_course
        actual = course.pega_situacao()
        assert actual == expected

    def test_should_set_course_status_as_pending_when_doesnt_have_minimun_disciplines(
        self,
    ):
        expected = "pending"
        actual = Curso().pega_situacao()
        assert actual == expected

    def test_should_be_cancelled_when_asked_for_anytime(self, setup_available_course):
        status = "cancelado"
        expected = status
        course = setup_available_course
        course.define_situacao(status)
        actual = course.pega_situacao()
        assert actual == expected

    def test_cursos_devem_ter_nomes_diferentes_se_mesma_unidade(self):
        unidade = Unidade(unidade_nome_1)
        curso_1 = Curso(curso_nome_1)
        curso_2 = Curso(curso_nome_1)
        expected = "Curso já existente na unidade {}".format(unidade_nome_1)
        curso_1.define_unidade(unidade)
        with raises(Exception, match=expected):
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

    def test_nome_curso_deve_ter_no_maximo_dez_letras(self):
        with raises(Exception, match=f"Nome do curso deve ter no máximao 10 letras."):
            Curso("AAAAAAAAAA_")

    def test_curso_nao_deve_adicionar_aluno_sem_nome(self, setup_available_course):
        course = setup_available_course
        with raises(
            Exception,
            match=f"Não foi possível adicionar o aluno ao curso de {course.pega_nome()}",
        ):
            course.adiciona_aluno("")

    def test_curso_deve_ter_todas_materias_com_nomes_diferentes(self):
        curso = Curso("mat")
        curso.atualiza_materias(Materia("alg"))
        curso.atualiza_materias(Materia("calc"))
        with raises(
            Exception, match="O curso não pode ter duas matérias com mesmo nome."
        ):
            curso.atualiza_materias(Materia("alg"))

    def test_curso_com_quantidade_materia_diferente_tres_retorna_uma_excecao(self):
        gerenciador_curso = GerenciadorCurso()
        curso = Curso("jornalismo")
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        gerenciador_curso.atualiza_cursos(curso)
        cursos = gerenciador_curso.pega_lista_cursos()
        materia_1 = Materia("mat")
        materia_2 = Materia("bio")
        cursos[0].atualiza_materias(materia_1)
        cursos[0].atualiza_materias(materia_2)
        with raises(
            Exception, match="Número mínimo que matérias é três. Adicione mais 1."
        ):
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
