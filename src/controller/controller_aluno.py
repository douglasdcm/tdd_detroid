from src.dao.dao_fabrica import DaoFabrica

class ControllerAluno:

    def __init__(self, aluno, bd):
        self.dao = DaoFabrica(aluno, bd).fabrica_objetos_dao()

    def salva(self):
        self.dao.salva()

    def pega_registro(self):
        return self.dao.pega_tudo()