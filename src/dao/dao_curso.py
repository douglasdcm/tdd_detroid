from src.model.curso import Curso
from src.dao.dao_base import DaoBase
from src.model.banco_dados import BancoDados


class DaoCurso(DaoBase):
    def __init__(self, curso, bd) -> None:
        self._bd = bd
        self._tabela = "cursos"
        self._campos = "nome"
        self._curso = curso
        super().__init__(self._bd, self._tabela, self._campos)
    
    def salva(self):
        self._bd.salva_registro(self._tabela, self._campos, \
                                f"'{self._curso.pega_nome()}'")

