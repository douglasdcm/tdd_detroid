from src.model.curso import Curso
from src.model.materia import Materia
from src.model.associa_curso_materia import AssociaCursoMateria
from src.dao.dao_associa_curso_materia import DaoAssociaCursoMateria
from src.dao.dao_materia import DaoMateria
from src.dao.dao_curso import DaoCurso
from pytest import fixture, raises
from src.model.banco_dados import BancoDados


class TestDaoAssociaCursoMateria:
    def test_should_return_3_course_ids_when_get_by_course_id(
        self, setup_database_in_memory
    ):
        expected = 3
        actual = len(
            DaoAssociaCursoMateria(
                AssociaCursoMateria(None, None),
                BancoDados(setup_database_in_memory),
            ).get_by_course_id(1)
        )
        assert actual == expected

    def test_should_save_course_with_disciplines_in_database(
        self, setup_database_in_memory
    ):
        id_ = 2
        expected = id_
        dao = DaoAssociaCursoMateria(
            AssociaCursoMateria(
                Curso().define_id(id_),
                Materia().define_id(id_),
            ),
            BancoDados(setup_database_in_memory),
        )
        dao.salva()
        actual = dao.get_by_biggest_id().pega_curso_id()
        assert actual == expected
