from _pytest.config import exceptions
from src.model.materia import Materia
from src.dao.dao_base import DaoBase
from src.tabelas import materias
from src.exceptions.exceptions import ErroMateriaSemNome


class DaoMateria(DaoBase):

    def __init__(self, materia: Materia, bd):
        self._bd = bd
        self._materia = materia
        self._campos = "nome"
        self._tabela = materias
        super().__init__(self._bd, self._tabela, self._campos)

    def salva(self):
        try:
            self._valida_campos()
            self._bd.salva_registro(self._tabela, self._campos,
                                    f"'{self._materia.pega_nome()}'")
        except Exception:
            raise ErroMateriaSemNome

    def _valida_campos(self):
        if self._materia.pega_nome() is None:
            raise ErroMateriaSemNome("""Matéria precisa ter nome para
                                     ser salva no banco de dados.""")

    def pega_por_id(self, id):
        registro = super().pega_por_id(id)
        (id_, nome) = registro[0]
        materia = Materia(nome)
        materia.define_id(id_)
        return materia
