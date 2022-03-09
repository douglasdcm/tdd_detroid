from src.dao.dao_curso import DaoCurso
from src.model.curso import Curso
from src.model.aluno import Aluno
from src.dao.dao_aluno import DaoAluno
from src.exceptions.exceptions import AlunoNaoEncontrado, CursoNaoEncontrado, ErroBancoDados
from _pytest.python_api import raises
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.dao.dao_base import DaoBase
from src.tabelas import inscricao_aluno_curso, alunos, cursos
from src.model.banco_dados import BancoDados


class DaoInscricao(DaoBase):

    def __init__(self, inscricao: InscricaoAlunoCurso, bd: BancoDados):
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
            linha = self._bd.salva_registro(self._tabela, self._campos, valores)

            aluno, curso = self._tuple_para_objeto(linha[0])

            dao_aluno = DaoAluno(aluno, self._bd)
            aluno = dao_aluno.pega_por_id(aluno.pega_id())

            dao_curso = DaoCurso(curso, self._bd)
            curso = dao_curso.pega_por_id(curso.pega_id())

            aluno = self._inscricao.atualiza_aluno(aluno, curso)
            DaoAluno(aluno, self._bd).salva()
        except AlunoNaoEncontrado:
            raise AlunoNaoEncontrado("Aluno não encontrado.")
        except CursoNaoEncontrado:
            raise CursoNaoEncontrado("Curso não encontrado.")
        except Exception as e:
            raise ErroBancoDados(e)

    def _tuple_para_objeto(self, linha):
        (id_, aluno_id, curso_id) = linha
        aluno = Aluno()
        aluno.define_id(aluno_id)
        curso = Curso()
        curso.define_id(curso_id)
        return aluno, curso

    def _valida_valores(self):
        try:
            self._bd.pega_registro_por_id(alunos, self._inscricao.pega_aluno_id())
        except Exception:
            raise AlunoNaoEncontrado
        try:
            self._bd.pega_registro_por_id(cursos, self._inscricao.pega_curso_id())
        except Exception:
            raise CursoNaoEncontrado
