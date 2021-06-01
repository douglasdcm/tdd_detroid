from src.model.curso import Curso
from src.dao.dao_aluno import DaoAluno
from src.model.aluno import Aluno
from src.model.banco_dados import BancoDados
from src.dao.dao_curso import DaoCurso

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
        else:
            raise Exception("Objeto Dao não identificado.")