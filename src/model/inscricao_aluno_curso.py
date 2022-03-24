from src.model.aluno import Aluno
from src.model.curso import Curso


class InscricaoAlunoCurso:
    def __init__(self, aluno=None, curso=None):
        """
        Args:
            aluno (Aluno)
            curso (Curso)
        """
        if aluno is None:
            aluno = Aluno()
        if curso is None:
            curso = Curso()
        self._aluno = aluno
        self._curso = curso
        self.__student_id = aluno.pega_id()
        self.__course_id = curso.pega_id()

    def update_student_id(self, id_):
        self.__student_id = id_

    def update_course_id(self, id_):
        self.__course_id = id_

    def get_student_id(self):
        return self.__student_id

    def get_course_id(self):
        return self.__course_id

    def pega_aluno(self) -> Aluno:
        return self._aluno

    def pega_curso(self) -> Curso:
        return self._curso

    def atualiza_aluno(self, aluno):
        self._aluno = aluno

    def atualiza_curso(self, curso):
        self._curso = curso
