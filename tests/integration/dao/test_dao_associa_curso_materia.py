from src.model.curso import Curso
from src.model.materia import Materia
from src.model.associa_curso_materia import AssociaCursoMateria
from src.dao.dao_associa_curso_materia import DaoAssociaCursoMateria
from src.dao.dao_materia import DaoMateria
from src.dao.dao_curso import DaoCurso
from pytest import fixture


class TestDaoAssociaCursoMateria:

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco):
        self.curso_id = 1
        self.materia_id = 1
        self.bd = cria_banco
        materia = "Química"
        curso = "Adm"
        DaoMateria(Materia(materia), self.bd).salva()
        DaoCurso(Curso(curso), self.bd).salva()

    def test_curso_com_materials_salvo_banco(self):
        expected = [tuple((1, self.curso_id, self.materia_id))]
        dao = DaoAssociaCursoMateria(AssociaCursoMateria(self.curso_id, 
                                                         self.materia_id), self.bd)
        dao.salva()
        actual = dao.pega_tudo()
        assert actual == expected
