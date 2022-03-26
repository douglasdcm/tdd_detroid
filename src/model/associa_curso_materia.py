from src.model.curso import Curso
from src.model.materia import Materia


class AssociaCursoMateria:
    def __init__(self, curso, materia):
        """
        Args:
            curso (Curso)
            materia (Materia)
        """
        if curso is None:
            curso = Curso()
        if materia is None:
            materia = Materia()
        self._curso_id = curso.pega_id()
        self._materia_id = materia.pega_id()
        self._curso = curso
        self._materia = materia

    def update_course_id(self, course_id):
        self._curso_id = course_id

    def update_discipline_id(self, discipline_id):
        self._materia_id = discipline_id

    def pega_curso_id(self):
        return self._curso_id

    def get_course_id(self):
        return self.pega_curso_id()

    def pega_materia_id(self):
        return self._materia_id

    def pega_curso_atualizado(self):
        return self._curso.atualiza_materias(self._materia)

    def pega_curso(self) -> Curso:
        return self._curso

    def pega_materia(self):
        return self._materia

    def atualiza_curso(self, curso):
        self._curso = curso

    def atualiza_materia(self, materia):
        self._materia = materia
