class AssociaCursoMateria:
    def __init__(self, curso_id, materia_id):
        self._curso_id = curso_id
        self._materia_id = materia_id

    def pega_curso_id(self):
        return self._curso_id

    def pega_materia_id(self):
        return self._materia_id
