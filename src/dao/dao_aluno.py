from src.model.aluno import Aluno
from src.model.banco_dados import BancoDados
from src.dao.dao_base import DaoBase
from src.tabelas import alunos


class DaoAluno(DaoBase):
    def __init__(self, aluno: Aluno, bd: BancoDados):
        self._bd = bd
        self._tabela = alunos
        campo_1 = "nome"
        campo_2 = "cr"
        campo_3 = "situacao"
        self._campos = f"{campo_1}, {campo_2}, {campo_3}"
        self._aluno = aluno
        super().__init__(self._bd, self._tabela, self._campos)

    def salva(self):
        self._bd.salva_registro(self._tabela, self._campos,
                                (f"'{self._aluno.pega_nome()}', "
                                 f"{self._aluno.pega_coeficiente_rendimento()}, "
                                 f"'{self._aluno.pega_situacao()}'"))

    def pega_por_id(self, id):
        linha = super().pega_por_id(id)
        return self._tuple_para_aluno(linha[0])

    def pega_tudo(self):
        registros = super().pega_tudo()
        lista_alunos = list()
        for linha in registros:
            aluno = self._tuple_para_aluno(linha)
            lista_alunos.append(aluno)
        return lista_alunos

    def _tuple_para_aluno(self, linha):
        (id_, nome, cr, situacao) = linha
        aluno = Aluno(nome)
        aluno.define_id(id_)
        aluno.define_cr(cr)
        aluno.define_situacao(situacao)
        return aluno
