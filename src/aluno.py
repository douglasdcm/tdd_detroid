class Aluno:
    def __init__(self):
        self._coeficiente_rendimento = 0
        self._situacao = "em curso"
        self.media_minima = 7
        self._materias_cursadas = dict()

    def atualiza_materias_cursadas(self, materias):
        for key, value in materias.items():
            self._materias_cursadas[key] = value
        self._calcula_coficiente_rendimento()
    
    def calcula_situacao(self,
                        quantidade_materias_cursadas, 
                        quantidade_materias_curso):
        if self._coeficiente_rendimento >= self.media_minima and quantidade_materias_cursadas == quantidade_materias_curso:
            self._situacao = "aprovado"
        elif quantidade_materias_cursadas < quantidade_materias_curso:
            self._situacao = "em curso"
        else:
            self._situacao = "reprovado"
    
    def pega_situacao(self):
        return self._situacao
    
    def pega_coeficiente_rendimento(self):
        self._calcula_coficiente_rendimento()
        return self._coeficiente_rendimento

    def _calcula_coficiente_rendimento(self):
        quantidade = 0
        soma_notas = 0
        for key in self._materias_cursadas:
            soma_notas += self._materias_cursadas[key]
            quantidade += 1
        if soma_notas > 0:
            self._coeficiente_rendimento = soma_notas / quantidade
