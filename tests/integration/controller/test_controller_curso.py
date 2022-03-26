from src.model.curso import Curso
from src.controller.controller import Controller
from tests.massa_dados import curso_nome_1, discipline_names
from src.model.materia import Materia


class TestControllerCurso:
    def test_curso_criado_banco_dados(self, setup_database_in_memory):
        expected = curso_nome_1
        course = Curso(curso_nome_1)
        for discipline in [
            discipline_names[0],
            discipline_names[1],
            discipline_names[2],
        ]:
            course.atualiza_materias(Materia(discipline))
        controller = Controller(course, setup_database_in_memory)
        controller.salva()
        actual = controller.get_by_biggest_id().pega_nome()
        assert actual == expected
