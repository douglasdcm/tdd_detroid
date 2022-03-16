from src.dao.dao_base import DaoBase
from src.tabelas import associa_curso_materia, cursos, materias
from src.model.banco_dados import BancoDados
from src.model.associa_curso_materia import AssociaCursoMateria
from src.controller import controller
from src.model.curso import Curso
from src.model.materia import Materia


class DaoAssociaCursoMateria(DaoBase):
    def __init__(self, objeto: AssociaCursoMateria, bd: BancoDados):
        self._bd = bd
        self.__db = bd
        self._tabela = associa_curso_materia
        self._campo_1 = "curso_id"
        self._campo_2 = "materia_id"
        self._campos = f"{self._campo_1}, {self._campo_2}"
        self._complemento = f"""FOREIGN KEY({self._campo_1})
                             REFERENCES {cursos}(id),
                             FOREIGN KEY({self._campo_2})
                             REFERENCES {materias}(id)"""
        self._objeto = objeto
        self.__assoc = objeto
        super().__init__(self._bd, self._tabela, self._campos, self._complemento)

    def salva(self):
        self._bd.salva_registro(
            self._tabela,
            self._campos,
            f"""{self._objeto.pega_curso_id()},
                                    {self._objeto.pega_materia_id()}""",
        )

        curso = self.__assoc.pega_curso()
        materia = self.__assoc.pega_materia()
        curso.atualiza_materias(materia)

        self.__assoc.atualiza_curso(curso)
        self.__assoc.atualiza_materia(materia)
        return True

    def get_by_biggest_id(self):
        row = super().get_by_biggest_id()[0]
        return self.__tuple_to_object(row)

    def __tuple_to_object(self, row):
        (id_, course_id, discipline_id) = row
        course_obj = controller.Controller(
            self.__assoc.pega_curso(), self.__db
        ).pega_registro_por_id(course_id)
        discipline_obj = controller.Controller(
            self.__assoc.pega_materia(), self.__db
        ).pega_registro_por_id(discipline_id)
        course_obj.atualiza_materias(discipline_obj)
        controller.Controller(course_obj, self.__db).update(course_id)
        self.__assoc.atualiza_curso(course_obj)
        self.__assoc.atualiza_materia(discipline_obj)
        return self.__assoc
