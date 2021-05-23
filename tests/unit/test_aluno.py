import pytest, sqlite3
from src.aluno import Aluno
from src.curso import Curso
from src.materia import Materia
from src.banco_dados import BancoDados

class TestAluno():
    aluno = None
    bd = None

    def setup_method(self, method):
        self.bd = BancoDados(sqlite3.connect(":memory:"))
        self.aluno = Aluno("joao")
        curso = Curso("pedagogia")
        curso.atualiza_materias(Materia("mat"))
        curso.atualiza_materias(Materia("hist"))
        curso.atualiza_materias(Materia("geo"))
        self.aluno.inscreve_curso(curso)

    def teardown_method(self, method):
        self.aluno = None
        self.bd.fecha_conexao_existente()

    def test_aluno_deve_ter_nome(self):
        expected = "joao"
        actual = self.aluno.pega_nome()
        assert actual == expected

    def test_aluno_nao_pode_increver_curso_sem_materias(self):
        curso = Curso("agricultura")
        aluno = Aluno("jose")
        with pytest.raises(Exception, match="Número mínimo que matérias é três. Adicione mais 3"):
            aluno.inscreve_curso(curso)

    def test_aluno_reprovado_curso_nao_pode_trancar_curso(self):
        materias = {"mat": 0, "hist": 0, "geo": 0}
        self.aluno.atualiza_materias_cursadas(materias)
        with pytest.raises(Exception, match="Aluno reprovado não pode trancar o curso."):
            self.aluno.tranca_curso(True)

    def test_aluno_aprovado_curso_nao_pode_trancar_curso(self):
        materias = {"mat": 10, "hist": 10, "geo": 10}
        self.aluno.atualiza_materias_cursadas(materias)
        with pytest.raises(Exception, match="Aluno aprovado não pode trancar o curso."):
            self.aluno.tranca_curso(True)

    def test_aluno_destranca_curso_situacao_volta_para_anterior(self):
        expected = "em curso"
        self.aluno.tranca_curso(True)
        self.aluno.tranca_curso(False)
        actual = self.aluno.pega_situacao()
        assert actual == expected

    def test_aluno_nao_cursou_nenhuma_materia_retorna_situacao_em_curso(self):
        expected = "em curso"
        self.aluno.calcula_situacao()
        actual = self.aluno.pega_situacao()
        assert actual == expected

    def test_aluno_nao_inscrito_curso_situacao_retorna_aluno_inexistente(self):
        expected = "aluno inexistente"
        aluno = Aluno("marta")
        aluno.calcula_situacao()
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_aluno_trancado_quando_calcula_situacao_retorna_trancado(self):
        expected = "trancado"
        self.aluno.tranca_curso(True)
        self.aluno.calcula_situacao()
        actual = self.aluno.pega_situacao()
        assert actual == expected

    def test_aluno_curso_trancado_nao_pode_atualizar_materias_cursadas(self):
        materias = {"mat": 9}
        self.aluno.tranca_curso(True)
        with pytest.raises(Exception, match="Aluno com curso trancado não pode fazer atualizações no sistema."):
            self.aluno.atualiza_materias_cursadas(materias)

    def test_aluno_curso_trancado_nao_pode_atualizar_notas(self):
        materias = {"mat": 0}
        self.aluno.atualiza_materias_cursadas(materias)
        self.aluno.tranca_curso(True)
        materias = {"mat": 8}
        with pytest.raises(Exception, match="Aluno com curso trancado não pode fazer atualizações no sistema."):
            self.aluno.atualiza_materias_cursadas(materias)

    def test_nota_minima_aluno_deve_ser_zero(self):
        materias = {"hist":-1}
        with pytest.raises(Exception, match="Nota mínima do aluno não pode ser menor do que 0."):
            self.aluno.atualiza_materias_cursadas(materias)

    def test_nota_maxima_aluno_deve_ser_dez(self):
        materias = {"mat":11}
        with pytest.raises(Exception, match="Nota máxima do aluno não pode ser maior do que 10."):
            self.aluno.atualiza_materias_cursadas(materias)

    def test_aluno_so_pode_cursar_materias_do_seu_curso(self):
        expected = 0
        materias = {"bio": 10}
        self.aluno.atualiza_materias_cursadas(materias)
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_calcula_situacao_aluno_baseado_nas_materias_reais(self):
        expected = "aprovado"
        materias = {"mat":8, "hist":7,"geo":9}
        self.aluno.atualiza_materias_cursadas(materias)
        self.aluno.calcula_situacao()
        actual = self.aluno.pega_situacao()
        assert actual == expected

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
        materias = {"mat": 7, "hist": 7, "geo": 7}
        self.aluno.atualiza_materias_cursadas(materias)
        self.aluno.calcula_situacao()
        actual = self.aluno.pega_situacao()
        assert actual == expected

    def test_aluno_com_quantidade_materias_cursadas_menor_que_em_curso_esta_com_situacao_em_curso(self):
        expected = "em curso"
        materias = {"mat":6, "hist":6}       
        self.aluno.atualiza_materias_cursadas(materias)
        self.aluno.calcula_situacao()
        actual = self.aluno.pega_situacao()
        assert actual == expected

    def test_aluno_cr_menor_sete_fim_curso_esta_reprovado(self):
        expected = "reprovado"
        materias = {"mat":6, "hist":6, "geo": 6}
        self.aluno.atualiza_materias_cursadas(materias)
        self.aluno.calcula_situacao()
        actual = self.aluno.pega_situacao()
        assert actual == expected

    def test_aluno_com_cr_maior_que_sete_ao_fim_do_curso_esta_aprovado(self):
        expected = "aprovado"
        materias = {"hist": 8, "mat": 8, "geo": 8}
        self.aluno.atualiza_materias_cursadas(materias)
        self.aluno.calcula_situacao()
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
            "mat":6,
            "hist": 6
            }
        self.aluno.atualiza_materias_cursadas(materias)
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_aluno_cursou_uma_materia_tem_coeficiente_rendimento_igual_nota(self):
        expected = 7
        materias = {"mat": 7}
        self.aluno.atualiza_materias_cursadas(materias)
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_coeficiente_rendimento_aluno_novo_tem_que_ser_zero(self):
        expected = 0
        actual = self.aluno.pega_coeficiente_rendimento()
        assert actual == expected
