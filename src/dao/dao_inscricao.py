from src.exceptions.exceptions import AlunoNaoEncontrado, CursoNaoEncontrado, ErroBancoDados
from _pytest.python_api import raises
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.dao.dao_base import DaoBase
from src.tabelas import inscricao_aluno_curso, alunos, cursos
from src.model.banco_dados import BancoDados

class DaoInscricao(DaoBase):

    def __init__(self, inscricao :InscricaoAlunoCurso, bd :BancoDados):
        self._bd = bd
        self._tabela = inscricao_aluno_curso
        self._campo_1 = "aluno_id"
        self._campo_2 = "curso_id"
        self._campos = f"{self._campo_1}, {self._campo_2}"
        self._complemento = f"FOREIGN KEY({self._campo_1}) REFERENCES {alunos}(id), \
                FOREIGN KEY({self._campo_2}) REFERENCES {cursos}(id)"
        self._inscricao = inscricao
        super().__init__(self._bd, self._tabela, self._campos, self._complemento)

    def salva(self):
        try:
            self._valida_valores()
            valores = f"'{self._inscricao.pega_aluno_id()}', \
                '{self._inscricao.pega_curso_id()}'"
            self._bd.salva_registro(self._tabela, self._campos, valores)
        except AlunoNaoEncontrado:
            raise AlunoNaoEncontrado("Aluno não encontrado.")
        except CursoNaoEncontrado:
            raise CursoNaoEncontrado("Curso não encontrado.")
        except Exception:
            raise ErroBancoDados()

    def _valida_valores(self):
        try:
            self._bd.pega_registro_por_id(alunos, self._inscricao.pega_aluno_id())
        except Exception:
            raise AlunoNaoEncontrado
        try:
            self._bd.pega_registro_por_id(cursos, self._inscricao.pega_curso_id())
        except Exception:
            raise CursoNaoEncontrado
