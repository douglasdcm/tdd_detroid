from src.dao.dao_aluno import DaoAluno
from tests.massa_dados import aluno_nome_1
from src.enums.enums import Situacao
from src.model.aluno import Aluno
from tests.massa_dados import materia_nome_2, materia_nome_3
from src.model.banco_dados import BancoDados


class TestDaoAluno:
    def __setup_aluno(
        self,
        setup_database_in_memory,
        id=1,
        nome=aluno_nome_1,
        cr=0,
        situacao=Situacao.em_curso.value,
    ):
        aluno, dao = self.__salva_aluno_banco(
            setup_database_in_memory, id, nome, cr, situacao
        )
        actual = dao.pega_tudo()
        return actual, aluno

    def __salva_aluno_banco(self, setup_database_in_memory, id, nome, cr, situacao):
        aluno = Aluno(nome)
        aluno.define_cr(cr)
        aluno.define_id(id)
        aluno.define_situacao(situacao)
        dao = DaoAluno(aluno, setup_database_in_memory)
        dao.salva()
        return aluno, dao

    def __setup_lista_alunos(
        self,
        setup_database_in_memory,
        id_=3,
        situacao=Situacao.em_curso.value,
        cr=0,
        nome=None,
    ):
        self.__setup_aluno(setup_database_in_memory)
        self.__setup_aluno(setup_database_in_memory)
        expected, actual = self.__setup_aluno(
            setup_database_in_memory, id=id_, situacao=situacao, cr=cr, nome=nome
        )
        return expected, actual

    def test_should_update_student_situation_when_enrolement_in_course(
        self, setup_database_in_memory
    ):
        expected = "em curso"
        student = DaoAluno(Aluno(), BancoDados(setup_database_in_memory)).get_by_id(1)
        actual = student.calcula_situacao().pega_situacao()

        assert actual == expected

    def test_should_get_student_by_id_when_id_informed(self, setup_database_in_memory):
        database = setup_database_in_memory
        expected = (
            Aluno()
            .define_id(1)
            .define_cr(10)
            .define_nome("student_name")
            .define_situacao("in progress")
        )
        actual = DaoAluno(Aluno(), database).pega_por_id(1)
        assert actual.pega_nome() == expected.pega_nome()

    def test_aluno_pode_ser_atualizado_banco(
        self, setup_database_in_memory, cria_massa_dados, cria_curso_com_materias
    ):
        cria_massa_dados
        id_ = "1"
        aluno = DaoAluno(Aluno(), setup_database_in_memory).pega_por_id(id_)
        curso = cria_curso_com_materias
        materias = {materia_nome_2: 7, materia_nome_3: 9}
        expected = 8
        aluno.inscreve_curso(curso).atualiza_materias_cursadas(materias)
        aluno.pega_coeficiente_rendimento(auto_calculo=True)
        DaoAluno(aluno, setup_database_in_memory).atualiza(id_)
        aluno = DaoAluno(aluno, setup_database_in_memory).pega_por_id(id_)
        actual = aluno.pega_coeficiente_rendimento()
        assert actual == expected

    def test_dao_pega_por_id_retorna_objeto_aluno_com_id_correto(
        self, setup_database_in_memory
    ):
        id_ = 3
        _, expected = self.__setup_lista_alunos(setup_database_in_memory, id_)
        actual = DaoAluno(Aluno(), setup_database_in_memory).pega_por_id(id_)
        assert actual.pega_id() == expected.pega_id()

    def test_lista_alunos_recuperada_banco_com_nome_correto(
        self, setup_database_in_memory
    ):
        indice = 2
        nome = aluno_nome_1
        expected, actual = self.__setup_lista_alunos(
            setup_database_in_memory, nome=nome
        )
        assert actual.pega_nome() == expected[indice].pega_nome()

    def test_lista_alunos_recuperada_banco_com_cr_correto(
        self, setup_database_in_memory
    ):
        indice = 2
        cr = 9
        expected, actual = self.__setup_lista_alunos(setup_database_in_memory, cr=cr)
        assert (
            actual.pega_coeficiente_rendimento()
            == expected[indice].pega_coeficiente_rendimento()
        )

    def test_lista_alunos_recuperada_banco_com_situacao_correta(
        self, setup_database_in_memory
    ):
        indice = 2
        situacao = Situacao.reprovado.value
        expected, actual = self.__setup_lista_alunos(
            setup_database_in_memory, situacao=situacao
        )
        assert actual.pega_situacao() == expected[indice].pega_situacao()

    def test_lista_alunos_recuperada_banco_com_id_correto(
        self, setup_database_in_memory
    ):
        indice = 2
        expected, actual = self.__setup_lista_alunos(setup_database_in_memory)
        assert actual.pega_id() == expected[indice].pega_id()

    def test_situacao_aluno_recuperado_banco(self, setup_database_in_memory):
        situacao = "trancado"
        expected, actual = self.__setup_aluno(
            setup_database_in_memory, situacao=situacao
        )
        assert actual.pega_situacao() == expected[0].pega_situacao()

    def test_id_aluno_recuperado_banco(self, setup_database_in_memory):
        id_ = 1
        expected, actual = self.__setup_aluno(setup_database_in_memory, id=id_)
        assert actual.pega_id() == expected[0].pega_id()

    def test_cr_diferente_zero_retornado_banco(self, setup_database_in_memory):
        cr = 7
        expected, actual = self.__setup_aluno(setup_database_in_memory, cr)
        assert (
            actual.pega_coeficiente_rendimento()
            == expected[0].pega_coeficiente_rendimento()
        )

    def test_coeficiente_rendimento_objeto_aluno_recuperado_banco(
        self, setup_database_in_memory
    ):
        actual, expected = self.__setup_aluno(setup_database_in_memory)
        assert (
            actual[0].pega_coeficiente_rendimento()
            == expected.pega_coeficiente_rendimento()
        )

    def test_situacao_objeto_aluno_recuperado_banco(self, setup_database_in_memory):
        actual, expected = self.__setup_aluno(setup_database_in_memory)
        assert actual[0].pega_situacao() == expected.pega_situacao()

    def test_nome_objeto_aluno_recuperado_banco(self, setup_database_in_memory):
        actual, expected = self.__setup_aluno(setup_database_in_memory)
        assert actual[0].pega_nome() == expected.pega_nome()
