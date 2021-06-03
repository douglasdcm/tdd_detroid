from src.dao.dao_base import DaoBase
from src.tabelas import inscricao_aluno_curso

class DaoInscricao(DaoBase):

    def __init__(self, inscricao, bd):
        self._bd = bd
        self._tabela = inscricao_aluno_curso
        self._campos = "aluno_id, curso_id"
        self._inscricao = inscricao
        super().__init__(self._bd, self._tabela, self._campos)

    def salva(self):
        valores = f"'{self._inscricao.pega_aluno_id()}', \
            '{self._inscricao.pega_curso_id()}'"
        self._bd.salva_registro(self._tabela, self._campos, valores)