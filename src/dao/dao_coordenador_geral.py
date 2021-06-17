from src.model.banco_dados import BancoDados
from src.model.coordenador_geral import CoordenadorGeral
from src.dao.dao_base import DaoBase
from src.tabelas import coordenador_geral


class DaoCoordenadorGeral(DaoBase):

    def __init__(self, obj: CoordenadorGeral, bd: BancoDados):
        self._bd = bd
        self._tabela = coordenador_geral
        self._campos = "_"
        super().__init__(self._bd, self._tabela, self._campos)

    def salva(self):
        self._bd.salva_registro(self._tabela, self._campos, "'_'")

    def pega_por_id(self, id):
        registro = super().pega_por_id(id)
        (id_, _) = registro[0]
        coordenador_geral = CoordenadorGeral()
        coordenador_geral.define_id(id_)
        return coordenador_geral
