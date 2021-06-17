from src.dao.dao_base import DaoBase
from src.tabelas import associa_curso_materia, cursos, materias
from src.model.banco_dados import BancoDados
from src.model.associa_curso_materia import AssociaCursoMateria


class DaoAssociaCursoMateria(DaoBase):

    def __init__(self, objeto: AssociaCursoMateria, bd: BancoDados):
        self._bd = bd
        self._tabela = associa_curso_materia
        self._campo_1 = "curso_id"
        self._campo_2 = "materia_id"
        self._campos = f"{self._campo_1}, {self._campo_2}"
        self._complemento = f"""FOREIGN KEY({self._campo_1})
                             REFERENCES {cursos}(id),
                             FOREIGN KEY({self._campo_2})
                             REFERENCES {materias}(id)"""
        self._objeto = objeto
        super().__init__(self._bd, self._tabela, self._campos,
                         self._complemento)

    def salva(self):
        self._bd.salva_registro(self._tabela, self._campos,
                                f"""{self._objeto.pega_curso_id()},
                                    {self._objeto.pega_materia_id()}""")
