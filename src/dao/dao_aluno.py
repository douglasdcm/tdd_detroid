from src.model.banco_dados import BancoDados
from src.dao.dao_base import DaoBase
from src.tabelas import alunos

class DaoAluno(DaoBase):
    def __init__(self, aluno, bd :BancoDados):
        self._bd = bd
        self._tabela = alunos
        campo_1 = "nome"
        campo_2 = "cr"
        campo_3 = "situacao"
        self._campos = f"{campo_1}, {campo_2}, {campo_3}"
        self._aluno = aluno
        super().__init__(self._bd, self._tabela, self._campos)
    
    def salva(self):
        self._bd.salva_registro(self._tabela, self._campos, \
                                f"'{self._aluno.pega_nome()}', \
                                   {self._aluno.pega_coeficiente_rendimento()}, \
                                   '{self._aluno.pega_situacao()}'")


