from src.model.i_catalogo import ICatalogo


class Catalogo(ICatalogo):

    def __init__(self, obj):
        """
        Args:
            obj (Objeto): objeto a ser monipulado pelo catálog, por exemplo,
                Aluno, Curso
        """
        self._lista_obj = []

    def adiciona(self, obj):
        self._lista_obj.append(obj)

    def remove(self, obj):
        self._lista_obj.pop(obj)

    def lista(self):
        return self._lista_obj

    def lista_item(self, item):
        return self._lista_obj.index(item)
