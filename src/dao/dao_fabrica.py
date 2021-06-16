from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.materia import Materia
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.model.curso import Curso
from src.dao.dao_aluno import DaoAluno
from src.model.aluno import Aluno
from src.model.banco_dados import BancoDados
from src.dao.dao_curso import DaoCurso
from src.dao.dao_inscricao import DaoInscricao
from src.dao.dao_materia import DaoMateria
from src.dao.dao_associa_curso_materia import DaoAssociaCursoMateria

class DaoFabrica:
    def __init__(self, obj, bd):
        self.obj = obj
        self.bd = bd

    def fabrica_objetos_dao(self):
        bd = BancoDados(self.bd)
        if isinstance(self.obj, Aluno):
            return DaoAluno(self.obj, bd)        
        if isinstance(self.obj, Curso):
            return DaoCurso(self.obj, bd)
        if isinstance(self.obj, InscricaoAlunoCurso):
            return DaoInscricao(self.obj, bd)
        if isinstance(self.obj, Materia):
            return DaoMateria(self.obj, bd)
        if isinstance(self.obj, AssociaCursoMateria):
            return DaoAssociaCursoMateria(self.obj, bd)
        else:
            raise Exception("Objeto Dao não identificado.")