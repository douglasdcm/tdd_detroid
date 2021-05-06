class Curso:

    def __init__(self):
        self._lista_materias = list()
        self._minimo_materia = 3
    
    def atualiza_materias(self, materia):
        if len(self._lista_materias) < self._minimo_materia:
            self._lista_materias.append(materia)

    def pega_lista_materias(self):
        quantidade_materias = len(self._lista_materias)
        if quantidade_materias == self._minimo_materia:
            return self._lista_materias
        delta = self._minimo_materia - quantidade_materias
        raise Exception(f"Número mínimo que matérias é três. Adicione mais {delta}.")