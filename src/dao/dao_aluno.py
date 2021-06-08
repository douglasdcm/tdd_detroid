from src.model.banco_dados import BancoDados
from src.dao.dao_base import DaoBase
from src.tabelas import alunos

class DaoAluno(DaoBase):
    def __init__(self, aluno, bd :BancoDados):
        self._bd = bd
        self._tabela = alunos
        self._campos = "nome"
        self._aluno = aluno
        super().__init__(self._bd, self._tabela, self._campos)
    
    def salva(self):
        self._bd.salva_registro(self._tabela, self._campos, \
                                f"'{self._aluno.pega_nome()}'")


