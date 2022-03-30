from pytest import raises
import pytest
from src.model.student_manager import StudentManager
from src.model.aluno import Aluno
from src.model.curso import Curso
from tests.massa_dados import (
    aluno_nome_1,
    curso_nome_1,
    materia_nome_1,
    materia_nome_2,
    materia_nome_3,
    materia_nome_4,
)
from src.enums.enums import Situacao
from src.model.materia import Materia


class TestStudentManager:
    # def test_aluno_deve_ser_capaz_de_listar_materias_faltantes(
    #     self, cria_curso_com_materias
    # ):
    #     aluno = Aluno(aluno_nome_1).inscreve_curso(cria_curso_com_materias)
    #     materias = {materia_nome_2: 7, materia_nome_3: 9}
    #     expected = [materia_nome_1]
    #     aluno.atualiza_materias_cursadas(materias)
    #     actual = aluno.lista_materias_faltantes()
    #     assert actual == expected

    # def test_aluno_pode_pegar_lista_materias_cursadas(self, cria_curso_com_materias):
    #     curso = cria_curso_com_materias
    #     materias = {materia_nome_2: 7, materia_nome_3: 9}
    #     expected = materias
    #     aluno = Aluno(aluno_nome_1).inscreve_curso(curso)
    #     aluno.atualiza_materias_cursadas(materias)
    #     actual = aluno.lista_materias_cursadas()
    #     assert actual == expected

    # def test_aluno_deve_ser_capaz_de_listar_as_materias_de_seu_curso(
    #     self, cria_curso_com_materias
    # ):
    #     curso = cria_curso_com_materias
    #     expected = [materia_nome_1, materia_nome_2, materia_nome_3]
    #     aluno = Aluno(aluno_nome_1).inscreve_curso(curso)
    #     actual = aluno.lista_materias()
    #     assert actual == expected

    # def test_aluno_nao_pode_se_inscrever_em_curso_cancelado(self, cria_curso_cancelado):
    #     curso = cria_curso_cancelado
    #     with pytest.raises(
    #         Exception, match="O aluno não pode se inscrever em um curso cancelado"
    #     ):
    #         Aluno(aluno_nome_1).inscreve_curso(curso)

    # def test_aluno_so_pode_se_inscrever_um_curso(self, cria_curso_com_materias):
    #     expected = "O aluno só pode se inscrever apenas em um curso"
    #     curso_1 = cria_curso_com_materias
    #     curso_2 = cria_curso_com_materias
    #     aluno = Aluno(None)
    #     aluno.inscreve_curso(curso_1)
    #     with pytest.raises(Exception, match=expected):
    #         aluno.inscreve_curso(curso_2)

    # def test_aluno_nao_pode_increver_curso_sem_materias(self):
    #     curso = Curso(curso_nome_1)
    #     aluno = Aluno(aluno_nome_1)
    #     with raises(
    #         Exception, match="Número mínimo que matérias é três. Adicione mais 3"
    #     ):
    #         aluno.inscreve_curso(curso)

    # def test_aluno_reprovado_curso_nao_pode_trancar_curso(self, inscreve_aluno):
    #     materias = {materia_nome_1: 0, materia_nome_2: 0, materia_nome_3: 0}
    #     aluno, _ = inscreve_aluno
    #     aluno.atualiza_materias_cursadas(materias)
    #     with raises(Exception, match="Aluno reprovado não pode trancar o curso."):
    #         aluno.tranca_curso(True)

    # def test_aluno_aprovado_curso_nao_pode_trancar_curso(self, inscreve_aluno):
    #     materias = {materia_nome_1: 10, materia_nome_2: 10, materia_nome_3: 10}
    #     aluno, _ = inscreve_aluno
    #     aluno.atualiza_materias_cursadas(materias)
    #     with raises(Exception, match="Aluno aprovado não pode trancar o curso."):
    #         aluno.tranca_curso(True)

    # def test_aluno_nao_cursou_nenhuma_materia_retorna_situacao_em_curso(
    #     self, inscreve_aluno
    # ):
    #     expected = "in progress"
    #     aluno, _ = inscreve_aluno
    #     aluno.calcula_situacao()
    #     actual = aluno.pega_situacao()
    #     assert actual == expected

    # def test_aluno_nao_inscrito_curso_situacao_retorna_aluno_inexistente(self):
    #     expected = Situacao.inexistente.value
    #     aluno = Aluno("UNKNOWN")
    #     aluno.calcula_situacao()
    #     actual = aluno.pega_situacao()
    #     assert actual == expected

    # def test_aluno_curso_trancado_nao_pode_atualizar_materias_cursadas(
    #     self, inscreve_aluno
    # ):
    #     materias = {materia_nome_1: 9}
    #     aluno, _ = inscreve_aluno
    #     aluno.tranca_curso(True)
    #     with raises(
    #         Exception,
    #         match="Aluno com curso trancado não pode fazer atualizações no sistema.",
    #     ):
    #         aluno.atualiza_materias_cursadas(materias)

    # def test_aluno_curso_trancado_nao_pode_atualizar_notas(self, inscreve_aluno):
    #     materias = {materia_nome_1: 0}
    #     aluno, _ = inscreve_aluno
    #     aluno.atualiza_materias_cursadas(materias)
    #     aluno.tranca_curso(True)
    #     materias = {materia_nome_1: 8}
    #     with raises(
    #         Exception,
    #         match="Aluno com curso trancado não pode fazer atualizações no sistema.",
    #     ):
    #         aluno.atualiza_materias_cursadas(materias)

    # def test_aluno_so_pode_cursar_materias_do_seu_curso(self, inscreve_aluno):
    #     expected = 0
    #     materias = {materia_nome_4: 10}
    #     aluno, _ = inscreve_aluno
    #     aluno.atualiza_materias_cursadas(materias)
    #     actual = aluno.pega_coeficiente_rendimento()
    #     assert actual == expected

    # def test_calcula_situacao_aluno_baseado_nas_materias_reais(self, inscreve_aluno):
    #     expected = Situacao.aprovado.value
    #     materias = {materia_nome_1: 8, materia_nome_2: 7, materia_nome_3: 9}
    #     aluno, _ = inscreve_aluno
    #     aluno.atualiza_materias_cursadas(materias)
    #     aluno.calcula_situacao()
    #     actual = aluno.pega_situacao()
    #     assert actual == expected

    # def test_lista_materias_pode_ser_atualizada_quando_aluno_nao_cursou_nada(
    #     self, inscreve_aluno
    # ):
    #     expected = 8
    #     materias = {materia_nome_1: 8}
    #     aluno, _ = inscreve_aluno
    #     aluno.atualiza_materias_cursadas(materias)
    #     actual = aluno.pega_coeficiente_rendimento()
    #     assert actual == expected

    # def test_aluno_com_quantidade_materias_cursadas_menor_que_em_curso_esta_com_situacao_em_curso(
    #     self, inscreve_aluno
    # ):
    #     expected = Situacao.in_progress.value
    #     materias = {materia_nome_1: 6, materia_nome_2: 6}
    #     aluno, _ = inscreve_aluno
    #     aluno.atualiza_materias_cursadas(materias)
    #     aluno.calcula_situacao()
    #     actual = aluno.pega_situacao()
    #     assert actual == expected

    # def test_aluno_cursou_mais_de_duas_materias_tem_cr_igual_a_media(
    #     self, inscreve_aluno
    # ):
    #     expected = 6
    #     materias = {materia_nome_1: 7, materia_nome_2: 3, materia_nome_3: 8}
    #     aluno, _ = inscreve_aluno
    #     aluno.atualiza_materias_cursadas(materias)
    #     actual = aluno.pega_coeficiente_rendimento()
    #     assert actual == expected

    # def test_aluno_cursou_duas_materias_tem_coeficiente_rendimento_igual_media_simples(
    #     self, inscreve_aluno
    # ):
    #     expected = 6
    #     materias = {materia_nome_1: 6, materia_nome_2: 6}
    #     aluno, _ = inscreve_aluno
    #     aluno.atualiza_materias_cursadas(materias)
    #     actual = aluno.pega_coeficiente_rendimento()
    #     assert actual == expected

    def test_should_student_score_be_equal_grade_when_finished_one_discipline(
        self, subscribe_student
    ):
        grade_1 = 8
        expected = 8
        subscrition = subscribe_student
        student = subscrition.get_student()
        course = subscrition.get_course()
        disciplines = course.get_disciplines()
        manager = StudentManager(student)
        manager.update_grade(disciplines[0], grade_1)
        actual = student.get_score()
        assert actual == expected

    def test_should_student_score_be_equal_main_when_finished_many_disciplines(
        self, subscribe_student
    ):
        grade_1 = 8
        grade_2 = 6
        expected = 7
        subscrition = subscribe_student
        student = subscrition.get_student()
        course = subscrition.get_course()
        disciplines = course.get_disciplines()
        manager = StudentManager(student)
        manager.update_grade(disciplines[0], grade_1)
        manager.update_grade(disciplines[1], grade_2)
        actual = student.get_score()
        assert actual == expected
