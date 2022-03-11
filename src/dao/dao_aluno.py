from src.model.aluno import Aluno
from src.model.banco_dados import BancoDados
from src.dao.dao_base import DaoBase
from src.tabelas import alunos


class DaoAluno(DaoBase):
    def __init__(self, aluno: Aluno, bd: BancoDados):
        self._bd = bd
        self._tabela = alunos
        self.campo_1 = "nome"
        self.campo_2 = "cr"
        self.campo_3 = "situacao"
        self._campos = f"{self.campo_1}, {self.campo_2}, {self.campo_3}"
        self._aluno = aluno
        self.__student = aluno
        super().__init__(self._bd, self._tabela, self._campos)

    def salva(self):
        """Retorna objeto com campos atualizados via banco de dados"""
        self._bd.salva_registro(
            self._tabela,
            self._campos,
            (
                f"'{self._aluno.pega_nome()}', "
                f"{self._aluno.pega_coeficiente_rendimento()}, "
                f"'{self._aluno.pega_situacao()}'"
            ),
        )
        return True

    def atualiza(self, id_):
        query = f"{self.campo_2} = {self._aluno.pega_coeficiente_rendimento()}"

        if isinstance(self._aluno.pega_nome(), str):
            query += f", {self.campo_1} = '{self._aluno.pega_nome()}'"

        if isinstance(self._aluno.pega_situacao(), str):
            query += f", {self.campo_3} = '{self._aluno.pega_situacao()}'"

        self._bd.atualiza_registro(self._tabela, query, id_)
        return True

    def pega_por_id(self, id_):
        """
        Args:
            id (int): identificador do aluno
        Returns:
            objeto aluno com dados pegos do banco de dados
        """
        linha = super().pega_por_id(id_)
        return self.__tuple_to_object(linha[0])

    def pega_tudo(self):
        registros = super().pega_tudo()
        lista_alunos = list()
        for linha in registros:
            aluno = self.__tuple_to_object(linha)
            lista_alunos.append(aluno)
        return lista_alunos

    def get_all(self):
        return self.pega_tudo()

    def get_by_biggest_id(self):
        row = super().get_by_biggest_id()[0]
        return self.__tuple_to_object(row)

    def __tuple_to_object(self, row):
        (id_, name, cr, status) = row
        self.__student.define_id(id_)
        self.__student.define_nome(name)
        self.__student.define_cr(cr)
        self.__student.define_situacao(status)
        return self.__student
