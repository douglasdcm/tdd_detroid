class AssociaCursoMateria:
    def __init__(self, curso, materia):
        """
        Args:
            curso (Curso)
            materia (Materia)
        """
        self._curso_id = curso.pega_id()
        self._materia_id = materia.pega_id()
        self._curso = curso
        self._materia = materia

    def pega_curso_id(self):
        return self._curso_id

    def pega_materia_id(self):
        return self._materia_id

    def pega_curso_atualizado(self):
        return self._curso.atualiza_materias(self._materia)
