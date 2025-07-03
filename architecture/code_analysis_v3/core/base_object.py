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
        return f"Name {name} NUI {self._nui}"

    def __repr__(self):
        return f"{self.__class__.__name__} NUI {self._nui} NAME '{self._name}'"

    @property
    def name(self) -> str:
        return self._name

    @property
    def nui(self) -> int:
        return self._nui


class NoneCoreObject(AbstractCoreObject):
    def __init__(self, name="None"):
        super().__init__(name)


class BasicInformation:
    def __init__(self, name, age) -> None:
        self._name: str = name
        self._age: int = age

    def __repr__(self):
        return f"{self.__class__.__name__} {vars(self)}"

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age
