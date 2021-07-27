from pytest import raises
import pytest
from src.model.aluno import Aluno
from src.model.curso import Curso
from tests.massa_dados import aluno_nome_1, curso_nome_1, \
    materia_nome_1, \
    materia_nome_2, materia_nome_3, materia_nome_4
from src.enums.enums import Situacao


class TestAluno:

    def test_situacao_nao_pode_ser_fora_dos_valores_definidos(self):
        aluno = Aluno()
        situacao = "ausente"
        expected = f"Situação do aluno '{situacao}' não é válida."
        with pytest.raises(Exception, match=expected):
            aluno.define_situacao(situacao)

    def test_aluno_deve_ser_capaz_de_listar_materias_faltantes(self, cria_curso_com_materias):
        aluno = Aluno(aluno_nome_1).inscreve_curso(cria_curso_com_materias)
        materias = {materia_nome_2: 7, materia_nome_3: 9}
        expected = [materia_nome_1]
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.lista_materias_faltantes()
        assert actual == expected

    def test_aluno_pode_pegar_lista_materias_cursadas(self, cria_curso_com_materias):
        curso = cria_curso_com_materias
        materias = {materia_nome_2: 7, materia_nome_3: 9}
        expected = materias
        aluno = Aluno(aluno_nome_1).inscreve_curso(curso)
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.lista_materias_cursadas()
        assert actual == expected

    def test_aluno_deve_ser_capaz_de_listar_as_materias_de_seu_curso(self, cria_curso_com_materias):
        curso = cria_curso_com_materias
        expected = [materia_nome_1, materia_nome_2, materia_nome_3]
        aluno = Aluno(aluno_nome_1).inscreve_curso(curso)
        actual = aluno.lista_materias()
        assert actual == expected

    def test_aluno_nao_pode_se_inscrever_em_curso_cancelado(self, cria_curso_cancelado):
        curso = cria_curso_cancelado
        with pytest.raises(Exception, match="O aluno não pode se inscrever em um curso cancelado"):
            Aluno(aluno_nome_1).inscreve_curso(curso)

    def test_aluno_so_pode_se_inscrever_um_curso(self, cria_curso_com_materias):
        expected = "O aluno só pode se inscrever apenas em um curso"
        curso_1 = cria_curso_com_materias
        curso_2 = cria_curso_com_materias
        aluno = Aluno(None)
        aluno.inscreve_curso(curso_1)
        with pytest.raises(Exception, match=expected):
            aluno.inscreve_curso(curso_2)

    def test_define_cr_retorna_aluno_com_cr_atualizado(self):
        expected = 7
        aluno = Aluno(aluno_nome_1).define_cr(expected)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_define_situacao_retorna_aluno_com_situacao_atualizada(self, cria_curso_com_materias):
        materias = {materia_nome_1: 8, materia_nome_2: 8, materia_nome_3: 8}
        expected = "aprovado"
        aluno = Aluno(aluno_nome_1)
        aluno.inscreve_curso(cria_curso_com_materias)
        aluno.atualiza_materias_cursadas(materias)
        aluno.define_situacao(Situacao.aprovado.value)
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_define_id_retorna_aluno_com_id_atualizado(self):
        expected = 1
        aluno = Aluno(aluno_nome_1).define_id(expected)
        actual = aluno.pega_id()
        assert actual == expected

    def test_aluno_deve_ter_nome(self):
        expected = aluno_nome_1
        aluno = Aluno(expected)
        actual = aluno.pega_nome()
        assert actual == expected

    def test_aluno_nao_pode_increver_curso_sem_materias(self):
        curso = Curso(curso_nome_1)
        aluno = Aluno(aluno_nome_1)
        with raises(Exception, match="Número mínimo que matérias é três. Adicione mais 3"):
            aluno.inscreve_curso(curso)

    def test_aluno_reprovado_curso_nao_pode_trancar_curso(self, inscreve_aluno):
        materias = {materia_nome_1: 0, materia_nome_2: 0, materia_nome_3: 0}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        with raises(Exception, match="Aluno reprovado não pode trancar o curso."):
            aluno.tranca_curso(True)

    def test_aluno_aprovado_curso_nao_pode_trancar_curso(self, inscreve_aluno):
        materias = {materia_nome_1: 10, materia_nome_2: 10, materia_nome_3: 10}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        with raises(Exception, match="Aluno aprovado não pode trancar o curso."):
            aluno.tranca_curso(True)

    def test_aluno_destranca_curso_situacao_volta_para_anterior(self, inscreve_aluno):
        expected = Situacao.em_curso.value
        aluno, _ = inscreve_aluno
        aluno.tranca_curso(True)
        aluno.tranca_curso(False)
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_nao_cursou_nenhuma_materia_retorna_situacao_em_curso(self, inscreve_aluno):
        expected = Situacao.em_curso.value
        aluno, _ = inscreve_aluno
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_nao_inscrito_curso_situacao_retorna_aluno_inexistente(self):
        expected = Situacao.inexistente.value
        aluno = Aluno("UNKNOWN")
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_trancado_quando_calcula_situacao_retorna_trancado(self, inscreve_aluno):
        expected = Situacao.trancado.value
        aluno, _ = inscreve_aluno
        aluno.tranca_curso(True)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_curso_trancado_nao_pode_atualizar_materias_cursadas(self, inscreve_aluno):
        materias = {materia_nome_1: 9}
        aluno, _ = inscreve_aluno
        aluno.tranca_curso(True)
        with raises(Exception, match="Aluno com curso trancado não pode fazer atualizações no sistema."):
            aluno.atualiza_materias_cursadas(materias)

    def test_aluno_curso_trancado_nao_pode_atualizar_notas(self, inscreve_aluno):
        materias = {materia_nome_1: 0}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.tranca_curso(True)
        materias = {materia_nome_1: 8}
        with raises(Exception, match="Aluno com curso trancado não pode fazer atualizações no sistema."):
            aluno.atualiza_materias_cursadas(materias)

    def test_nota_minima_aluno_deve_ser_zero(self, inscreve_aluno):
        aluno, _ = inscreve_aluno
        materias = {materia_nome_1: -1}
        with raises(Exception, match="Nota mínima do aluno não pode ser menor do que 0."):
            aluno.atualiza_materias_cursadas(materias)

    def test_nota_maxima_aluno_deve_ser_dez(self, inscreve_aluno):
        materias = {materia_nome_1: 11}
        aluno, _ = inscreve_aluno
        with raises(Exception, match="Nota máxima do aluno não pode ser maior do que 10."):
            aluno.atualiza_materias_cursadas(materias)

    def test_aluno_so_pode_cursar_materias_do_seu_curso(self, inscreve_aluno):
        expected = 0
        materias = {materia_nome_4: 10}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_calcula_situacao_aluno_baseado_nas_materias_reais(self, inscreve_aluno):
        expected = Situacao.aprovado.value
        materias = {materia_nome_1:8, materia_nome_2:7,materia_nome_3:9}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_lista_materias_pode_ser_atualizada_quando_aluno_nao_cursou_nada(self, inscreve_aluno):
        expected = 8
        materias = {materia_nome_1: 8}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_aprovado_em_segunda_tentativa_entao_nova_nota_entra_no_cr(self, inscreve_aluno):
        expected = 8
        materias = {materia_nome_1: 8, materia_nome_2: 6}
        materia = {materia_nome_2: 8}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.atualiza_materias_cursadas(materia)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_com_nota_sete_ao_fim_do_curso_esta_aprovado(self, inscreve_aluno):
        expected = Situacao.aprovado.value
        materias = {materia_nome_1: 7, materia_nome_2: 7, materia_nome_3: 7}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_com_quantidade_materias_cursadas_menor_que_em_curso_esta_com_situacao_em_curso(self, inscreve_aluno):
        expected = Situacao.em_curso.value
        materias = {materia_nome_1:6, materia_nome_2:6}   
        aluno, _ = inscreve_aluno    
        aluno.atualiza_materias_cursadas(materias)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_cr_menor_sete_fim_curso_esta_reprovado(self, inscreve_aluno):
        expected = Situacao.reprovado.value
        materias = {materia_nome_1:6, materia_nome_2:6, materia_nome_3: 6}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_com_cr_maior_que_sete_ao_fim_do_curso_esta_aprovado(self, inscreve_aluno):
        expected = Situacao.aprovado.value
        materias = {materia_nome_1: 8, materia_nome_2: 8, materia_nome_3: 8}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected
    
    def test_coeficiente_rendimento_calculado_com_decimais(self, inscreve_aluno):
        expected = 1.5
        materias = {materia_nome_1: 1, materia_nome_2: 2}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_cursou_mais_de_duas_materias_tem_cr_igual_a_media(self, inscreve_aluno):
        expected = 6
        materias = {materia_nome_1: 7, materia_nome_2: 3, materia_nome_3: 8}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_cursou_duas_materias_tem_coeficiente_rendimento_igual_media_simples(self, inscreve_aluno):
        expected = 6
        materias = {
            materia_nome_1:6,
            materia_nome_2: 6
            }
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_cursou_uma_materia_tem_coeficiente_rendimento_igual_nota(self, inscreve_aluno):
        expected = 7
        materias = {materia_nome_1: 7}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_coeficiente_rendimento_aluno_novo_tem_que_ser_zero(self):
        expected = 0
        aluno = Aluno(aluno_nome_1)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected
