from architecture.code_analysis_v3.core.common import IState


class AbstractCoreObject:
    def __init__(self, name: str) -> None:
        self._nui: int = self.__hash__()
        self._state: IState
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class NoneCoreObject(AbstractCoreObject):
    def __init__(self, name=""):
        super().__init__(name)
