from src.dao.dao_fabrica import DaoFabrica


class Controller:

    def __init__(self, obj_dao, bd):
        """
            Args: obj_dao (Objeto): instância do objeto, exemplo: Aluno, Curso
        """
        self.dao = DaoFabrica(obj_dao, bd).fabrica_objetos_dao()

    def salva(self):
        try:
            return self.dao.salva()
        except Exception:
            raise

    def atualiza(self, id_):
        try:
            return self.dao.atualiza(id_)
        except Exception:
            raise

    def pega_registros(self):
        return self.dao.pega_tudo()

    def pega_registro_por_id(self, id_):
        """
        Args: id (int): id do objeto
        Returns: objeto Aluno com valores atualizados via banco de dados 
        """
        return self.dao.pega_por_id(id_)

    def pega_registro_por_query(self, query):
        return self.dao.pega_por_query(query)

    def deleta(self, id):
        return self.dao.deleta(id)
