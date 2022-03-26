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

    def test_should_update_student_situation_when_enrolement_in_course(
        self, setup_database_in_memory
    ):
        expected = "em curso"
        student = DaoAluno(Aluno(), BancoDados(setup_database_in_memory)).get_by_id(1)
        actual = student.calcula_situacao().pega_situacao()

        assert actual == expected

    def test_should_get_student_by_id_when_id_informed(self, setup_database_in_memory):
        expected = "student_name_1"
        actual = (
            DaoAluno(Aluno(), BancoDados(setup_database_in_memory))
            .pega_por_id(1)
            .pega_nome()
        )
        assert actual == expected

    def test_should_update_student_name_in_database_when_asked_for(
        self, setup_database_in_memory
    ):
        id_ = 1
        new_name = "new_name"
        expected = new_name
        student_dao = DaoAluno(Aluno(new_name), BancoDados(setup_database_in_memory))
        student_dao.atualiza(id_)
        actual = student_dao.get_by_id(id_).pega_nome()
        assert actual == expected

    def test_should_return_correct_student_id_from_database_when_asked_for(
        self, setup_database_in_memory
    ):
        id_ = 3
        expected = id_
        actual = (
            DaoAluno(Aluno(), BancoDados(setup_database_in_memory))
            .pega_por_id(id_)
            .pega_id()
        )
        assert actual == expected

    def test_should_get_student_score_from_list_from_databse_when_asked_for(
        self, setup_database_in_memory
    ):
        indice = 3
        expected = 0
        students = DaoAluno(Aluno(), BancoDados(setup_database_in_memory)).get_all()
        actual = students[indice].pega_coeficiente_rendimento()
        assert actual == expected

    def test_lista_alunos_recuperada_banco_com_situacao_correta(
        self, setup_database_in_memory
    ):
        indice = 0
        expected = "em curso"
        students = DaoAluno(Aluno(), BancoDados(setup_database_in_memory)).get_all()
        actual = students[indice].pega_situacao()
        assert actual == expected

    def test_should_get_student_id_from_list_from_databse_when_asked_for(
        self, setup_database_in_memory
    ):
        indice = 2
        expected = 3
        students = DaoAluno(Aluno(), BancoDados(setup_database_in_memory)).get_all()
        actual = students[indice].pega_id()
        assert actual == expected

    def test_id_aluno_recuperado_banco(self, setup_database_in_memory):
        expected = 3
        indice = 2
        students = DaoAluno(Aluno(), BancoDados(setup_database_in_memory)).get_all()
        actual = students[indice].pega_id()
        assert actual == expected

    def test_cr_diferente_zero_retornado_banco(self, setup_database_in_memory):
        expected = 3
        indice = 1
        students = DaoAluno(Aluno(), BancoDados(setup_database_in_memory)).get_all()
        actual = students[indice].pega_coeficiente_rendimento()
        assert actual == expected
