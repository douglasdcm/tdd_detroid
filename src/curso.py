import time

class Curso:

    def __init__(self, nome):
        self._lista_materias = list()
        self._minimo_materia = 3
        self._identificador_unico = time.time()
        self._nome = nome
        
    def pega_nome(self):
        return self._nome
    
    def pega_identificador_unico(self):
        return self._identificador_unico
    
    def atualiza_materias(self, materia):
        if len(self._lista_materias) == 0:
            self._lista_materias.append(materia)
        else:
            for item in self._lista_materias:
                if item.pega_nome() == materia.pega_nome():
                    return
            if len(self._lista_materias) < self._minimo_materia:
                    self._lista_materias.append(materia)

    def pega_lista_materias(self):
        quantidade_materias = len(self._lista_materias)
        if quantidade_materias == self._minimo_materia:
            return self._lista_materias
        delta = self._minimo_materia - quantidade_materias
        raise Exception(f"Número mínimo que matérias é três. Adicione mais {delta}.")
    

            