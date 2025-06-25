class BaseCoreObject:
    def __init__(self, name: str) -> None:
        # name is the name defined by the user
        self._niu: int = self.__hash__()
        """The Unique Identifier Number of all objects"""

    def __str__(self):
        # TODO default implementation
        pass
