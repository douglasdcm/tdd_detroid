from pytest import raises
from src.model.aluno import Aluno
from src.model.curso import Curso

class TestAluno:


    def test_aluno_deve_ter_nome(self):
        expected = "Pedro"
        aluno = Aluno(expected)
        actual = aluno.pega_nome()
        assert actual == expected

    def test_aluno_nao_pode_increver_curso_sem_materias(self):
        curso = Curso("agricultura")
        aluno = Aluno("Joaquim")
        with raises(Exception, match="Número mínimo que matérias é três. Adicione mais 3"):
            aluno.inscreve_curso(curso)

    def test_aluno_reprovado_curso_nao_pode_trancar_curso(self, inscreve_aluno):
        materias = {"mat": 0, "hist": 0, "geo": 0}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        with raises(Exception, match="Aluno reprovado não pode trancar o curso."):
            aluno.tranca_curso(True)

    def test_aluno_aprovado_curso_nao_pode_trancar_curso(self, inscreve_aluno):
        materias = {"mat": 10, "hist": 10, "geo": 10}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        with raises(Exception, match="Aluno aprovado não pode trancar o curso."):
            aluno.tranca_curso(True)

    def test_aluno_destranca_curso_situacao_volta_para_anterior(self, inscreve_aluno):
        expected = "em curso"
        aluno, _ = inscreve_aluno
        aluno.tranca_curso(True)
        aluno.tranca_curso(False)
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_nao_cursou_nenhuma_materia_retorna_situacao_em_curso(self, inscreve_aluno):
        expected = "em curso"
        aluno, _ = inscreve_aluno
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_nao_inscrito_curso_situacao_retorna_aluno_inexistente(self):
        expected = "aluno inexistente"
        aluno = Aluno("UNKNOWN")
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_trancado_quando_calcula_situacao_retorna_trancado(self, inscreve_aluno):
        expected = "trancado"
        aluno, _ = inscreve_aluno
        aluno.tranca_curso(True)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_curso_trancado_nao_pode_atualizar_materias_cursadas(self, inscreve_aluno):
        materias = {"mat": 9}
        aluno, _ = inscreve_aluno
        aluno.tranca_curso(True)
        with raises(Exception, match="Aluno com curso trancado não pode fazer atualizações no sistema."):
            aluno.atualiza_materias_cursadas(materias)

    def test_aluno_curso_trancado_nao_pode_atualizar_notas(self, inscreve_aluno):
        materias = {"mat": 0}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.tranca_curso(True)
        materias = {"mat": 8}
        with raises(Exception, match="Aluno com curso trancado não pode fazer atualizações no sistema."):
            aluno.atualiza_materias_cursadas(materias)

    def test_nota_minima_aluno_deve_ser_zero(self, inscreve_aluno):
        aluno, _ = inscreve_aluno
        materias = {"hist":-1}
        with raises(Exception, match="Nota mínima do aluno não pode ser menor do que 0."):
            aluno.atualiza_materias_cursadas(materias)

    def test_nota_maxima_aluno_deve_ser_dez(self, inscreve_aluno):
        materias = {"mat":11}
        aluno, _ = inscreve_aluno
        with raises(Exception, match="Nota máxima do aluno não pode ser maior do que 10."):
            aluno.atualiza_materias_cursadas(materias)

    def test_aluno_so_pode_cursar_materias_do_seu_curso(self, inscreve_aluno):
        expected = 0
        materias = {"bio": 10}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_calcula_situacao_aluno_baseado_nas_materias_reais(self, inscreve_aluno):
        expected = "aprovado"
        materias = {"mat":8, "hist":7,"geo":9}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_lista_materias_pode_ser_atualizada_quando_aluno_nao_cursou_nada(self, inscreve_aluno):
        expected = 8
        materias = {"mat": 8}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_aprovado_em_segunda_tentativa_entao_nova_nota_entra_no_cr(self, inscreve_aluno):
        expected = 8
        materias = {"mat": 8, "hist": 6}
        materia = {"hist": 8}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.atualiza_materias_cursadas(materia)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_com_nota_sete_ao_fim_do_curso_esta_aprovado(self, inscreve_aluno):
        expected = "aprovado"
        materias = {"mat": 7, "hist": 7, "geo": 7}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_com_quantidade_materias_cursadas_menor_que_em_curso_esta_com_situacao_em_curso(self, inscreve_aluno):
        expected = "em curso"
        materias = {"mat":6, "hist":6}   
        aluno, _ = inscreve_aluno    
        aluno.atualiza_materias_cursadas(materias)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_cr_menor_sete_fim_curso_esta_reprovado(self, inscreve_aluno):
        expected = "reprovado"
        materias = {"mat":6, "hist":6, "geo": 6}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_com_cr_maior_que_sete_ao_fim_do_curso_esta_aprovado(self, inscreve_aluno):
        expected = "aprovado"
        materias = {"hist": 8, "mat": 8, "geo": 8}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected
    
    def test_coeficiente_rendimento_calculado_com_decimais(self, inscreve_aluno):
        expected = 1.5
        materias = {"mat": 1, "hist": 2}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_cursou_mais_de_duas_materias_tem_cr_igual_a_media(self, inscreve_aluno):
        expected = 6
        materias = {"mat": 7, "hist": 3, "geo": 8}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_cursou_duas_materias_tem_coeficiente_rendimento_igual_media_simples(self, inscreve_aluno):
        expected = 6
        materias = {
            "mat":6,
            "hist": 6
            }
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_cursou_uma_materia_tem_coeficiente_rendimento_igual_nota(self, inscreve_aluno):
        expected = 7
        materias = {"mat": 7}
        aluno, _ = inscreve_aluno
        aluno.atualiza_materias_cursadas(materias)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_coeficiente_rendimento_aluno_novo_tem_que_ser_zero(self):
        expected = 0
        aluno = Aluno("Renato")
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected
