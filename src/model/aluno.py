class Aluno:
    def __init__(self, nome):
        self._coeficiente_rendimento = 0
        self._situacao = "em curso"
        self.media_minima = 7
        self._materias_cursadas = dict()
        self._curso = None
        self._nota_maxima = 10
        self._nota_minima = 0
        self._nome = nome
        self._id = None

    def tranca_curso(self, decisao):
        self.calcula_situacao()
        if self._situacao == "aprovado" or self._situacao == "reprovado":
            raise Exception(f"Aluno {self._situacao} não pode trancar o curso.")
        else:
            if decisao:
                self._situacao = "trancado"
            else:
                self._situacao = "destrancando"
                self.calcula_situacao()

    def inscreve_curso(self, curso):
        if curso.pega_lista_materias():
            self._curso = curso        
            curso.adiciona_aluno(self)

    def pega_nome(self):
        return self._nome

    def atualiza_materias_cursadas(self, materias):
        if self._situacao == "trancado":
            raise Exception("Aluno com curso trancado não pode fazer atualizações no sistema.")
        for key, value in materias.items():
            if value > self._nota_maxima:
                raise Exception(f"Nota máxima do aluno não pode ser maior do que 10.")
            if value < self._nota_minima:
                raise Exception(f"Nota mínima do aluno não pode ser menor do que 0.")
        lista_materias = self._curso.pega_lista_materias()
        for key, value in materias.items():
            for materia in lista_materias:
                if key == materia.pega_nome():
                    self._materias_cursadas[key] = value
                    break
        self._calcula_coficiente_rendimento()

    def pega_materias_cursadas(self):
        return self._materias_cursadas
    
    def calcula_situacao(self):
        if self._curso is None:
            self._situacao = "aluno inexistente"
        elif self._situacao == "trancado":
            pass
        else:
            quantidade_materias_cursadas = 0
            for _ in self._materias_cursadas:
                quantidade_materias_cursadas += 1
            quantidade_materias_curso = len(self._curso.pega_lista_materias())
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
