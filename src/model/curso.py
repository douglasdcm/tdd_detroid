from src.model.materia import Materia
from src.model.unidade import Unidade
from src.model.i_model import IModel
import time
from src.model.catalogo_curso import CatalogoCurso
from src.model import aluno as student
from src.exceptions.exceptions import MaximoCaracteres, UnidadeInvalida, MateriaInvalida
from typing import List
from src.enums.enums import SituacaoCurso


class Curso(IModel):
    def __init__(self, nome=""):
        self.__list_disciplines: List[Materia] = list()
        self.__minimum_disciplines = 3
        self._maximo_caracteres = 10
        self._identificador_unico = time.time()
        self._nome = nome
        self._lista_alunos = list()
        self.__adiciona_catalogo_cursos()
        self._id = None
        self._unidade = None
        self.__situacao = SituacaoCurso.pending.value
        self.__valida_parametros(nome)

    def __valida_parametros(self, nome):
        if len(nome) > self._maximo_caracteres:
            raise MaximoCaracteres(
                "Nome do curso deve ter no máximao {} letras.".format(
                    self._maximo_caracteres
                )
            )

    def define_situacao(self, situacao):
        if situacao == SituacaoCurso.cancelado.value:
            self.__situacao = situacao
        elif (
            self.__situacao == SituacaoCurso.cancelado.value
            and situacao == self.__calculate_status()
        ):
            self.__situacao = situacao
        elif situacao in [SituacaoCurso]:
            self.__situacao = self.__calculate_status()

    def pega_situacao(self):
        return self.__situacao

    def pega_unidade(self):
        return self._unidade

    def define_unidade(self, unidade: Unidade):
        if self._nome in unidade.pega_cursos():
            raise UnidadeInvalida(
                "Curso já existente na unidade {}".format(unidade.pega_nome())
            )
        self._unidade = unidade.pega_nome()
        unidade.define_cursos(self._nome)

    def pega_id(self):
        return self._id

    def define_id(self, id):
        self._id = id
        return self

    def __adiciona_catalogo_cursos(self):
        catalogo = CatalogoCurso()
        catalogo.adiciona_curso(self)

    def pega_nome(self):
        return self._nome

    def pega_identificador_unico(self):
        return self._identificador_unico

    def atualiza_materias(self, materia: Materia):
        """
        Args:
            material (Materia)
        Returns:
            self
        """
        if len(self.__list_disciplines) == 0:
            self.__list_disciplines.append(materia)
        else:
            for item in self.__list_disciplines:
                if item.pega_nome() == materia.pega_nome():
                    raise MateriaInvalida(
                        "O curso não pode ter duas matérias com mesmo nome."
                    )
            if len(self.__list_disciplines) < self.__minimum_disciplines:
                self.__list_disciplines.append(materia)
        self.__situacao = self.__calculate_status()
        return self

    def __calculate_status(self):
        if len(self.__list_disciplines) >= self.__minimum_disciplines:
            status = SituacaoCurso.available.value
        else:
            status = SituacaoCurso.pending.value
        return status

    def pega_lista_materias(self):
        quantidade_materias = len(self.__list_disciplines)
        if quantidade_materias == self.__minimum_disciplines:
            return self.__list_disciplines
        delta = self.__minimum_disciplines - quantidade_materias
        raise Exception(f"Número mínimo que matérias é três. Adicione mais {delta}.")

    def get_disciplines(self):
        return self.pega_lista_materias()

    def pega_lista_alunos(self):
        return self._lista_alunos

    def get_students(self):
        return self.pega_lista_alunos()

    def add_student(self, student):
        self.adiciona_aluno(student)

    def adiciona_aluno(self, aluno):
        if isinstance(aluno, student.Aluno):
            self._lista_alunos.append(aluno)
        else:
            raise Exception(
                "Não foi possível adicionar o aluno ao curso de {}.".format(
                    self.pega_nome()
                )
            )
