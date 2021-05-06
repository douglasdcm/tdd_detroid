import pytest
from src.aluno import Aluno

class TestAluno():
    aluno = None

    def setup_method(self, method):
        self.aluno = Aluno()

    def teardown_method(self, method):
        self.aluno = None

    def test_lista_materias_pode_ser_atualizada_quando_aluno_nao_cursou_nada(self):
        expected = 8
        materias = {"mat": 8}
        self.aluno.atualiza_materias_cursadas(materias)
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_aprovado_em_segunda_tentativa_entao_nova_nota_entra_no_cr(self):
        expected = 8
        materias = {"mat": 8, "hist": 6}
        materia = {"hist": 8}
        self.aluno.atualiza_materias_cursadas(materias)
        self.aluno.atualiza_materias_cursadas(materia)
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_com_nota_sete_ao_fim_do_curso_esta_aprovado(self):
        expected = "aprovado"
        quantidade_materias_cursadas = 3
        quantidade_materias_curso = 3
        materias = {"mat": 7, "hist": 7, "geo": 7}
        self.aluno.atualiza_materias_cursadas(materias)
        self.aluno.calcula_situacao(quantidade_materias_cursadas,
                                    quantidade_materias_curso)
        actual = self.aluno.pega_situacao()
        assert actual == expected

    def test_aluno_com_quantidade_materias_cursadas_menor_que_em_curso_esta_com_situacao_em_curso(self):
        expected = "em curso"
        quantidade_materias_cursadas = 2
        quantidade_materias_curso = 3
        coeficiente = 6
        self.aluno.calcula_situacao(quantidade_materias_cursadas,
                                    quantidade_materias_curso)
        actual = self.aluno.pega_situacao()
        assert actual == expected 

    def test_aluno_cr_menor_sete_fim_curso_esta_reprovado(self):
        expected = "reprovado"
        quantidade_materias_curso = 3
        quantidade_materias_cursadas = 3
        coeficiciente = 6
        self.aluno.calcula_situacao(quantidade_materias_cursadas,
                                    quantidade_materias_curso)
        actual = self.aluno.pega_situacao()
        assert actual == expected

    def test_aluno_com_cr_maior_que_sete_ao_fim_do_curso_esta_aprovado(self):
        expected = "aprovado"
        quantidade_materias_curso = 3
        quantidade_materias_cursadas = 3
        materias = {"hist": 8, "mat": 8, "geo": 8}
        self.aluno.atualiza_materias_cursadas(materias)
        self.aluno.calcula_situacao(quantidade_materias_cursadas,
                                    quantidade_materias_curso)
        actual = self.aluno.pega_situacao()
        assert actual == expected
    
    def test_coeficiente_rendimento_calculado_com_decimais(self):
        expected = 1.5
        materias = {"mat": 1, "hist": 2}
        self.aluno.atualiza_materias_cursadas(materias)
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_cursou_mais_de_duas_materias_tem_cr_igual_a_media(self):
        expected = 6
        materias = {"mat": 7, "hist": 3, "geo": 8}
        self.aluno.atualiza_materias_cursadas(materias)
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_cursou_duas_materias_tem_coeficiente_rendimento_igual_media_simples(self):
        expected = 6
        materias = {
            "matematica":6,
            "história": 6
            }
        self.aluno.atualiza_materias_cursadas(materias)
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_cursou_uma_materia_tem_coeficiente_rendimento_igual_nota(self):
        expected = 7
        materias = {"matematica": 7}
        self.aluno.atualiza_materias_cursadas(materias)
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_coeficiente_rendimento_aluno_novo_tem_que_ser_zero(self):
        expected = 0
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected
