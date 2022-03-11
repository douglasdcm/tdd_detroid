from src.model.curso import Curso
from src.model.materia import Materia
from src.model.associa_curso_materia import AssociaCursoMateria
from src.dao.dao_associa_curso_materia import DaoAssociaCursoMateria
from src.dao.dao_materia import DaoMateria
from src.dao.dao_curso import DaoCurso
from pytest import fixture


class TestDaoAssociaCursoMateria:
    @fixture(autouse=False, scope="function")
    def setup(self, cria_banco):
        self.curso_id = 1
        self.materia_id = 1
        self.bd = cria_banco
        materia = "Química"
        curso = "Adm"
        materia_obj = DaoMateria(Materia(materia), self.bd).salva()
        course_controller = DaoCurso(Curso(curso), self.bd)
        course_controller.salva()
        curso_obj = course_controller.get_by_biggest_id()
        curso_obj.define_id(self.curso_id)
        materia_obj.define_id(self.materia_id)
        yield curso_obj, materia_obj

    def test_curso_com_materials_salvo_banco(self, setup):
        expected = [tuple((1, self.curso_id, self.materia_id))]
        curso_obj, materia_obj = setup
        dao = DaoAssociaCursoMateria(
            AssociaCursoMateria(
                curso_obj,
                materia_obj,
            ),
            self.bd,
        )
        dao.salva()
        actual = dao.pega_tudo()
        assert actual == expected
