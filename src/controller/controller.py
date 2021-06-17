from src.dao.dao_fabrica import DaoFabrica


class Controller:

    def __init__(self, obj, bd):
        self.dao = DaoFabrica(obj, bd).fabrica_objetos_dao()

    def salva(self):
        try:
            self.dao.salva()
        except Exception:
            raise

    def pega_registros(self):
        return self.dao.pega_tudo()

    def pega_registro_por_id(self, id):
        return self.dao.pega_por_id(id)

    def pega_registro_por_query(self, query):
        return self.dao.pega_por_query(query)

    def deleta(self, id):
        return self.dao.deleta(id)
