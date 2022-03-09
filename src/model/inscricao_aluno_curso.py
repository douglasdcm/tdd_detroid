from src.model.aluno import Aluno


class InscricaoAlunoCurso:

    def __init__(self, aluno, curso):
        """
        Args:
            aluno (Aluno)
            curso (Curso)
        """
        self._aluno_id = aluno.pega_id()
        self._curso_id = curso.pega_id()

    def pega_aluno_id(self):
        return self._aluno_id

    def pega_curso_id(self):
        return self._curso_id

