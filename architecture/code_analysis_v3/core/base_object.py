from architecture.code_analysis_v3.core.common import IState


class AbstractCoreObject:
    def __init__(self, name: str) -> None:
        self._nui: int = self.__hash__()
        self._state: IState
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def nui(self) -> int:
        return self._nui

    def __str__(self):
        return "Not found"

    def __repr__(self):
        return self._name


class NoneCoreObject(AbstractCoreObject):
    def __init__(self, name="None"):
        super().__init__(name)
