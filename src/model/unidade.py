class Unidade:

    def __init__(self, nome):
        self.nome = nome
        self.cursos = list()

    def define_cursos(self, curso):
        self.cursos.append(curso)

    def pega_cursos(self):
        return self.cursos

    def pega_nome(self):
        return self.nome
