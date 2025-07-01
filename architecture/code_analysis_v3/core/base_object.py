from core.common import AbstractState


class AbstractCoreObject:
    def __init__(self, name: str) -> None:
        self._nui: int = self.__hash__()
        self._state: AbstractState
        self._name = name

    def __str__(self):
        name = self.__class__.__name__
        if not name:
            return "Empty or not found"
        return f"Name {name}, NUI {self._nui}"

    def __repr__(self):
        return f"{self.__class__.__name__}, NUI {self._nui}, NAME '{self._name}'"

    @property
    def name(self) -> str:
        return self._name

    @property
    def nui(self) -> int:
        return self._nui


class NoneCoreObject(AbstractCoreObject):
    def __init__(self, name="None"):
        super().__init__(name)
