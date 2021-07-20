from src.model.i_model import IModel
from src.model.curso import Curso
from src.dao.dao_base import DaoBase
from src.model.banco_dados import BancoDados
from src.tabelas import cursos


class DaoCurso(DaoBase):
    def __init__(self, curso: Curso, bd: BancoDados):
        self._bd = bd
        self._tabela = cursos
        self._campos = "nome"
        self._curso = curso
        super().__init__(self._bd, self._tabela, self._campos)

    def salva(self):
        return self._bd.salva_registro(self._tabela, self._campos,
                                       f"'{self._curso.pega_nome()}'")

    def pega_tudo(self) -> list():
        registros = super().pega_tudo()
        lista = list()
        for linha in registros:
            (id_, nome) = linha
            curso = Curso(nome)
            curso.define_id(id_)
            lista.append(curso)
        return lista

    def pega_por_id(self, id):
        linha = super().pega_por_id(id)
        (id_, nome) = linha[0]
        curso = Curso(nome)
        curso.define_id(id_)
        return curso
