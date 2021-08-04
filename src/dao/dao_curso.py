from src.model.i_model import IModel
from src.model.curso import Curso
from src.dao.dao_base import DaoBase
from src.model.banco_dados import BancoDados
from src.tabelas import cursos
from src.dao.dao_associa_curso_materia import DaoAssociaCursoMateria
from src.model.associa_curso_materia import AssociaCursoMateria


class DaoCurso(DaoBase):
    def __init__(self, curso: Curso, bd: BancoDados):
        self._bd = bd
        self._tabela = cursos
        self._campos = "nome"
        self._curso = curso
        super().__init__(self._bd, self._tabela, self._campos)

    def salva(self):
        """Retorna objeto com campos atualizados via banco de dados"""
        linha = self._bd.salva_registro(self._tabela, self._campos,
                                        f"'{self._curso.pega_nome()}'")
        return self._tuple_para_objeto(linha[0])

    def pega_tudo(self) -> list():
        registros = super().pega_tudo()
        lista = list()
        for linha in registros:
            (id_, nome) = linha
            curso = Curso(nome)
            curso.define_id(id_)
            lista.append(curso)
        return lista

    def pega_por_nome(self, nome):
        try:
            registro = super().pega_por_nome(nome)
            (id_, nome) = registro[0]
            obj = Curso(nome)
            obj.define_id(id_)
            return obj
        except Exception:
            raise

    def pega_por_id(self, id):
        """
        Args:
            id (int): identificador do curso
        Returns:
            objeto curso com dados pegos do banco de dados
        """
        linha = super().pega_por_id(id)
        return self._tuple_para_objeto(linha[0])

    def _tuple_para_objeto(self, linha):
        (id_, nome) = linha
        curso = Curso(nome)
        curso.define_id(id_)
        return curso
