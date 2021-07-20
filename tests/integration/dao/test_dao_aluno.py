from src.dao.dao_aluno import DaoAluno
from tests.massa_dados import aluno_nome_1
from src.enums.enums import Situacao
from src.model.aluno import Aluno
from tests.massa_dados import materia_nome_2, materia_nome_3


class TestDaoAluno:

    def _setup_aluno(self, cria_banco, id=1, nome=aluno_nome_1, cr=0,
                     situacao=Situacao.em_curso.value):
        aluno, dao = self._salva_aluno_banco(cria_banco, id, nome, cr,
                                             situacao)
        actual = dao.pega_tudo()
        return actual, aluno

    def _salva_aluno_banco(self, cria_banco, id, nome, cr, situacao):
        aluno = Aluno(nome)
        aluno.define_cr(cr)
        aluno.define_id(id)
        aluno.define_situacao(situacao)
        dao = DaoAluno(aluno, cria_banco)
        dao.salva()
        return aluno, dao

    def _setup_lista_alunos(self, cria_banco, id_=3,
                            situacao=Situacao.em_curso.value,
                            cr=0, nome=None):
        self._setup_aluno(cria_banco)
        self._setup_aluno(cria_banco)
        expected, actual = self._setup_aluno(cria_banco, id=id_,
                                             situacao=situacao,
                                             cr=cr, nome=nome)
        return expected, actual

    def test_aluno_pode_ser_atualizado_banco(self, cria_banco, cria_massa_dados,
                                             cria_curso_com_materias):
        cria_massa_dados
        id_ = "1"
        aluno = DaoAluno(None, cria_banco).pega_por_id(id_)
        curso = cria_curso_com_materias
        materias = {materia_nome_2: 7, materia_nome_3: 9}
        expected = 8
        aluno.inscreve_curso(curso).atualiza_materias_cursadas(materias)
        aluno.pega_coeficiente_rendimento(auto_calculo=True)
        DaoAluno(aluno, cria_banco).atualiza(id_)
        aluno = DaoAluno(None, cria_banco).pega_por_id(id_)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_dao_pega_por_id_retorna_objeto_aluno_com_id_correto(self,
                                                                 cria_banco):
        id_ = 3
        _, expected = self._setup_lista_alunos(cria_banco, id_)
        actual = DaoAluno(None, cria_banco).pega_por_id(id_)
        assert actual.pega_id() == expected.pega_id()

    def test_lista_alunos_recuperada_banco_com_nome_correto(self, cria_banco):
        indice = 2
        nome = aluno_nome_1
        expected, actual = self._setup_lista_alunos(cria_banco, nome=nome)
        assert actual.pega_nome() == expected[indice].pega_nome()

    def test_lista_alunos_recuperada_banco_com_cr_correto(self, cria_banco):
        indice = 2
        cr = 9
        expected, actual = self._setup_lista_alunos(cria_banco, cr=cr)
        assert actual.pega_coeficiente_rendimento() == \
               expected[indice].pega_coeficiente_rendimento()

    def test_lista_alunos_recuperada_banco_com_situacao_correta(self,
                                                                cria_banco):
        indice = 2
        situacao = Situacao.reprovado.value
        expected, actual = self._setup_lista_alunos(cria_banco,
                                                    situacao=situacao)
        assert actual.pega_situacao() == expected[indice].pega_situacao()

    def test_lista_alunos_recuperada_banco_com_id_correto(self, cria_banco):
        indice = 2
        expected, actual = self._setup_lista_alunos(cria_banco)
        assert actual.pega_id() == expected[indice].pega_id()

    def test_situacao_aluno_recuperado_banco(self, cria_banco):
        situacao = "trancado"
        expected, actual = self._setup_aluno(cria_banco, situacao=situacao)
        assert actual.pega_situacao() == expected[0].pega_situacao()

    def test_id_aluno_recuperado_banco(self, cria_banco):
        id_ = 1
        expected, actual = self._setup_aluno(cria_banco, id=id_)
        assert actual.pega_id() == expected[0].pega_id()

    def test_cr_diferente_zero_retornado_banco(self, cria_banco):
        cr = 7
        expected, actual = self._setup_aluno(cria_banco, cr)
        assert actual.pega_coeficiente_rendimento() == \
            expected[0].pega_coeficiente_rendimento()

    def test_coeficiente_rendimento_objeto_aluno_recuperado_banco(self,
                                                                  cria_banco):
        actual, expected = self._setup_aluno(cria_banco)
        assert actual[0].pega_coeficiente_rendimento() == \
               expected.pega_coeficiente_rendimento()

    def test_situacao_objeto_aluno_recuperado_banco(self, cria_banco):
        actual, expected = self._setup_aluno(cria_banco)
        assert actual[0].pega_situacao() == expected.pega_situacao()

    def test_nome_objeto_aluno_recuperado_banco(self, cria_banco):
        actual, expected = self._setup_aluno(cria_banco)
        assert actual[0].pega_nome() == expected.pega_nome()
