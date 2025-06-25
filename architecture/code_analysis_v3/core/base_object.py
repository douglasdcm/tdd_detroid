from architecture.code_analysis_v3.core.common import IState


class AbstractCoreObject:
    def __init__(self, name: str) -> None:
        self._nui: int
        self._state: IState

    def __str__(self):
        pass
