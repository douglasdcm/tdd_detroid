class CatalogoCurso:

    _instance = None
    _catalogo = list()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def adiciona_curso(cls, curso):
        cls._catalogo.append(curso)

    @classmethod
    def remove_curso(cls, curso):
        cls._catalogo.remove(curso)

    @classmethod
    def limpa_catalogo(cls):
        cls._catalogo.clear()

    @classmethod
    def pega_cursos(cls):
        return cls._catalogo