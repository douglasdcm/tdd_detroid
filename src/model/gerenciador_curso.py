from src.model.curso import Curso


class GerenciadorCurso:
    def __init__(self):
        self._lista_cursos = list()

    def atualiza_cursos(self, curso):
        if len(self._lista_cursos) < 3:
            self._lista_cursos.append(curso)

    def pega_lista_cursos(self):
        quantidade_cursos = len(self._lista_cursos)
        minimo_cursos = 3
        if quantidade_cursos == minimo_cursos:
            return self._lista_cursos
        delta = minimo_cursos - quantidade_cursos
        print(f"O número mínimo de cursos é três. Adicione mais {delta}")
        return None
