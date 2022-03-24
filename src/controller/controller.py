from src.dao.dao_fabrica import DaoFabrica


class Controller:
    def __init__(self, obj_dao, connection):
        """
        Args: obj_dao (Objeto): instância do objeto, exemplo: Aluno, Curso
        """
        self.dao = DaoFabrica(obj_dao, connection).fabrica_objetos_dao()

    def get_by_biggest_id(self):
        return self.dao.get_by_biggest_id()

    def salva(self):
        """Retorna objeto com campos atualizados via banco de dados"""
        try:
            return self.dao.salva()
        except Exception:
            raise

    def atualiza(self, id_):
        try:
            return self.dao.atualiza(id_)
        except Exception:
            raise

    def update(self, id_):
        return self.atualiza(id_)

    def pega_registros(self):
        return self.dao.pega_tudo()

    def get_all(self):
        return self.pega_registros()

    def pega_registro_por_id(self, id_):
        """
        Args: id (int): id do objeto
        Returns: objeto, por exemplo Aluno, com valores atualizados via banco de dados
        """
        return self.dao.pega_por_id(id_)

    def pega_registro_por_nome(self, nome):
        """
        Args: nome (str): nome do objeto
        Returns: objeto, por exemplo Aluno, com valores atualizados via banco de dados
        """
        try:
            return self.dao.pega_por_nome(nome)
        except Exception:
            raise

    def get_by_name(self, name):
        """
        Args: name (str): name do objeto
        Returns: objeto, por exemplo Aluno, com valores atualizados via banco de dados
        """
        try:
            return self.dao.get_by_name(name)
        except Exception:
            raise

    def pega_registro_por_query(self, query):
        return self.dao.pega_por_query(query)

    def deleta(self, id):
        return self.dao.deleta(id)
