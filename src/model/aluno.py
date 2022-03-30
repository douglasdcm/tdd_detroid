from src.enums.enums import SituacaoCurso, Situacao
from src.exceptions.exceptions import CursoUnico, CursoCancelado, SituacaoInvalida
from src.model import curso
from src.model import materia


class Aluno:
    def __init__(self, nome=None):
        self._coeficiente_rendimento = 0
        self.__score = 0
        self.__status = Situacao.unsubscribed.value
        self.media_minima = 7
        self.__disciplines = []
        self.__course = None
        self._nota_maxima = 10
        self._nota_minima = 0
        self._nome = nome
        self._id = None

    def define_nome(self, nome):
        self._nome = nome
        return self

    def set_status(self, status):
        self.__status = status
        return self

    def define_situacao(self, situacao: Situacao):
        situacao_valida = [e.value for e in Situacao]
        if situacao not in situacao_valida:
            raise SituacaoInvalida(
                "Situação do aluno '{}' não é válida.".format(situacao)
            )
        if situacao == Situacao.trancado.value:
            self.tranca_curso(True)
        else:
            self.calcula_situacao()
        return self

    def define_cr(self, cr):
        """
        Args:
            cr (int): coeficiente de rendimento atualizado.
        Returns:
            self
        """
        self._coeficiente_rendimento = cr
        return self

    def define_id(self, id_):
        self._id = id_
        return self

    def pega_id(self):
        return self._id

    def tranca_curso(self, decisao):
        self.calcula_situacao()
        if (
            self.__status == Situacao.aprovado.value
            or self.__status == Situacao.reprovado.value
        ):
            raise Exception(f"Aluno {self.__status} não pode trancar o curso.")
        else:
            if decisao:
                self.__status = Situacao.trancado.value
            else:
                self.__status = Situacao.in_progress.value
                self.calcula_situacao()
        return self

    def lista_materias_faltantes(self):
        materias_curso = self.__course.pega_lista_materias()
        lista_materias_faltantes = list()
        materias_cursadas = list()
        for materia, _ in self.__disciplines.items():
            materias_cursadas.append(materia)
        for materia in materias_curso:
            nome_materia = materia.pega_nome()
            if nome_materia not in materias_cursadas:
                lista_materias_faltantes.append(nome_materia)
        return lista_materias_faltantes

    def lista_materias(self):
        lista_materias = list()
        materias = self.__course.pega_lista_materias()
        for materia in materias:
            lista_materias.append(materia.pega_nome())
        return lista_materias

    def inscreve_curso(self, curso):
        """
        Args:
            curso (Curso): nome do curso que o aluno está se inscrevendo
        """
        if curso.pega_situacao() == SituacaoCurso.cancelado.value:
            raise CursoCancelado("O aluno não pode se inscrever em um curso cancelado.")
        if self.__course is not None:
            raise CursoUnico("O aluno só pode se inscrever apenas em um curso")
        if curso.pega_lista_materias():
            self.__course = curso
            curso.adiciona_aluno(self)
            self.calcula_situacao()
        return self

    def set_course(self, course: curso.Curso):
        self.__course = course
        self.calcula_situacao()

    def set_score(self, score: float):
        self.__score = score

    def pega_nome(self):
        return self._nome

    def lista_materias_cursadas(self):
        return self.__disciplines

    def update_discipline(self, discipline: str, grade: float):
        self.__disciplines.append(materia.Materia().set_grade(grade))

    def atualiza_materias_cursadas(self, materias):
        """
        Args:
            materias (dict): dicionário com matérias cursadas e notas a serem atualizadas
            Por examplo: {materia_nome_1: 8, materia_nome_2: 7,materia_nome_3: 9}
        """
        if self.__status == "trancado":
            raise Exception(
                "Aluno com curso trancado não pode fazer atualizações no sistema."
            )
        for key, value in materias.items():
            if value > self._nota_maxima:
                raise Exception(f"Nota máxima do aluno não pode ser maior do que 10.")
            if value < self._nota_minima:
                raise Exception(f"Nota mínima do aluno não pode ser menor do que 0.")
        lista_materias = self.__course.pega_lista_materias()
        for key, value in materias.items():
            for materia in lista_materias:
                if key == materia.pega_nome():
                    self.__disciplines[key] = value
                    break
        self._calcula_coficiente_rendimento()
        return self

    def pega_materias_cursadas(self):
        return self.__disciplines

    def get_disciplines(self):
        return self.__disciplines

    def calcula_situacao(self):
        """Define the status of the student, like 'approved', 'reproved', 'in progress'"""
        if self.__course is None:
            self.__status = "aluno não matriculado"
        elif self.__status == "trancado":
            pass
        else:
            quantidade_materias_cursadas = 0
            for _ in self.__disciplines:
                quantidade_materias_cursadas += 1
            quantidade_materias_curso = len(self.__course.pega_lista_materias())
            if (
                self._coeficiente_rendimento >= self.media_minima
                and quantidade_materias_cursadas == quantidade_materias_curso
            ):
                self.__status = Situacao.aprovado.value
            elif quantidade_materias_cursadas < quantidade_materias_curso:
                self.__status = Situacao.in_progress.value
            else:
                self.__status = Situacao.reprovado.value
        return self

    def pega_situacao(self):
        return self.__status

    def get_status(self):
        return self.pega_situacao()

    def get_score(self):
        return self.__score

    def pega_coeficiente_rendimento(self, auto_calculo=False):
        """
        Args:
            auto_calculo (bool): informa se o cr será calculado antes de ser retornado
        Returns: coeficiente de rendimento calculado.
        """
        if auto_calculo:
            self._calcula_coficiente_rendimento()
        return self._coeficiente_rendimento

    def _calcula_coficiente_rendimento(self):
        quantidade = 0
        soma_notas = 0
        for key in self.__disciplines:
            soma_notas += self.__disciplines[key]
            quantidade += 1
        if soma_notas > 0:
            self._coeficiente_rendimento = soma_notas / quantidade
        return self
