from src.dao.dao_curso import DaoCurso
from src.model.curso import Curso
from tests.massa_dados import curso_nome_1
from pytest import raises, fixture
from src.model.banco_dados import BancoDados
from src.model.materia import Materia
from src.dao.dao_associa_curso_materia import DaoAssociaCursoMateria
from src.model.associa_curso_materia import AssociaCursoMateria


class TestDaoCurso:
    @fixture(autouse=False, scope="function")
    def setup(self, setup_database_in_memory):
        self.curso_id = 1
        self.materia_id = 1
        self.__db_connection = setup_database_in_memory
        yield curso_obj, materia_obj

    def __setup_curso(self, setup_database_in_memory, id=None, nome=None):
        course = Curso(curso_nome_1)
        course.atualiza_materias(Materia("m1"))
        course.atualiza_materias(Materia("m2"))
        course.atualiza_materias(Materia("m3"))
        course.define_id(id)
        dao = DaoCurso(course, BancoDados(setup_database_in_memory))
        dao.salva()
        return course, dao

    def __pega_todos_registros(self, setup_database_in_memory, id=None, nome=None):
        course, dao = self.__setup_curso(setup_database_in_memory, id, nome)
        actual = dao.pega_tudo()
        return course, actual

    def __pega_registro_por_id(self, setup_database_in_memory, id=None, nome=None):
        expected, dao = self.__setup_curso(setup_database_in_memory, id, nome)
        actual = dao.pega_por_id(id)
        return expected, actual

    def test_should_update_the_discipline_list_of_course_when_assoc_course_and_discipline(
        self, setup_database_in_memory
    ):
        expected = 3
        course = Curso().define_id(1)
        DaoCurso(course, BancoDados(setup_database_in_memory)).get_by_id(1)
        actual = len(course.pega_lista_materias())
        assert actual == expected

    def test_should_save_course_when_it_has_at_least_3_disciplines(
        self, setup_empty_database_in_memory
    ):
        course = Curso("course_1")
        course.atualiza_materias(Materia("m1"))
        course.atualiza_materias(Materia("m2"))
        course.atualiza_materias(Materia("m3"))

        assert (
            DaoCurso(course, BancoDados(setup_empty_database_in_memory)).salva() is True
        )

    def test_should_not_save_course_when_it_does_not_have_at_least_3_disciplines(
        self, setup_empty_database_in_memory
    ):
        with raises(
            Exception, match="Número mínimo que matérias é três. Adicione mais 3."
        ):
            DaoCurso(
                Curso("course_1"), BancoDados(setup_empty_database_in_memory)
            ).salva()

    def test_curso_recupera_nome_por_id(self, setup_database_in_memory):
        expected, actual = self.__pega_registro_por_id(
            setup_database_in_memory, id=1, nome=curso_nome_1
        )
        assert actual.pega_nome() == expected.pega_nome()

    def test_curso_recupera_id_banco_por_id(self, setup_database_in_memory):
        expected, actual = self.__pega_registro_por_id(
            setup_database_in_memory, id=1, nome=curso_nome_1
        )
        assert actual.pega_id() == expected.pega_id()

    def test_multiplos_cursos_recuperados_banco_dados(self, setup_database_in_memory):
        indice = 2
        self.__setup_curso(setup_database_in_memory)
        self.__setup_curso(setup_database_in_memory)
        expected, actual = self.__pega_todos_registros(
            setup_database_in_memory, id=3, nome=curso_nome_1
        )
        assert actual[indice].pega_id() == expected.pega_id()

    def test_should_the_name_of_course_be_the_same_when_fetched_from_database(
        self, setup_database_in_memory
    ):
        id_ = 1
        expected = "course_1"
        actual = (
            DaoCurso(
                Curso(expected).define_id(id_), BancoDados(setup_database_in_memory)
            )
            .get_by_id(id_)
            .pega_nome()
        )
        assert actual == expected

    def test_curso_id_recuperado_do_banco_dados(self, setup_database_in_memory):
        id_ = 1
        expected = id_
        actual = (
            DaoCurso(Curso(), BancoDados(setup_database_in_memory))
            .get_by_id(id_)
            .pega_id()
        )
        assert actual == expected
