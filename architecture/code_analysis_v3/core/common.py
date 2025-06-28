class AbstractState:
    def __repr__(self):
        return f"{self.__class__.__name__}"

    def get_next_state(self, context) -> "AbstractState":
        raise NotImplementedError


class NoneState(AbstractState):
    def get_next_state(self, context):
        return self
