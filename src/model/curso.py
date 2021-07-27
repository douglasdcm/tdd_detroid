from src.model.unidade import Unidade
from src.model.i_model import IModel
import time
from src.model.catalogo_curso import CatalogoCurso
from src.model.aluno import Aluno
from src.exceptions.exceptions import MaximoCaracteres, UnidadeInvalida, MateriaInvalida


class Curso(IModel):

    def __init__(self, nome=""):
        self._lista_materias = list()
        self._minimo_materia = 3
        self._maximo_caracteres = 10
        self._identificador_unico = time.time()
        self._nome = nome
        self._lista_alunos = list()
        self._adiciona_catalogo_cursos()
        self._id = None
        self._unidade = None
        self._situacao = None
        self._valida_parametros(nome)

    def _valida_parametros(self, nome):
        if len(nome) > self._maximo_caracteres:
            raise MaximoCaracteres("Nome do curso deve ter no máximao {} letras.".format(
                self._maximo_caracteres))

    def define_situacao(self, situacao):
        self._situacao = situacao

    def pega_situacao(self):
        return self._situacao

    def pega_unidade(self):
        return self._unidade

    def define_unidade(self, unidade: Unidade):
        if self._nome in unidade.pega_cursos():
            raise UnidadeInvalida("Curso já existente na unidade {}".format(unidade.pega_nome()))
        self._unidade = unidade.pega_nome()
        unidade.define_cursos(self._nome)

    def pega_id(self):
        return self._id

    def define_id(self, id):
        self._id = id
        return self

    def _adiciona_catalogo_cursos(self):
        catalogo = CatalogoCurso()
        catalogo.adiciona_curso(self)

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
                    raise MateriaInvalida("O curso não pode ter duas matérias com mesmo nome.")
            if len(self._lista_materias) < self._minimo_materia:
                self._lista_materias.append(materia)

    def pega_lista_materias(self):
        quantidade_materias = len(self._lista_materias)
        if quantidade_materias == self._minimo_materia:
            return self._lista_materias
        delta = self._minimo_materia - quantidade_materias
        raise Exception(f"Número mínimo que matérias é três. Adicione mais {delta}.")

    def pega_lista_alunos(self):
        return self._lista_alunos

    def adiciona_aluno(self, aluno):
        if isinstance(aluno, Aluno):
            self._lista_alunos.append(aluno)
        else:
            raise Exception(f"Não foi possível adicionar o aluno ao curso de {self.pega_nome()}.")
