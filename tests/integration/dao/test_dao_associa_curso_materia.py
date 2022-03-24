from src.model.curso import Curso
from src.model.materia import Materia
from src.model.associa_curso_materia import AssociaCursoMateria
from src.dao.dao_associa_curso_materia import DaoAssociaCursoMateria
from src.dao.dao_materia import DaoMateria
from src.dao.dao_curso import DaoCurso
from pytest import fixture, raises
from src.model.banco_dados import BancoDados


class TestDaoAssociaCursoMateria:
    @fixture(autouse=False, scope="function")
    def setup(self, setup_database_in_memory):
        self.curso_id = 1
        self.materia_id = 1
        self.__db_connection = setup_database_in_memory
        materia = "Química"
        curso = "Adm"
        materia_obj = DaoMateria(Materia(materia), self.__db_connection).salva()
        course_controller = DaoCurso(Curso(curso), self.__db_connection)
        course_controller.salva()
        curso_obj = course_controller.get_by_biggest_id()
        curso_obj.define_id(self.curso_id)
        materia_obj.define_id(self.materia_id)
        yield curso_obj, materia_obj

    def test_should_return_3_course_ids_when_get_by_course_id(self, setup):
        course_obj, discipline_obj = setup
        expected = 3
        actual = len(
            DaoAssociaCursoMateria(
                AssociaCursoMateria(course_obj, discipline_obj), self.__db_connection
            ).get_by_course_id(1)
        )
        assert actual == expected

    def test_should_update_discipline_list_of_course_when_new_discipline_associated(
        self, setup
    ):
        course_obj, discipline_obj = setup
        expected = 1
        DaoAssociaCursoMateria(
            AssociaCursoMateria(course_obj, discipline_obj), self.__db_connection
        ).salva()
        course = Curso()
        course_obj = DaoCurso(course, self.__db_connection).get_by_id(1)
        actual = course_obj.pega_

    def test_should_save_course_with_disciplines_in_database(self, setup):
        expected = [tuple((1, self.curso_id, self.materia_id))]
        curso_obj, materia_obj = setup
        dao = DaoAssociaCursoMateria(
            AssociaCursoMateria(
                curso_obj,
                materia_obj,
            ),
            self.__db_connection,
        )
        dao.salva()
        actual = dao.pega_tudo()
        assert actual == expected
